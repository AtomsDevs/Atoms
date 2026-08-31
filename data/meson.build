desktop_file = i18n.merge_file(
  input: 'pm.mirko.Atoms.desktop.in',
  output: 'pm.mirko.Atoms.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'pm.mirko.Atoms.appdata.xml.in',
  output: 'pm.mirko.Atoms.metainfo.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'metainfo')
)

appstream_cli = find_program('appstreamcli', required: false)
if appstream_cli.found()
  test('Validate AppStream metadata', appstream_cli,
    args: ['validate', '--no-net', appstream_file]
  )
endif

gnome.compile_schemas(
  build_by_default: true,
  depend_files: files('pm.mirko.Atoms.gschema.xml')
)

install_data(
  'pm.mirko.Atoms.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

gnome.post_install(glib_compile_schemas: true)

subdir('icons')
