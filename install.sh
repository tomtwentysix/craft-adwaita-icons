#!/usr/bin/env bash
# Installs the icons into the user hicolor theme, which is searched before /usr/share.
# PNGs are rendered at every fixed size too: GTK prefers an exact-size PNG from any base
# directory over a scalable SVG, so the SVG alone would not replace the packaged icons.
# Usage: ./install.sh [--uninstall]
set -euo pipefail

here=$(dirname "$(realpath "$0")")
dest=${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor
sizes=(16 24 32 48 64 128 256 512)

for svg in "$here"/icons/scalable/apps/*.svg; do
    id=$(basename "$svg" .svg)
    if [[ ${1:-} == --uninstall ]]; then
        rm -f "$dest/scalable/apps/$id.svg"
        for s in "${sizes[@]}"; do rm -f "$dest/${s}x${s}/apps/$id.png"; done
        continue
    fi
    install -Dm644 "$svg" "$dest/scalable/apps/$id.svg"
    for s in "${sizes[@]}"; do
        mkdir -p "$dest/${s}x${s}/apps"
        inkscape "$svg" -w "$s" -h "$s" -o "$dest/${s}x${s}/apps/$id.png" 2>/dev/null
    done
    echo "$id"
done

touch "$dest"
