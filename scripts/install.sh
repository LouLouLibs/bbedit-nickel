#!/bin/sh
# Install only this package; preserve existing installations as timestamped backups.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
support=${1:-"$HOME/Library/Application Support/BBEdit"}
target="$support/Packages/Nickel.bbpackage"
mkdir -p "$support/Packages"
if [ -e "$target" ] || [ -L "$target" ]; then
    backup="$support/Nickel-package-backups/$(date +%Y%m%d-%H%M%S)-$$"
    mkdir -p "$backup"
    mv "$target" "$backup/"
    printf 'Previous package saved in %s\n' "$backup"
fi
cp -R "$root/Nickel.bbpackage" "$target"
printf 'Installed %s\nQuit and reopen BBEdit to load Nickel.\n' "$target"
