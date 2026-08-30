using Gtk;
using Vte;
using Gee;

namespace Atoms {

    public enum TerminalDropZone {
        LEFT,
        RIGHT,
        TOP,
        BOTTOM,
        CENTER
    }

    private class TerminalDragPayload : Object {
        public string id;

        public TerminalDragPayload (string id) {
            this.id = id;
        }
    }

    public class LeafPane : Gtk.Box {
        public string pane_id { get; private set; }
        public Environment environment { get; private set; }
        public int tab_count { get { return tabs.size; } }
        public bool tab_bar_visible { get { return chip_bar.visible; } }
        public int background_process_count {
            get {
                var tab = active_tab ();
                return tab != null ? tab.background_processes : 0;
            }
        }

        private Gtk.Window host_window;
        private ProviderRegistry registry;
        private bool smoke_mode;
        private Gtk.Stack terminal_stack;
        private Singularity.Widgets.ChipBar chip_bar;
        private Singularity.Widgets.HoverControls hover_controls;
        private Gtk.DrawingArea drop_overlay;
        private TerminalDropZone drop_zone = TerminalDropZone.CENTER;
        private ArrayList<TerminalTab> tabs;
        private Singularity.Widgets.ContextMenu? add_menu;
        private int tab_sequence = 0;

        public signal void focused (LeafPane terminal);
        public signal void new_terminal_requested (LeafPane terminal);
        public signal void new_tab_requested (LeafPane terminal);
        public signal void search_requested (LeafPane terminal);
        public signal void process_manager_requested (LeafPane terminal);
        public signal void settings_requested (LeafPane terminal);
        public signal void close_requested (LeafPane terminal);
        public signal void close_all_requested ();
        public signal void move_requested (string source_id,
                                           LeafPane target,
                                           TerminalDropZone zone);
        public signal void status_changed (LeafPane terminal);

        public LeafPane (Gtk.Window host_window,
                         Environment environment,
                         ProviderRegistry registry,
                         bool smoke_mode = false) {
            Object (orientation: Orientation.VERTICAL, spacing: 0);
            this.host_window = host_window;
            this.environment = environment;
            this.registry = registry;
            this.smoke_mode = smoke_mode;
            pane_id = GLib.Uuid.string_random ();

            hexpand = true;
            vexpand = true;
            add_css_class ("atoms-terminal");

            tabs = new ArrayList<TerminalTab> ();
            terminal_stack = new Gtk.Stack ();
            terminal_stack.hexpand = true;
            terminal_stack.vexpand = true;

            build_hover_controls ();

            var terminal_overlay = new Gtk.Overlay ();
            terminal_overlay.hexpand = true;
            terminal_overlay.vexpand = true;
            terminal_overlay.set_child (hover_controls);

            drop_overlay = new Gtk.DrawingArea ();
            drop_overlay.hexpand = true;
            drop_overlay.vexpand = true;
            drop_overlay.can_target = false;
            drop_overlay.visible = false;
            drop_overlay.set_draw_func (draw_drop_zone);
            terminal_overlay.add_overlay (drop_overlay);
            append (terminal_overlay);

            install_drop_target ();

            chip_bar = new Singularity.Widgets.ChipBar ();
            chip_bar.add_css_class ("atoms-terminal-tabs");
            chip_bar.reorderable = true;
            chip_bar.chip_activated.connect (activate_tab);
            chip_bar.chip_closed.connect (close_tab);
            chip_bar.visible = false;
            append (chip_bar);

            var focus = new Gtk.EventControllerFocus ();
            focus.enter.connect (() => focused (this));
            add_controller (focus);

            add_tab (environment);
        }

        private void build_hover_controls () {
            hover_controls = Singularity.Widgets.HoverControls.with_window_bubbles (
                host_window,
                false,
                true
            );
            hover_controls.add_css_class ("singularity-hover-on-content");
            hover_controls.set_content (terminal_stack);

            var drag_button = new Gtk.Button ();
            drag_button.add_css_class ("flat");
            drag_button.add_css_class ("atoms-terminal-drag");
            drag_button.tooltip_text = "Move terminal";
            drag_button.set_child (new Gtk.Image.from_icon_name (
                "atoms-terminal-drag-symbolic"
            ));

            var drag = new Gtk.DragSource ();
            drag.set_actions (Gdk.DragAction.MOVE);
            drag.prepare.connect ((x, y) => {
                return new Gdk.ContentProvider.for_value (
                    new TerminalDragPayload (pane_id)
                );
            });
            drag.drag_begin.connect ((native_drag) => {
                var paintable = new Gtk.WidgetPaintable (drag_button);
                drag.set_icon (
                    paintable,
                    drag_button.get_width () / 2,
                    drag_button.get_height () / 2
                );
                drag_button.add_css_class ("dragging");
            });
            drag.drag_end.connect ((native_drag, delete_data) => {
                drag_button.remove_css_class ("dragging");
            });
            drag_button.add_controller (drag);
            hover_controls.add_control (drag_button);

            var add_button = new Gtk.Button.from_icon_name ("list-add-symbolic");
            add_button.tooltip_text = "Create terminal or tab";
            add_button.clicked.connect (() => open_add_menu (add_button));
            hover_controls.add_control (add_button);

            var search_button = new Gtk.Button.from_icon_name ("system-search-symbolic");
            search_button.tooltip_text = "Commands and terminal history";
            search_button.clicked.connect (() => search_requested (this));
            hover_controls.add_control (search_button);

            var processes_button = new Gtk.Button.from_icon_name (
                "atoms-process-monitor-symbolic"
            );
            processes_button.tooltip_text = "Environment processes";
            processes_button.clicked.connect (() => process_manager_requested (this));
            hover_controls.add_control (processes_button);

            var settings_button = new Gtk.Button.from_icon_name ("emblem-system-symbolic");
            settings_button.tooltip_text = "Environment settings";
            settings_button.clicked.connect (() => settings_requested (this));
            hover_controls.add_control (settings_button);

            hover_controls.add_close_menu_item (
                "Close Terminal",
                "window-close-symbolic",
                () => close_requested (this)
            );
            hover_controls.add_close_menu_separator ();
            hover_controls.add_close_menu_item (
                "Close All Terminals",
                "application-exit-symbolic",
                () => close_all_requested ()
            );
        }

        private void install_drop_target () {
            var target = new Gtk.DropTarget (
                typeof (TerminalDragPayload),
                Gdk.DragAction.MOVE
            );
            target.motion.connect ((x, y) => {
                drop_zone = drop_zone_at (x, y);
                drop_overlay.visible = true;
                drop_overlay.queue_draw ();
                return Gdk.DragAction.MOVE;
            });
            target.leave.connect (() => drop_overlay.visible = false);
            target.drop.connect ((value, x, y) => {
                drop_overlay.visible = false;
                var payload = value.get_object () as TerminalDragPayload;
                if (payload == null || payload.id == pane_id)
                    return false;

                move_requested (payload.id, this, drop_zone_at (x, y));
                return true;
            });
            add_controller (target);
        }

        private TerminalDropZone drop_zone_at (double x, double y) {
            double width = double.max (1.0, get_width ());
            double height = double.max (1.0, get_height ());
            double nx = x / width;
            double ny = y / height;
            if (nx >= 0.25 && nx <= 0.75 && ny >= 0.25 && ny <= 0.75)
                return TerminalDropZone.CENTER;

            double edge = nx;
            TerminalDropZone zone = TerminalDropZone.LEFT;
            if (1.0 - nx < edge) {
                edge = 1.0 - nx;
                zone = TerminalDropZone.RIGHT;
            }
            if (ny < edge) {
                edge = ny;
                zone = TerminalDropZone.TOP;
            }
            if (1.0 - ny < edge)
                zone = TerminalDropZone.BOTTOM;
            return zone;
        }

        private void draw_drop_zone (Gtk.DrawingArea area,
                                     Cairo.Context cr,
                                     int width,
                                     int height) {
            double x = 0;
            double y = 0;
            double w = width;
            double h = height;
            switch (drop_zone) {
                case TerminalDropZone.LEFT:
                    w /= 2;
                    break;
                case TerminalDropZone.RIGHT:
                    x = width / 2.0;
                    w /= 2;
                    break;
                case TerminalDropZone.TOP:
                    h /= 2;
                    break;
                case TerminalDropZone.BOTTOM:
                    y = height / 2.0;
                    h /= 2;
                    break;
                case TerminalDropZone.CENTER:
                    x = width * 0.2;
                    y = height * 0.2;
                    w = width * 0.6;
                    h = height * 0.6;
                    break;
            }

            Gdk.RGBA accent = {};
            accent.parse ("#326fd1");
            cr.rectangle (x + 3, y + 3, double.max (0, w - 6), double.max (0, h - 6));
            cr.set_source_rgba (accent.red, accent.green, accent.blue, 0.24);
            cr.fill_preserve ();
            cr.set_source_rgba (accent.red, accent.green, accent.blue, 0.9);
            cr.set_line_width (2);
            cr.stroke ();
        }

        private void open_add_menu (Gtk.Button anchor) {
            add_menu = new Singularity.Widgets.ContextMenu (anchor);
            Gdk.Rectangle rect = { 0, 0, 1, 1 };
            add_menu.set_pointing_to (rect);
            add_menu.add_item (
                "New Terminal",
                "atoms-terminal-symbolic",
                () => new_terminal_requested (this)
            );
            add_menu.add_item (
                "New Tab",
                "atoms-tab-new-symbolic",
                () => new_tab_requested (this)
            );
            add_menu.closed.connect (() => {
                add_menu.unparent ();
                add_menu = null;
            });
            add_menu.popup ();
        }

        public void set_active (bool active) {
            if (active)
                add_css_class ("active");
            else
                remove_css_class ("active");
        }

        public void switch_environment (Environment profile) {
            environment = profile;
            reset_tabs ();
        }

        public void restart () {
            reset_tabs ();
        }

        public void add_tab (Environment? profile = null) {
            var tab_environment = profile ?? environment;
            tab_sequence++;
            string id = GLib.Uuid.string_random ();
            string label = tab_sequence == 1
                ? "Terminal"
                : "Terminal %d".printf (tab_sequence);
            var terminal = configure_terminal ();
            var tab = new TerminalTab (id, label, terminal, tab_environment);
            install_history_capture (tab);
            terminal.child_exited.connect ((status) => {
                tab.shell_pid = 0;
                status_changed (this);
            });
            tabs.add (tab);
            terminal_stack.add_named (terminal, id);
            chip_bar.add_chip (id, label);
            sync_tab_bar ();
            spawn_terminal (tab);
            activate_tab (id);
        }

        private Vte.Terminal configure_terminal () {
            var terminal = new Vte.Terminal ();
            terminal.hexpand = true;
            terminal.vexpand = true;
            terminal.set_scrollback_lines (10000);
            terminal.set_audible_bell (false);

            Gdk.RGBA background = {};
            Gdk.RGBA foreground = {};
            background.parse ("#171a20");
            foreground.parse ("#d8dee9");
            terminal.set_color_background (background);
            terminal.set_color_foreground (foreground);

            var click = new Gtk.GestureClick ();
            click.pressed.connect ((n, x, y) => focused (this));
            terminal.add_controller (click);

            return terminal;
        }

        private void install_history_capture (TerminalTab tab) {
            var keys = new Gtk.EventControllerKey ();
            keys.set_propagation_phase (Gtk.PropagationPhase.CAPTURE);
            keys.key_pressed.connect ((keyval, keycode, state) => {
                if (keyval == Gdk.Key.Return || keyval == Gdk.Key.KP_Enter)
                    capture_current_command (tab);
                return false;
            });
            tab.terminal.add_controller (keys);
        }

        private void capture_current_command (TerminalTab tab) {
            string? contents = tab.terminal.get_text_format (Vte.Format.TEXT);
            if (contents == null)
                return;

            var lines = contents.split ("\n");
            for (int i = lines.length - 1; i >= 0; i--) {
                string command = command_from_terminal_line (lines[i]);
                if (command == "")
                    continue;
                record_history_command (tab, command);
                return;
            }
        }

        private string command_from_terminal_line (string line) {
            string command = line.strip ();
            foreach (var prompt in new string[] { "$ ", "# ", "> " }) {
                int position = command.last_index_of (prompt);
                if (position >= 0) {
                    command = command.substring (position + prompt.length).strip ();
                    break;
                }
            }
            return command;
        }

        private void record_history_command (TerminalTab tab, string command) {
            if (command == "")
                return;
            if (tab.history.size > 0 && tab.history[0] == command)
                return;

            tab.history.insert (0, command);
            if (tab.history.size > 100)
                tab.history.remove_at (tab.history.size - 1);
        }

        private void spawn_terminal (TerminalTab tab) {
            var envv = GLib.Environ.get ();
            envv = GLib.Environ.set_variable (
                (owned) envv,
                "ATOMS_ENVIRONMENT",
                tab.environment.id,
                true
            );
            envv = GLib.Environ.set_variable (
                (owned) envv,
                "PS1",
                "[atoms:%s] \\w $ ".printf (tab.environment.name.down ()),
                true
            );
            envv = GLib.Environ.set_variable (
                (owned) envv,
                "TERM",
                "xterm-256color",
                true
            );

            string[] argv;
            try {
                argv = smoke_mode
                    ? new string[] { "/bin/bash", "--noprofile", "--norc", "-i" }
                    : registry.require (tab.environment.provider_id).shell_argv (
                        tab.environment,
                        "/bin/bash",
                        { "-i" }
                    );
            } catch (Error error) {
                string message = "Unable to open environment: %s\r\n".printf (
                    error.message
                );
                tab.terminal.feed (message.data);
                return;
            }
            tab.terminal.spawn_async (
                Vte.PtyFlags.DEFAULT,
                GLib.Environment.get_home_dir (),
                argv,
                envv,
                (GLib.SpawnFlags) 0,
                null,
                -1,
                tab.spawn_cancellable,
                (source, pid, error) => {
                    if (error != null) {
                        if (!tab.closing)
                            warning ("Terminal spawn failed: %s", error.message);
                        return;
                    }

                    tab.shell_pid = (int) pid;
                    if (tab.closing) {
                        Posix.kill ((Posix.pid_t) pid, Posix.Signal.TERM);
                        tab.shell_pid = 0;
                        return;
                    }
                    status_changed (this);
                }
            );
        }

        public TerminalTab? active_tab () {
            string? id = terminal_stack.visible_child_name;
            if (id == null)
                return null;

            foreach (var tab in tabs) {
                if (tab.id == id)
                    return tab;
            }
            return null;
        }

        public void insert_history_command (string command) {
            var tab = active_tab ();
            if (tab == null)
                return;

            tab.terminal.feed_child (command.data);
            tab.terminal.grab_focus ();
        }

        public ArrayList<string> active_history () {
            var tab = active_tab ();
            return tab != null ? tab.history : new ArrayList<string> ();
        }

        public void add_history_for_test (string command) {
            var tab = active_tab ();
            if (tab != null)
                record_history_command (tab, command);
        }

        private void activate_tab (string id) {
            terminal_stack.visible_child_name = id;
            chip_bar.set_active (id);

            foreach (var tab in tabs) {
                if (tab.id != id)
                    continue;

                environment = tab.environment;
                tab.terminal.grab_focus ();
                focused (this);
                status_changed (this);
                break;
            }
        }

        private void close_tab (string id) {
            if (tabs.size == 1) {
                close_requested (this);
                return;
            }

            TerminalTab? closing = null;
            int closing_index = -1;
            for (int i = 0; i < tabs.size; i++) {
                if (tabs[i].id == id) {
                    closing = tabs[i];
                    closing_index = i;
                    break;
                }
            }

            if (closing == null)
                return;

            stop_tab (closing);
            terminal_stack.remove (closing.terminal);
            chip_bar.remove_chip (id);
            tabs.remove (closing);
            sync_tab_bar ();

            int next_index = int.min (closing_index, tabs.size - 1);
            activate_tab (tabs[next_index].id);
        }

        private void reset_tabs () {
            foreach (var tab in tabs) {
                stop_tab (tab);
                terminal_stack.remove (tab.terminal);
                chip_bar.remove_chip (tab.id);
            }

            tabs.clear ();
            tab_sequence = 0;
            add_tab (environment);
        }

        public void terminate_sessions () {
            foreach (var tab in tabs)
                stop_tab (tab);
        }

        private void stop_tab (TerminalTab tab) {
            if (tab.closing)
                return;

            tab.closing = true;
            tab.spawn_cancellable.cancel ();
            if (tab.shell_pid > 0) {
                Posix.kill ((Posix.pid_t) tab.shell_pid, Posix.Signal.TERM);
                tab.shell_pid = 0;
            }
        }

        public void update_environment_profile (Environment profile) {
            foreach (var tab in tabs) {
                if (tab.environment.id == profile.id)
                    tab.environment = profile;
            }
            if (environment.id == profile.id)
                environment = profile;
        }

        private void sync_tab_bar () {
            chip_bar.visible = tabs.size > 1;
        }
    }
}
