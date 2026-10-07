<div align="center">

# bbedit-nickel
### Nickel language support for BBEdit

[![Version](https://img.shields.io/badge/version-0.1.0-1f5f8b)](CHANGELOG.md)
[![Vibecoded](https://img.shields.io/badge/vibecoded-%E2%9C%A8-blueviolet)](#a-word-on-vibe-coding)
[![BBEdit](https://img.shields.io/badge/BBEdit-14%2B-1f5f8b)](#requirements)
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](#requirements)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Contents

- [What is this?](#what-is-this)
- [A word on vibe coding](#a-word-on-vibe-coding)
- [What you get](#what-you-get)
- [Requirements](#requirements)
- [Install](#install)
- [Setup](#setup)
- [Everyday use](#everyday-use)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [License](#license)

## What is this?

A small package for editing [Nickel](https://nickel-lang.org/) configuration
files in BBEdit. Open a `.ncl` file and get syntax highlighting; add the Nickel
language server for completion, hover information, and diagnostics.

It's a standard **`Nickel.bbpackage`**, with a codeless language module inside.
No plug-in to compile and no server binary bundled. This is **v0.1.0**, tested
in BBEdit 15.5.5 with Nickel/NLS 1.18.0.

## A word on vibe coding

This project is **totally vibe coded**. The package, tests, and documentation
were written with an AI coding agent (Codex), with me describing what I wanted
and trying it in BBEdit.

The checks include highlighting regression tests, a real NLS protocol test,
and verification of syntax colors and live diagnostics in BBEdit itself.
There are still limits to what a codeless language module can do; see
[Limitations](#limitations), and
[open an issue](https://github.com/LouLouLibs/bbedit-nickel/issues) if something
looks wrong.

## What you get

- **Open and edit.** `.ncl` files are recognized as Nickel automatically.
- **Syntax colors.** Keywords, built-in types, `#` comments, quoted strings,
  multiline strings with matching `%` delimiters, and symbolic strings.
- **Line comments.** BBEdit's Un/Comment Selection command uses `#`.
- **Language server support.** The module is preconfigured to use `nls` for
  the completion, hover, and diagnostic features supported by BBEdit and NLS.

## Requirements

- A Mac with [BBEdit](https://www.barebones.com/products/bbedit/) **14 or later**.
- [Nickel Language Server](https://github.com/nickel-lang/nickel) (`nls`) for
  language-server features. Syntax highlighting works without it.
- For development only: Python 3 for the checks and release builder, and the
  Nickel CLI to evaluate the example.

## Install

**From a release:** grab `bbedit-nickel-0.1.0.zip` from
[Releases](https://github.com/LouLouLibs/bbedit-nickel/releases/latest), unzip it,
and copy `Nickel.bbpackage` into the folder opened by
**BBEdit → Folders → Packages**. This finds the right folder even if you use a
synchronized or custom support folder.

**From source:**

```sh
git clone https://github.com/LouLouLibs/bbedit-nickel.git
cd bbedit-nickel
./scripts/install.sh
```

For a custom support folder, pass its path:

```sh
./scripts/install.sh '/path/to/Application Support/BBEdit'
```

The installer backs up an existing Nickel package outside `Packages`.
**Quit and reopen BBEdit** after installing.

To uninstall, remove `Nickel.bbpackage` from the active `Packages` folder and
restart BBEdit. NLS is installed separately and is not removed.

## Setup

Install NLS using the [official Nickel instructions](https://nickel-lang.org/getting-started/),
or build it with Cargo:

```sh
cargo install --locked nickel-lang-lsp
nls --version
```

Installing `nickel` alone does not guarantee that `nls` is installed. Make sure
`nls --version` works in Terminal before checking the connection in BBEdit.

The package supplies these defaults:

| Setting | Value |
|---|---|
| Server command | `nls` |
| Language ID | `nickel` |
| Arguments | None |

BBEdit searches its `Language Servers` support folder, installed packages, and
the login shell's PATH. If it can't find NLS, put a symlink to your working
executable in the active `Language Servers` folder, or set its absolute path
in **Settings → Languages → Nickel → Server** and enable the server there.
Existing custom language settings can override the package defaults.

## Everyday use

1. Open a `.ncl` file with **File → Open…** (<kbd>⌘O</kbd>). The language menu
   at the bottom should say **Nickel**.
2. Edit as usual. With NLS running, try completion after `std.` or hover on a
   variable for information.
3. If there's a syntax error, use the document's diagnostics indicator to see
   what NLS found.

From Terminal, with BBEdit's command-line tools installed:

```sh
bbedit path/to/config.ncl
```

For a quick check, open [`examples/highlighting.ncl`](examples/highlighting.ncl).
It includes comments, contracts, enums, and multiline strings. Temporarily
replace the contents with `{ broken = }` to check diagnostics, then undo.

## Limitations

This is a codeless language module, not a complete Nickel parser:

- Interpolation is colored as part of its surrounding string. Nested quoted
  expressions inside interpolation may end coloring early.
- Incomplete strings may temporarily lose coloring.
- Function navigation, syntax-aware folding, semantic token coloring, and
  custom operator/enum colors are not provided. BBEdit applies its default
  number coloring.

Language-server features depend on both BBEdit and NLS. LSP does not supply
BBEdit's syntax coloring.

## Troubleshooting

**The file isn't highlighted.** Check that the language menu says **Nickel**,
that the package is in the active `Packages` folder, and that BBEdit has been
restarted since installation.

**Highlighting works, but the server doesn't.** Run `nls --version` in Terminal,
then check **Settings → Languages → Nickel → Server**. See
[BBEdit's LSP setup and troubleshooting guide](https://www.barebones.com/support/bbedit/lsp-notes.html)
for server discovery and logging.

**NLS 1.18.0 reports `dyld: Library not loaded`.** The official ARM64 executable
tested during development referenced a missing `/nix/store/.../libiconv.2.dylib`.
Building with Cargo avoids relying on that downloaded binary. For development
verification, a separate copy was relinked to macOS's `/usr/lib/libiconv.2.dylib`
and ad-hoc signed. That workaround is not bundled or applied automatically to
other users' installations.

## Development

```sh
make check                                   # plist validation and pattern tests
nickel export examples/highlighting.ncl       # evaluate the example
python3 scripts/check-lsp.py /path/to/nls      # initialize, hover, diagnostics, shutdown
make release                                 # build the package ZIP
```

The module lives in
[`Nickel.bbpackage/Contents/Language Modules/Nickel.plist`](Nickel.bbpackage/Contents/Language%20Modules/Nickel.plist).
The Python tests cover highlighting regression cases; check colors in BBEdit
before releasing, since its regex engine and language-module integration differ
from Python's.

`make release` creates `dist/bbedit-nickel-0.1.0.zip` with the package, README,
license, changelog, and example. It excludes local executables and machine-specific
configuration. Attach the ZIP to the matching GitHub release; update the version
in `scripts/release.py` and [`CHANGELOG.md`](CHANGELOG.md) together for new releases.

Useful references:

- [BBEdit codeless language modules](https://www.barebones.com/support/develop/clm.html)
- [BBEdit language server support](https://www.barebones.com/support/bbedit/lsp-notes.html)
- [Nickel source and releases](https://github.com/nickel-lang/nickel)

## License

[MIT](LICENSE)
