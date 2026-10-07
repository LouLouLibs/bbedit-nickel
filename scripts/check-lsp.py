#!/usr/bin/env python3
"""Exercise stdio LSP initialization, hover and diagnostics; no editor required."""
import json
import queue
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else 'nls'
    messages = queue.Queue()
    with tempfile.TemporaryDirectory(prefix='nickel-lsp-') as directory:
        path = Path(directory) / 'check.ncl'
        source = 'let answer = 42 in\n{ result = answer }\n'
        path.write_text(source)
        process = subprocess.Popen([command], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        def read():
            try:
                while True:
                    headers = {}
                    while True:
                        line = process.stdout.readline()
                        if not line:
                            raise EOFError('NLS closed stdout')
                        if line == b'\r\n':
                            break
                        key, value = line.decode().split(':', 1)
                        headers[key.lower()] = value.strip()
                    size = int(headers['content-length'])
                    messages.put(json.loads(process.stdout.read(size)))
            except Exception as error:
                messages.put(error)

        threading.Thread(target=read, daemon=True).start()

        def send(method, params=None, request_id=None):
            message = dict(jsonrpc='2.0', method=method)
            if params is not None:
                message['params'] = params
            if request_id is not None:
                message['id'] = request_id
            payload = json.dumps(message).encode()
            process.stdin.write(f'Content-Length: {len(payload)}\r\n\r\n'.encode() + payload)
            process.stdin.flush()

        def wait_for(predicate):
            deadline = time.monotonic() + 20
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('Timed out waiting for NLS')
                message = messages.get(timeout=remaining)
                if isinstance(message, Exception):
                    raise message
                if 'error' in message:
                    raise RuntimeError(message['error'])
                if predicate(message):
                    return message

        try:
            send('initialize', {'processId': None, 'rootUri': Path(directory).as_uri(),
                               'capabilities': {}}, 1)
            response = wait_for(lambda m: m.get('id') == 1)
            assert response['result']['capabilities']['hoverProvider']
            send('initialized', {})
            send('textDocument/didOpen', {'textDocument': {
                'uri': path.as_uri(), 'languageId': 'nickel', 'version': 1, 'text': source}})
            send('textDocument/hover', {'textDocument': {'uri': path.as_uri()},
                                       'position': {'line': 1, 'character': 13}}, 2)
            hover = wait_for(lambda m: m.get('id') == 2)
            assert hover['result'], 'No hover information returned'
            send('textDocument/didChange', {'textDocument': {'uri': path.as_uri(), 'version': 2},
                                           'contentChanges': [{'text': '{ broken = }'}]})
            diagnostics = wait_for(lambda m: m.get('method') == 'textDocument/publishDiagnostics'
                                   and m['params']['uri'] == path.as_uri()
                                   and bool(m['params']['diagnostics']))
            assert diagnostics['params']['diagnostics']
            send('shutdown', request_id=3)
            wait_for(lambda m: m.get('id') == 3)
            send('exit')
            process.wait(timeout=5)
            assert process.returncode == 0, process.returncode
            print('PASS: NLS initialization, hover, error diagnostics, and clean shutdown')
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()


if __name__ == '__main__':
    main()
