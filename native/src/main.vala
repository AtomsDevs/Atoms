using GLib;

namespace Atoms {

    public class AtomsApplication : Singularity.Application {
        private AtomsWindow? window;
        private ProviderRegistry registry;
        private GLib.Settings settings;
        private Gtk.CssProvider theme_provider;
        private bool smoke_mode;
        private bool automated_smoke;

        public int smoke_status { get; private set; default = 0; }

        public AtomsApplication () {
            bool is_smoke = GLib.Environment.get_variable ("ATOMS_SMOKE") == "1";
            bool is_visual_test = GLib.Environment.get_variable ("ATOMS_VISUAL_TEST") == "1";
            Object (
                application_id: is_smoke
                    ? "pm.mirko.Atoms.Smoke"
                    : is_visual_test
                        ? "pm.mirko.Atoms.VisualTest"
                        : "pm.mirko.Atoms",
                flags: ApplicationFlags.DEFAULT_FLAGS
            );
            smoke_mode = is_smoke || is_visual_test;
            automated_smoke = is_smoke;
            registry = new ProviderRegistry ();
            registry.load ();
            settings = new GLib.Settings ("pm.mirko.Atoms");
        }

        protected override void startup () {
            base.startup ();

            Gtk.Settings.get_default ().gtk_application_prefer_dark_theme = true;
            Singularity.Style.StyleManager.get_default ().apply_color_scheme (true);

            var provider = new Gtk.CssProvider ();
            provider.load_from_resource ("/pm/mirko/Atoms/style.css");
            Gtk.IconTheme.get_for_display (Gdk.Display.get_default ()).add_resource_path (
                "/pm/mirko/Atoms/icons"
            );
            Gtk.StyleContext.add_provider_for_display (
                Gdk.Display.get_default (),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            );

            theme_provider = new Gtk.CssProvider ();
            Gtk.StyleContext.add_provider_for_display (
                Gdk.Display.get_default (),
                theme_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1
            );
            settings.changed["color-scheme"].connect (() => apply_theme ());
            apply_theme ();
        }

        protected override void activate () {
            if (window == null)
                window = new AtomsWindow (this, registry, settings, smoke_mode);

            if (automated_smoke) {
                smoke_status = window.run_smoke_test () ? 0 : 1;
                Idle.add (() => {
                    quit ();
                    return Source.REMOVE;
                });
                return;
            }

            window.present ();
        }

        private void apply_theme () {
            string scheme = settings.get_string ("color-scheme");
            var theme = scheme == "auto"
                ? Singularity.Core.TerminalThemes.make_auto_theme (true)
                : Singularity.Core.TerminalThemes.get_by_id (scheme);
            if (theme == null)
                theme = Singularity.Core.TerminalThemes.get_by_id ("onedark");
            if (theme == null)
                return;
            theme_provider.load_from_string (
                ("@define-color atoms_terminal %s; " +
                 "@define-color atoms_terminal_text %s;").printf (
                    theme.background,
                    theme.foreground
                )
            );
            window?.apply_terminal_theme ();
        }
    }
}

int main (string[] args) {
    Intl.setlocale (GLib.LocaleCategory.ALL, "");
    string locale_dir = "/usr/share/locale";
    try {
        string executable = GLib.FileUtils.read_link ("/proc/self/exe");
        locale_dir = GLib.Path.build_filename (
            GLib.Path.get_dirname (GLib.Path.get_dirname (executable)),
            "share",
            "locale"
        );
    } catch (GLib.Error error) {
    }
    Intl.bindtextdomain ("atoms", locale_dir);
    Intl.bind_textdomain_codeset ("atoms", "UTF-8");
    Intl.textdomain ("atoms");

    var app = new Atoms.AtomsApplication ();
    int status = app.run (args);
    return status == 0 ? app.smoke_status : status;
}
