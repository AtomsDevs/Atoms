<div align="center">
  <img src="https://raw.githubusercontent.com/mirkobrombin/Atoms/main/data/icons/hicolor/scalable/apps/pm.mirko.Atoms.svg" width="64">
  <h1 align="center">Atoms</h1>
  <p align="center">Easily manage Linux chroot(s) with Atoms</p>
  <a href="https://www.codefactor.io/repository/github/mirkobrombin/atoms"><img src="https://www.codefactor.io/repository/github/mirkobrombin/atoms/badge" alt="CodeFactor" /></a>
</div>

<br/>

> ⚠️ Current state: Beta


### Supported Images
We are testing many images and more will be added in the future. Experimental images
can be enabled using the `SHOW_EXPERIMENTAL_IMAGES=1` environment variable.

#### Stable (know-working) images
- Alpine Linux
- Ubuntu
- Fedora

#### Experimental (not fully working) images
- Arch Linux

### Flatpak build dependencies
- `org.gnome.Platform`
- `org.gnome.Sdk`
- `org.gnome.Platform.Compat.i386`
- `org.freedesktop.Platform.GL32`
- `org.flatpak.Builder`


### Build & Run Flatpak

```bash
flatpak run org.flatpak.Builder build pm.mirko.Atoms.yml --user --install --force-clean
flatpak run pm.mirko.Atoms
```