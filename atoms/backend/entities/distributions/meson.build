pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
distributionsdir = join_paths(pkgdatadir, 'atoms/backend/entities/distributions')

atoms_sources = [
  '__init__.py',
  'unknown.py',
  'alpinelinux.py',
  'ubuntu.py',
  'archlinux.py',
  'debian.py',
  'fedora.py',
]

install_data(atoms_sources, install_dir: distributionsdir)
