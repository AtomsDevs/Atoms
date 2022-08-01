<div align="center">
  <img src="https://raw.githubusercontent.com/mirkobrombin/Atoms/main/data/icons/hicolor/scalable/apps/pm.mirko.Atoms.svg" width="64">
  <h1 align="center">Atoms</h1>
  <p align="center">Easily manage Linux chroot(s) with Atoms</p>
</div>

<br/>

> ⚠️ Under early development. The icon is temporary.


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