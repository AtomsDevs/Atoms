<div align="center">
  <img src="https://raw.githubusercontent.com/AtomsDevs/Atoms/main/data/icons/hicolor/scalable/apps/pm.mirko.Atoms.svg" width="64">
  <h1 align="center">Atoms</h1>
  <p align="center">Easily manage Linux chroot(s) with Atoms</p>
  <a href="https://www.codefactor.io/repository/github/AtomsDevs/Atoms"><img src="https://www.codefactor.io/repository/github/AtomsDevs/Atoms/badge" alt="CodeFactor" /></a>
</div>

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

### Install through Flathub

<a href='https://flathub.org/apps/details/pm.mirko.Atoms'>
  <img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/>
</a>

### Supported Images
We are testing many images and more will be added in the future. Experimental images
can be enabled using the `SHOW_EXPERIMENTAL_IMAGES=1` environment variable.

#### Stable (know-working) images
- Alpine Linux
- Ubuntu
- Fedora
- Alma Linux
- Centos
- Debian
- Gentoo
- OpenSUSE
- RockyLinux

#### Experimental (not fully working) images
- Arch Linux
- Void Linux

### Flatpak build dependencies
- `org.gnome.Platform`
- `org.gnome.Sdk`
- `org.gnome.Platform.Compat.i386`
- `org.freedesktop.Platform.GL32.default`
- `org.flatpak.Builder`


### Build & Run Flatpak
```bash
flatpak run org.flatpak.Builder build pm.mirko.Atoms.yml --user --install --force-clean
flatpak run pm.mirko.Atoms
```

### Enable distrobox integration
To enable the distrobox integration, you need to give Atoms the Flatpak permission
to talk to `org.freedesktop.Flatpak`.

### PROOT_NO_SECCOMP
To enable the `PROOT_NO_SECCOMP` option for old kernels, set the `ATOMS_NO_SECCOMP` env var to `1`.
