project('atoms', ['vala', 'c'],
          version: '2.0.0',
    meson_version: '>= 1.10.0',
  default_options: [ 'warning_level=2',
                     'werror=false',
                   ],
)

i18n = import('i18n')

gnome = import('gnome')

subdir('atoms-core/src')
subdir('atoms-provider-cpak/src')

posix_dep = meson.get_compiler('vala').find_library('posix')
subdir('atoms-cli/src')

subdir('data')
subdir('native')
subdir('po')

subdir('atoms-core/tests')
subdir('atoms-provider-cpak/tests')
subdir('atoms-cli/tests')

gnome.post_install(
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
