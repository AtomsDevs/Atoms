using Gtk;

namespace Atoms {

    public Gtk.Image environment_icon (string icon_path,
                                       int size = 24,
                                       string fallback = "atoms-terminal-symbolic") {
        Gtk.Image image;
        if (icon_path != "" && FileUtils.test (icon_path, FileTest.IS_REGULAR))
            image = new Gtk.Image.from_file (icon_path);
        else
            image = new Gtk.Image.from_icon_name (fallback);
        image.pixel_size = size;
        return image;
    }

    public void add_environment_icon (Singularity.Widgets.ActionRow row,
                                      string icon_path,
                                      string fallback = "atoms-terminal-symbolic") {
        row.add_prefix (environment_icon (icon_path, 24, fallback));
    }

    public class EnvironmentSidebarRow : Singularity.Widgets.SidebarRow {
        public EnvironmentSidebarRow (Environment environment) {
            base ("atoms-terminal-symbolic", environment.display_name ());

            var content = new Gtk.Box (Orientation.HORIZONTAL, 12);
            content.append (environment_icon (environment.icon_path, 16));
            var label = new Gtk.Label (environment.display_name ());
            label.xalign = 0;
            label.hexpand = true;
            label.ellipsize = Pango.EllipsizeMode.END;
            content.append (label);
            set_child (content);
        }
    }

    public class PendingEnvironmentSidebarRow : Singularity.Widgets.SidebarRow {
        public PendingEnvironmentSidebarRow (Distribution distribution) {
            base ("atoms-package-symbolic", _("Creating..."));
            sensitive = false;

            var content = new Gtk.Box (Orientation.HORIZONTAL, 12);
            content.append (environment_icon (
                distribution.icon_path,
                16,
                "atoms-package-symbolic"
            ));
            var label = new Gtk.Label (_("Creating..."));
            label.xalign = 0;
            label.hexpand = true;
            content.append (label);
            set_child (content);
        }
    }
}
