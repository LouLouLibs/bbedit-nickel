"""Regression cases for the CLM's PCRE-compatible string/comment patterns."""
import plistlib
import re
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'Nickel.bbpackage/Contents/Language Modules/Nickel.plist'


class HighlightingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = plistlib.loads(MODULE.read_bytes())
        cls.strings = re.compile(cls.module['Language Features']['String Pattern'])
        cls.comments = re.compile(cls.module['Language Features']['Comment Pattern'])

    def test_strings(self):
        for source in ['"hello"', r'"an escaped \"quote\""', '"# not a comment"',
                       'm%"a "quoted"\nline"%', 'm%%"embedded "% delimiter"%%',
                       'json-s%"{"value": 1}"%', '"Hello, %{name}!"']:
            with self.subTest(source=source):
                self.assertIsNotNone(self.strings.fullmatch(source))

    def test_multiline_delimiters_must_match(self):
        source = 'm%%"one "% two"%%'
        self.assertEqual(self.strings.match(source).group(), source)

    def test_comment_stops_at_line_ending(self):
        for ending in ['\n', '\r', '\r\n']:
            self.assertEqual(self.comments.match('# hello' + ending + 'true').group(), '# hello')

    def test_identifier_does_not_split_at_hyphen_or_apostrophe(self):
        chars = self.module['Language Features']['Identifier and Keyword Character Class']
        self.assertIsNotNone(re.fullmatch('[' + chars + ']+', "default-value'"))


if __name__ == '__main__':
    unittest.main()
