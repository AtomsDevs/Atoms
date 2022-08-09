pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
wrappersdir = join_paths(pkgdatadir, 'atoms/backend/wrappers')

atoms_sources = [
  '__init__.py',
  'proot.py',
  'podman.py',
  'client_bridge.py',
  'launcher.sh',
]

install_data(atoms_sources, install_dir: wrappersdir)