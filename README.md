<div align="center">
  <img src="https://raw.githubusercontent.com/AtomsDevs/Atoms/main/data/icons/hicolor/scalable/apps/pm.mirko.Atoms.svg" width="64">
  <h1 align="center">Atoms</h1>
  <p align="center">Linux, one shell away.</p>
</div>

Atoms is a terminal-first desktop frontend for persistent Linux environments.
Each terminal runs inside a named environment with its own writable system
layer, home directory, permission policy, and lifecycle.

The native GTK4 frontend uses libsingularity and VTE. It supports terminal
tiling, tabs, real terminal history search, per-environment permissions, process
inspection, signals, restart, and deletion.

## Requirements

- atoms-core 2 and an Atoms provider
- GTK 4
- VTE for GTK 4
- libgee and JSON-GLib
- Meson and Vala for source builds

libsingularity is built from the pinned Meson wrap when it is not installed.

## Build and run

```sh
meson setup build-native
meson compile -C build-native
meson test -C build-native --print-errorlogs
build-native/native/atoms
```

The source tree builds atoms-core, atoms-cli, the cpak provider, and the GTK
frontend together. Each component remains available as a separate repository.

## cpak

cpak is the primary package format for Atoms:

```sh
cpak install github.com/atomsdevs/atoms
cpak run github.com/atomsdevs/atoms
```

The package requests typed access to cpak discovery and persistent environment
operations. It cannot invoke arbitrary host commands.

## Flatpak

```sh
flatpak install --user flathub org.gnome.Platform//50 org.gnome.Sdk//50
flatpak install --user flathub org.flatpak.Builder
flatpak run org.flatpak.Builder flatpak-build pm.mirko.Atoms.yml --user --install --force-clean
flatpak run pm.mirko.Atoms
```

The bundled provider requires cpak to be installed on the host. Its
`org.freedesktop.Flatpak` access is used only to invoke the cpak CLI outside the
application sandbox, where cpak applies the selected environment policy.

## Providers

Atoms loads native providers through the atoms-core ABI. The bundled cpak
provider reads available distributions from the `Distributions` category of
the cpak Store, so the application does not carry a fixed distribution list.

To add a distribution to the original Atoms workflow, publish it as a cpak and
submit it to that Store category. See the [cpak documentation](https://github.com/Containerpak/docs)
and the [Store repository](https://github.com/Containerpak/store).
