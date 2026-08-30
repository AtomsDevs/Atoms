#!/bin/sh
set -eu

native_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
repo_dir=$(CDPATH='' cd -- "$native_dir/.." && pwd)
build_dir="$repo_dir/build-native"

if [ ! -d "$build_dir" ]; then
    meson setup "$build_dir" "$repo_dir"
else
    meson setup --reconfigure "$build_dir" "$repo_dir"
fi

meson compile -C "$build_dir"
"$build_dir/native/atoms"
