<div align="center">
  <img src="https://raw.githubusercontent.com/AtomsDevs/Atoms/main/data/icons/hicolor/scalable/apps/pm.mirko.Atoms.svg" width="64">
  <h1 align="center">Atoms</h1>
  <p align="center">Easily manage Linux chroot(s) with Atoms</p>
  <a href="https://www.codefactor.io/repository/github/AtomsDevs/Atoms"><img src="https://www.codefactor.io/repository/github/AtomsDevs/Atoms/badge" alt="CodeFactor" /></a>
</div>

<br/>

> ⚠️ Current state: Beta

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/AtomsDevs/Atoms/main/screenshot.png">
</div>

### Why a new application?
Atoms was created to solve the lack of a GUI to create, manage and use chroot 
environments. Although there is support for Distrobox, Atoms does not aim to offer 
a fine integration with Podman as its purpose is only to allow the user to open a 
shell in a new environment, be it chroot or container.

If you are looking for a Podman container manager that does a finer job offering 
more accurate management and more features, check out [pods](https://github.com/marhkb/pods).

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