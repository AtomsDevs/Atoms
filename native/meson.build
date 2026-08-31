gnome = import('gnome')

gtk_dep = dependency('gtk4')
vte_dep = dependency('vte-2.91-gtk4')
gee_dep = dependency('gee-0.8')
if not is_variable('atoms_core_dep')
  atoms_core_dep = dependency('atoms-core-2', version: '>= 2.0.0')
endif
libpeas_dep = dependency('libpeas-2', version: '>= 2.0')
libsingularity_dep = dependency(
  'singularity-1.0',
  fallback: ['libsingularity', 'libsingularity_dep'],
  default_options: ['system=false', 'introspection=false']
)

libsingularity_vapi_args = []
if not meson.is_subproject() and libsingularity_dep.type_name() == 'internal'
  libsingularity_vapi_dir = join_paths(
    meson.project_build_root(),
    'subprojects',
    'libsingularity'
  )
  libsingularity_vapi_args = ['--vapidir=' + libsingularity_vapi_dir]
endif

native_config = configuration_data()
native_config.set_quoted('APP_VERSION', meson.project_version())
native_build_config = configure_file(
  input: 'src/build_config.vala.in',
  output: 'build_config.vala',
  configuration: native_config
)

resources = gnome.compile_resources(
  'atoms-resources',
  'resources/pm.mirko.Atoms.gresource.xml',
  source_dir: meson.current_source_dir() / 'resources'
)

atoms = executable(
  'atoms',
  files(
    'src/main.vala',
    'src/models.vala',
    'src/widgets.vala',
    'src/leaf_pane.vala',
    'src/dialogs.vala',
    'src/window.vala'
  ) + [native_build_config, resources],
  dependencies: [
    gtk_dep,
    vte_dep,
    gee_dep,
    atoms_core_dep,
    libpeas_dep,
    libsingularity_dep,
    posix_dep
  ],
  vala_args: libsingularity_vapi_args,
  install: true,
  install_rpath: get_option('prefix') / get_option('libdir')
)

test_env = environment()
test_env.set('ATOMS_SMOKE', '1')
test_env.set('GSETTINGS_SCHEMA_DIR', meson.project_build_root() / 'data')

test(
  'native-smoke',
  atoms,
  env: test_env,
  timeout: 30
)
