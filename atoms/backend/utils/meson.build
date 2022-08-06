pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
utilsdir = join_paths(pkgdatadir, 'atoms/backend/utils')

atoms_sources = [
  '__init__.py',
  'paths.py',
  'distribution.py',
  'image.py',
  'file.py',
  'download.py',
  'hash.py'
]

install_data(atoms_sources, install_dir: utilsdir)