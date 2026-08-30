#!/bin/sh
set -eu

flatpak run org.flatpak.Builder flatpak-build pm.mirko.Atoms.prod.yml \
    --user \
    --install \
    --force-clean
