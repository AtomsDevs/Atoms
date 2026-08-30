#!/bin/sh
set -eu

build_dir=${1:-build-native}

if [ -d "$build_dir" ]; then
    meson setup --reconfigure "$build_dir"
else
    meson setup "$build_dir"
fi

meson compile -C "$build_dir"
meson test -C "$build_dir" --print-errorlogs
