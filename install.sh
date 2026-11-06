#!/usr/bin/env bash
# Installs the icons into the user hicolor theme, which is searched before /usr/share.
# The PNGs matter: GTK prefers an exact-size PNG from any base directory over a scalable
# SVG, so the SVGs alone would not replace the packaged icons.
# Usage: ./install.sh [--uninstall]
set -euo pipefail

src=$(dirname "$(realpath "$0")")/icons
dest=${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor

cd "$src"
for f in */apps/*; do
    if [[ ${1:-} == --uninstall ]]; then
        rm -f "$dest/$f"
    else
        install -Dm644 "$f" "$dest/$f"
    fi
done

touch "$dest"
