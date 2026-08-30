using GLib;

namespace Atoms {

    public class AtomsApplication : Singularity.Application {
        private AtomsWindow? window;
        private ProviderRegistry registry;
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
        }

        protected override void activate () {
            if (window == null)
                window = new AtomsWindow (this, registry, smoke_mode);

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
    }
}

int main (string[] args) {
    var app = new Atoms.AtomsApplication ();
    int status = app.run (args);
    return status == 0 ? app.smoke_status : status;
}
