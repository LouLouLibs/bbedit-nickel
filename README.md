# Nickel for BBEdit

A BBEdit package from louloulibs for editing [Nickel](https://nickel-lang.org/) configuration files.

- Automatic language selection for `.ncl` files.
- Syntax coloring for keywords, built-in types, `#` comments, quoted strings,
  multiline strings with matching `%` delimiters, and symbolic strings.
- Line commenting with BBEdit's Un/Comment Selection command.
- Preconfigured connection to the Nickel language server, `nls`, for the LSP
  features supported by BBEdit and NLS, including completion, hover and diagnostics.

Requires macOS and BBEdit 14 or later. Install NLS separately for language-server
features; syntax coloring works without it. No server binary is bundled.

## Install

Download and unzip the [latest release](https://github.com/louloulibs/bbedit-nickel/releases/latest), then copy `Nickel.bbpackage` into BBEdit's
`Packages` folder. Use **BBEdit → Folders → Packages** to locate the active folder,
especially if you use a synchronized or custom support folder.

From a source checkout, run:

```sh
./scripts/install.sh
# Or supply your active BBEdit support folder:
./scripts/install.sh '/path/to/Application Support/BBEdit'
```

The installer backs up an existing Nickel package outside `Packages`. Quit and
reopen BBEdit after installing, then open `examples/highlighting.ncl`.
The document's language should be **Nickel**.

## Enable the language server

Install NLS using the [official Nickel instructions](https://nickel-lang.org/getting-started/)
or build it with Cargo:

```sh
cargo install --locked nickel-lang-lsp
nls --version
```

Installing `nickel` alone does not guarantee that `nls` is installed. The server
must start successfully from Terminal before BBEdit can use it.

The module sets **Command: `nls`**, **Language ID: `nickel`**, with no arguments.
BBEdit searches its `Language Servers` support folder, installed packages, and
the login shell's PATH. If necessary, put a symlink to your working NLS executable
in BBEdit's active `Language Servers` folder. Alternatively, set its absolute
path in **Settings → Languages → Nickel → Server** and enable the server there.
Existing custom language settings can override the package defaults.

Open the example and try completion after `std.`, hover on a variable, and
temporarily enter `{ broken = }` to check error diagnostics. Restore the file
afterward. BBEdit's Languages settings show the server's availability; consult
its LSP troubleshooting documentation below if the connection fails.

### NLS 1.18.0 macOS binary issue

The official ARM64 executable tested during development referenced a missing
`/nix/store/.../libiconv.2.dylib`. That causes a `dyld: Library not loaded` failure
before LSP starts. Building with Cargo avoids relying on that downloaded binary.
For development verification, a separate copy was relinked to macOS's
`/usr/lib/libiconv.2.dylib` and ad-hoc signed. This workaround is not embedded in
the package or applied automatically to other users' installations.

## Highlighting limits

This is a codeless language module, not a complete Nickel parser. Interpolation
is colored as part of its surrounding string; nested quoted expressions inside
interpolation may end coloring early. Incomplete strings may temporarily lose
coloring. Function navigation, syntax-aware folding, semantic token coloring,
and custom operator/enum colors are not provided. BBEdit also applies its default
number coloring. NLS features depend on both the server and BBEdit; LSP does not
supply BBEdit's syntax coloring.

## Develop and publish

```sh
make check
nickel export examples/highlighting.ncl
python3 scripts/check-lsp.py /absolute/path/to/nls
make release
```

`make release` creates `dist/bbedit-nickel-0.1.0.zip`, containing the package,
documentation, MIT license, and example. It excludes local executables and
machine-specific configuration. The Python pattern tests cover key regression
cases; check actual coloring in BBEdit before releasing because its regex engine
and CLM integration differ from Python's.

Version 0.1.0 was checked on BBEdit 15.5.5 with Nickel/NLS 1.18.0: automatic
language detection and string/comment/keyword coloring were verified in the
editor, and a temporary syntax error produced an NLS diagnostic in BBEdit.
The protocol smoke test also verified hover and clean server shutdown.

Source: [louloulibs/bbedit-nickel](https://github.com/louloulibs/bbedit-nickel).
Attach the ZIP to the matching version's GitHub release. Neither running the
installer nor building the archive publishes anything. Update the version in
`scripts/release.py` and `CHANGELOG.md` together for subsequent releases.

To uninstall, remove `Nickel.bbpackage` from the active `Packages` folder and
restart BBEdit. NLS is independently installed and is not removed.

## References

- [BBEdit codeless language modules](https://www.barebones.com/support/develop/clm.html)
- [BBEdit LSP setup and troubleshooting](https://www.barebones.com/support/bbedit/lsp-notes.html)
- [Nickel source and releases](https://github.com/nickel-lang/nickel)

MIT licensed; see [LICENSE](LICENSE).
