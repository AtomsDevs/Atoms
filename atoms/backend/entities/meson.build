pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
entitiesdir = join_paths(pkgdatadir, 'atoms/backend/entities')

subdir('distributions')

atoms_sources = [
  '__init__.py',
  'config.py',
  'atom.py',
  'image.py',
  'result.py',
  'distribution.py',
]

install_data(atoms_sources, install_dir: entitiesdir)