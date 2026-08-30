using Gtk;
using Gee;

namespace Atoms {

    public class AtomsWindow : Singularity.Widgets.Window {
        private ArrayList<Environment> environments;
        private ArrayList<LeafPane> terminals;
        private HashMap<string, Singularity.Widgets.SidebarRow> environment_rows;
        private Singularity.Widgets.AppSidebar sidebar;
        private Gtk.Box environment_list;
        private Gtk.Box layout_host;
        private Gtk.Widget? layout_root;
        private Gtk.Label status_label;
        private Singularity.Widgets.CommandPalette palette;
        private LeafPane? active_terminal;
        private ProviderRegistry registry;
        private bool smoke_mode;

        public AtomsWindow (Gtk.Application app,
                            ProviderRegistry registry,
                            bool smoke_mode = false) {
            base (app);
            this.registry = registry;
            this.smoke_mode = smoke_mode;
            set_title ("Atoms");
            set_default_size (1280, 760);
            flat = true;
            toolbar.visible = false;

            environments = new ArrayList<Environment> ();
            terminals = new ArrayList<LeafPane> ();
            environment_rows = new HashMap<string, Singularity.Widgets.SidebarRow> ();

            build_sidebar ();
            build_workspace ();
            build_shortcuts ();
            close_request.connect (() => {
                terminate_terminal_sessions ();
                return false;
            });

            if (smoke_mode) {
                seed_environments ();
                foreach (var environment in environments)
                    append_environment_row (environment);
                add_terminal (environments[0]);
                add_terminal (environments[1]);
            } else {
                show_welcome_page ();
                update_status ("Loading environments...");
                load_environments.begin ();
            }
        }

        private void seed_environments () {
            environments.add (new Environment (
                "smoke",
                "environment-one",
                "Environment One",
                "1",
                "example.test/project/one"
            ));
            environments.add (new Environment (
                "smoke",
                "environment-two",
                "Environment Two",
                "2",
                "example.test/project/two"
            ));
            environments.add (new Environment (
                "smoke",
                "environment-three",
                "Environment Three",
                "3",
                "example.test/project/three"
            ));
        }

        private void build_sidebar () {
            sidebar = new Singularity.Widgets.AppSidebar (240);

            var brand = new Gtk.Box (Orientation.VERTICAL, 0);
            brand.add_css_class ("atoms-sidebar-brand");

            var title = new Gtk.Label ("Atoms");
            title.add_css_class ("atoms-wordmark");
            title.halign = Align.START;
            brand.append (title);

            var description = new Gtk.Label ("Linux, one shell away.");
            description.add_css_class ("atoms-sidebar-copy");
            description.halign = Align.START;
            brand.append (description);
            sidebar.box.append (brand);

            sidebar.box.append (new Singularity.Widgets.SidebarSectionLabel ("Environments"));
            environment_list = new Gtk.Box (Orientation.VERTICAL, 2);
            var create_environment = new Singularity.Widgets.SidebarRow (
                "atoms-add-symbolic",
                "New environment"
            );
            create_environment.clicked.connect (() => open_catalogue (true));
            environment_list.append (create_environment);
            sidebar.box.append (environment_list);

            var spacer = new Gtk.Box (Orientation.VERTICAL, 0);
            spacer.vexpand = true;
            sidebar.box.append (spacer);

            var support = new Gtk.Button ();
            support.add_css_class ("atoms-support-button");
            var support_content = new Gtk.Box (Orientation.HORIZONTAL, 8);
            support_content.append (new Gtk.Image.from_icon_name ("atoms-heart-symbolic"));
            support_content.append (new Gtk.Label ("Support Atoms"));
            support.set_child (support_content);
            support.clicked.connect (open_funding);
            sidebar.box.append (support);

            var version = new Gtk.Label ("Atoms 2.0");
            version.add_css_class ("atoms-version");
            version.halign = Align.START;
            sidebar.box.append (version);

            set_sidebar (sidebar);
            set_sidebar_width (240);
            set_sidebar_visible (true);
        }

        private void append_environment_row (Environment environment) {
            var row = new EnvironmentSidebarRow (environment);
            row.clicked.connect (() => assign_environment (environment));
            environment_rows[environment.id] = row;
            environment_list.append (row);
        }

        private void build_workspace () {
            var content = new Gtk.Box (Orientation.VERTICAL, 0);

            layout_host = new Gtk.Box (Orientation.VERTICAL, 0);
            layout_host.hexpand = true;
            layout_host.vexpand = true;
            layout_host.add_css_class ("atoms-workspace");
            content.append (layout_host);

            var status = new Gtk.Box (Orientation.HORIZONTAL, 8);
            status.add_css_class ("atoms-statusbar");
            status_label = new Gtk.Label ("");
            status_label.add_css_class ("atoms-muted");
            status_label.halign = Align.START;
            status_label.hexpand = true;
            status.append (status_label);
            content.append (status);

            var overlay = new Gtk.Overlay ();
            overlay.set_child (content);

            palette = new Singularity.Widgets.CommandPalette ();
            palette.close_requested.connect (close_palette);
            overlay.add_overlay (palette);
            set_content (overlay);
        }

        private void build_shortcuts () {
            var keys = new Gtk.EventControllerKey ();
            keys.set_propagation_phase (Gtk.PropagationPhase.CAPTURE);
            keys.key_pressed.connect ((keyval, keycode, state) => {
                bool ctrl = (state & Gdk.ModifierType.CONTROL_MASK) != 0;
                bool shift = (state & Gdk.ModifierType.SHIFT_MASK) != 0;
                if (!ctrl)
                    return false;

                uint key = Gdk.keyval_to_lower (keyval);
                if (ctrl && shift) {
                    if (key == Gdk.Key.n) {
                        open_catalogue (false);
                        return true;
                    }
                    if (key == Gdk.Key.t && active_terminal != null) {
                        open_tab_dialog (active_terminal);
                        return true;
                    }
                    return false;
                }

                if (key == Gdk.Key.k && active_terminal != null) {
                    open_search (active_terminal);
                    return true;
                }
                if (key == Gdk.Key.comma && active_terminal != null) {
                    open_settings (active_terminal);
                    return true;
                }
                return false;
            });
            ((Gtk.Widget) this).add_controller (keys);
        }

        private void add_terminal (Environment profile) {
            if (terminals.size >= 4) {
                status_label.label = "Four terminal areas are already open";
                return;
            }

            var terminal = new LeafPane (this, profile, registry, smoke_mode);
            terminal.focused.connect (set_active_terminal);
            terminal.new_terminal_requested.connect ((requested) => {
                set_active_terminal (requested);
                add_terminal (requested.environment);
            });
            terminal.new_tab_requested.connect ((requested) => {
                set_active_terminal (requested);
                open_tab_dialog (requested);
            });
            terminal.search_requested.connect ((requested) => {
                set_active_terminal (requested);
                open_search (requested);
            });
            terminal.process_manager_requested.connect ((requested) => {
                set_active_terminal (requested);
                open_process_manager (requested);
            });
            terminal.settings_requested.connect ((requested) => {
                set_active_terminal (requested);
                open_settings (requested);
            });
            terminal.close_requested.connect (close_terminal);
            terminal.close_all_requested.connect (() => {
                terminate_terminal_sessions ();
                close ();
            });
            terminal.move_requested.connect (move_terminal);
            terminal.status_changed.connect ((requested) => {
                if (requested == active_terminal) {
                    update_status ();
                    refresh_process_count.begin (requested);
                }
            });

            terminals.add (terminal);
            rebuild_layout ();
            set_active_terminal (terminal);
        }

        private void close_terminal (LeafPane terminal) {
            int index = terminals.index_of (terminal);
            terminal.terminate_sessions ();
            terminals.remove (terminal);
            if (terminals.size == 0) {
                active_terminal = null;
                rebuild_layout ();
                show_welcome_page ();
                update_status ("Choose an environment to open a terminal");
                return;
            }
            rebuild_layout ();
            set_active_terminal (terminals[int.min (index, terminals.size - 1)]);
        }

        private void move_terminal (string source_id,
                                    LeafPane target,
                                    TerminalDropZone zone) {
            LeafPane? source = null;
            foreach (var terminal in terminals) {
                if (terminal.pane_id == source_id) {
                    source = terminal;
                    break;
                }
            }
            if (source == null || source == target)
                return;

            int source_index = terminals.index_of (source);
            int target_index = terminals.index_of (target);
            if (zone == TerminalDropZone.CENTER) {
                terminals[source_index] = target;
                terminals[target_index] = source;
            } else {
                terminals.remove (source);
                target_index = terminals.index_of (target);
                bool before = zone == TerminalDropZone.LEFT ||
                              zone == TerminalDropZone.TOP;
                terminals.insert (target_index + (before ? 0 : 1), source);
            }

            rebuild_layout ();
            set_active_terminal (source);
        }

        private void rebuild_layout () {
            if (layout_root != null) {
                layout_host.remove (layout_root);
                release_layout (layout_root);
            }

            if (terminals.size == 0) {
                layout_root = null;
                update_status ();
                return;
            }

            switch (terminals.size) {
                case 1:
                    layout_root = terminals[0];
                    break;
                case 2:
                    layout_root = split (Orientation.HORIZONTAL, terminals[0], terminals[1]);
                    break;
                case 3:
                    var right = split (Orientation.VERTICAL, terminals[1], terminals[2]);
                    layout_root = split (Orientation.HORIZONTAL, terminals[0], right);
                    break;
                default:
                    var left = split (Orientation.VERTICAL, terminals[0], terminals[1]);
                    var right = split (Orientation.VERTICAL, terminals[2], terminals[3]);
                    layout_root = split (Orientation.HORIZONTAL, left, right);
                    break;
            }

            layout_host.append (layout_root);
            update_status ();
        }

        private void release_layout (Gtk.Widget widget) {
            var paned = widget as Gtk.Paned;
            if (paned == null)
                return;

            Gtk.Widget? start = paned.start_child;
            Gtk.Widget? end = paned.end_child;
            paned.set_start_child (null);
            paned.set_end_child (null);

            if (start != null)
                release_layout (start);
            if (end != null)
                release_layout (end);
        }

        private Gtk.Paned split (Orientation orientation,
                                 Gtk.Widget start,
                                 Gtk.Widget end) {
            var paned = new Gtk.Paned (orientation);
            paned.hexpand = true;
            paned.vexpand = true;
            paned.wide_handle = true;
            paned.set_start_child (start);
            paned.set_end_child (end);
            return paned;
        }

        private void terminate_terminal_sessions () {
            foreach (var terminal in terminals)
                terminal.terminate_sessions ();
        }

        private void set_active_terminal (LeafPane terminal) {
            active_terminal = terminal;
            foreach (var item in terminals)
                item.set_active (item == terminal);

            foreach (var entry in environment_rows.entries)
                entry.value.set_active (entry.key == terminal.environment.id);

            update_status ();
        }

        private void assign_environment (Environment profile) {
            if (active_terminal == null)
                return;

            active_terminal.switch_environment (profile);
            set_active_terminal (active_terminal);
        }

        private void open_tab_dialog (LeafPane terminal) {
            var dialog = new TabCreationDialog (
                (Gtk.Application) application,
                this,
                terminal.environment
            );
            dialog.tab_created.connect ((new_instance) => {
                if (new_instance)
                    create_additional_instance (terminal);
                else {
                    terminal.add_tab (terminal.environment);
                    set_active_terminal (terminal);
                }
            });
            dialog.open_dialog ();
        }

        private void open_catalogue (bool create_environment) {
            open_catalogue_async.begin (create_environment);
        }

        private async void open_catalogue_async (bool create_environment) {
            var available_environments = new Environment[environments.size];
            for (int i = 0; i < environments.size; i++)
                available_environments[i] = environments[i];

            var available_distributions = new ArrayList<Distribution> ();
            if (create_environment) {
                update_status ("Loading available distributions...");
                foreach (var provider in registry.providers) {
                    if (!provider.available)
                        continue;
                    try {
                        var distributions = yield provider.list_distributions ();
                        available_distributions.add_all (distributions);
                    } catch (Error error) {
                        warning ("Could not load %s distributions: %s", provider.id, error.message);
                    }
                }
            }
            var distribution_array = new Distribution[available_distributions.size];
            for (int i = 0; i < available_distributions.size; i++)
                distribution_array[i] = available_distributions[i];

            var dialog = new CatalogueDialog (
                (Gtk.Application) application,
                this,
                create_environment,
                available_environments,
                distribution_array
            );
            dialog.terminal_requested.connect ((profile) => {
                add_terminal (profile);
            });
            dialog.distribution_requested.connect ((distribution) => {
                create_distribution.begin (distribution);
            });
            dialog.open_dialog ();
            update_status ();
        }

        private void open_search (LeafPane terminal) {
            var items = new ArrayList<Singularity.Widgets.CommandPaletteItem> ();
            items.add (new Singularity.Widgets.CommandPaletteItem (
                    "atoms-terminal-symbolic",
                    "New Terminal",
                    "Atoms command",
                    "Ctrl+Shift+N",
                    "Result",
                    () => add_terminal (terminal.environment)
                ));
            items.add (new Singularity.Widgets.CommandPaletteItem (
                    "atoms-tab-new-symbolic",
                    "New Tab",
                    "Atoms command",
                    "Ctrl+Shift+T",
                    "Result",
                    () => open_tab_dialog (terminal)
                ));
            items.add (new Singularity.Widgets.CommandPaletteItem (
                    "atoms-process-monitor-symbolic",
                    "Environment Processes",
                    "Atoms command",
                    null,
                    "Result",
                    () => open_process_manager (terminal)
                ));
            items.add (new Singularity.Widgets.CommandPaletteItem (
                    "emblem-system-symbolic",
                    "Environment Settings",
                    "Atoms command",
                    "Ctrl+,",
                    "Result",
                    () => open_settings (terminal)
                ));
            items.add (new Singularity.Widgets.CommandPaletteItem (
                    "list-add-symbolic",
                    "New Environment",
                    "Atoms command",
                    null,
                    "Result",
                    () => open_catalogue (true)
                ));
            foreach (var command in terminal.active_history ())
                items.add (history_item (terminal, command));

            var palette_items = new Singularity.Widgets.CommandPaletteItem[items.size];
            for (int i = 0; i < items.size; i++)
                palette_items[i] = items[i];
            palette.set_items (palette_items);
            palette.open ();
        }

        private Singularity.Widgets.CommandPaletteItem history_item (
            LeafPane terminal,
            string command
        ) {
            return new Singularity.Widgets.CommandPaletteItem (
                "atoms-terminal-symbolic",
                command,
                "Terminal history",
                null,
                "Result",
                () => terminal.insert_history_command (command)
            );
        }

        private void close_palette () {
            palette.close ();
            active_terminal?.active_tab ()?.terminal.grab_focus ();
        }

        private void open_process_manager (LeafPane terminal) {
            open_process_manager_async.begin (terminal);
        }

        private async void open_process_manager_async (LeafPane terminal) {
            update_status ("Loading %s processes...".printf (terminal.environment.name));
            try {
                var provider = registry.require (terminal.environment.provider_id);
                var processes = yield provider.list_processes (terminal.environment);
                string[] signals = yield provider.list_signals ();
                if (signals.length == 0)
                    throw new CoreError.INVALID_DATA ("provider returned no process signals");
                var dialog = new ProcessManagerDialog (
                    (Gtk.Application) application,
                    this,
                    terminal.environment,
                    provider,
                    processes,
                    signals
                );
                dialog.open_dialog ();
                update_status ();
            } catch (Error error) {
                update_status ("Could not open process manager: %s".printf (error.message));
            }
        }

        private void open_settings (LeafPane terminal) {
            var dialog = new EnvironmentSettingsDialog (
                (Gtk.Application) application,
                this,
                terminal.environment
            );
            dialog.saved.connect ((profile) => {
                save_policy.begin (profile);
            });
            dialog.restart_requested.connect ((profile) => {
                restart_environment (profile);
            });
            dialog.delete_requested.connect ((profile) => {
                delete_environment (profile);
            });
            dialog.open_dialog ();
        }

        private void restart_environment (Environment profile) {
            restart_environment_async.begin (profile);
        }

        private void delete_environment (Environment profile) {
            delete_environment_async.begin (profile);
        }

        private void remove_environment_from_ui (Environment profile) {

            var removing = new ArrayList<LeafPane> ();
            foreach (var terminal in terminals) {
                if (terminal.environment.id == profile.id)
                    removing.add (terminal);
            }
            foreach (var terminal in removing) {
                terminal.terminate_sessions ();
                terminals.remove (terminal);
            }

            var row = environment_rows[profile.id];
            if (row != null)
                environment_list.remove (row);
            environment_rows.unset (profile.id);
            environments.remove (profile);

            if (terminals.size == 0) {
                if (layout_root != null) {
                    layout_host.remove (layout_root);
                    release_layout (layout_root);
                }
                layout_root = null;
                active_terminal = null;
                show_welcome_page ();
                update_status (
                    environments.size == 0
                        ? "Create a distribution environment to begin"
                        : "Choose an environment to open a terminal"
                );
            } else {
                rebuild_layout ();
                set_active_terminal (terminals[0]);
            }
        }

        private async void load_environments () {
            foreach (var provider in registry.providers) {
                if (!provider.available)
                    continue;
                try {
                    var loaded = yield provider.list_environments ();
                    foreach (var environment in loaded) {
                        environments.add (environment);
                        append_environment_row (environment);
                    }
                } catch (Error error) {
                    warning ("Could not load %s environments: %s", provider.id, error.message);
                }
            }

            if (environments.size == 0) {
                show_welcome_page ();
                update_status (
                    registry.providers.size == 0
                        ? "No Atoms provider is installed"
                        : "Create a distribution environment to begin"
                );
                return;
            }

            add_terminal (environments[0]);
        }

        private async void create_distribution (Distribution distribution,
                                                LeafPane? target = null) {
            var pending = new PendingEnvironmentSidebarRow (distribution);
            environment_list.append (pending);
            var dialog = new EnvironmentCreationDialog (
                (Gtk.Application) application,
                this,
                distribution
            );
            dialog.open_dialog ();
            update_status ("Installing %s...".printf (distribution.display_name ()));
            Provider? provider = null;
            ulong progress_handler = 0;
            try {
                string name = unique_environment_name (distribution.name);
                provider = registry.require (distribution.provider_id);
                progress_handler = provider.operation_progress.connect ((message) => {
                    dialog.set_phase (message);
                    update_status (message);
                });
                var profile = yield provider.create_environment (distribution, name);
                if (progress_handler != 0)
                    provider.disconnect (progress_handler);
                environment_list.remove (pending);
                environments.add (profile);
                append_environment_row (profile);
                dialog.close_dialog ();
                if (target == null)
                    add_terminal (profile);
                else {
                    target.add_tab (profile);
                    set_active_terminal (target);
                }
                update_status ("%s is ready".printf (profile.display_name ()));
            } catch (Error error) {
                if (provider != null && progress_handler != 0)
                    provider.disconnect (progress_handler);
                environment_list.remove (pending);
                dialog.fail (error.message);
                update_status ("Could not create %s: %s".printf (
                    distribution.name,
                    error.message
                ));
            }
        }

        private void create_additional_instance (LeafPane terminal) {
            var source = terminal.environment;
            var distribution = new Distribution (
                source.provider_id,
                source.origin,
                source.name,
                source.version,
                "",
                source.origin,
                source.icon_path
            );
            create_distribution.begin (distribution, terminal);
        }

        private async void save_policy (Environment profile) {
            update_status ("Saving %s permissions...".printf (profile.name));
            try {
                var provider = registry.require (profile.provider_id);
                var updated = yield provider.update_policy (profile);
                int index = environments.index_of (profile);
                if (index >= 0)
                    environments[index] = updated;
                foreach (var terminal in terminals)
                    terminal.update_environment_profile (updated);
                update_status ("Permissions saved for %s".printf (updated.name));
            } catch (Error error) {
                update_status ("Could not save permissions: %s".printf (error.message));
            }
        }

        private async void restart_environment_async (Environment profile) {
            update_status ("Restarting %s...".printf (profile.name));
            try {
                var provider = registry.require (profile.provider_id);
                yield provider.stop_environment (profile);
                foreach (var terminal in terminals) {
                    if (terminal.environment.id == profile.id)
                        terminal.restart ();
                }
                update_status ("%s restarted".printf (profile.name));
            } catch (Error error) {
                update_status ("Could not restart %s: %s".printf (
                    profile.name,
                    error.message
                ));
            }
        }

        private async void delete_environment_async (Environment profile) {
            update_status ("Deleting %s...".printf (profile.name));
            try {
                var provider = registry.require (profile.provider_id);
                yield provider.delete_environment (profile);
                remove_environment_from_ui (profile);
                update_status ("%s deleted".printf (profile.name));
            } catch (Error error) {
                update_status ("Could not delete %s: %s".printf (
                    profile.name,
                    error.message
                ));
            }
        }

        private async void refresh_process_count (LeafPane terminal,
                                                  int retries = 2) {
            var tab = terminal.active_tab ();
            if (tab == null)
                return;

            try {
                var provider = registry.require (tab.environment.provider_id);
                var current = yield provider.list_processes (tab.environment);
                int count = 0;
                foreach (var process in current) {
                    if (process.can_signal)
                        count++;
                }
                tab.background_processes = count;
                if (terminal == active_terminal)
                    update_status ();
            } catch (Error error) {
                if (retries == 0 && terminal == active_terminal)
                    status_label.label = "%s  |  process data unavailable".printf (
                        tab.environment.display_name ()
                    );
            }
            if (retries > 0) {
                Timeout.add_seconds (1, () => {
                    refresh_process_count.begin (terminal, retries - 1);
                    return Source.REMOVE;
                });
            }
        }

        private string unique_environment_name (string base_name) {
            string candidate = base_name;
            int sequence = 2;
            while (environment_name_exists (candidate)) {
                candidate = "%s %d".printf (base_name, sequence);
                sequence++;
            }
            return candidate;
        }

        private bool environment_name_exists (string name) {
            foreach (var environment in environments) {
                if (environment.name == name)
                    return true;
            }
            return false;
        }

        private void show_welcome_page () {
            if (layout_root != null) {
                layout_host.remove (layout_root);
                release_layout (layout_root);
            }

            var welcome = new Singularity.Widgets.WelcomePage ();
            welcome.app_icon_name = "pm.mirko.Atoms-symbolic";
            welcome.title = "Atoms";
            welcome.subtitle = "Linux, one shell away.";
            if (environments.size > 0) {
                welcome.add_action (
                    "atoms-terminal-symbolic",
                    "New Terminal",
                    "Open a shell in an installed environment.",
                    () => open_catalogue (false)
                );
            }
            welcome.add_action (
                "list-add-symbolic",
                "New Environment",
                "Install a Linux distribution and create its environment.",
                () => open_catalogue (true)
            );

            var welcome_controls = Singularity.Widgets.HoverControls.with_window_bubbles (
                this
            );
            welcome_controls.set_content (welcome);
            layout_root = welcome_controls;
            layout_host.append (layout_root);
        }

        private void open_funding () {
            var dialog = new FundingDialog ((Gtk.Application) application, this);
            dialog.open_dialog ();
        }

        private void update_status (string? message = null) {
            if (message != null) {
                status_label.label = message;
                return;
            }

            if (active_terminal == null) {
                status_label.label = "No active terminal";
                return;
            }

            int count = active_terminal.background_process_count;
            status_label.label = "%d background %s  |  %s".printf (
                count,
                count == 1 ? "process" : "processes",
                active_terminal.environment.display_name ()
            );
        }

        public bool run_smoke_test () {
            bool passed = true;
            Gdk.RGBA sidebar_foreground = sidebar.get_color ();
            bool dark_sidebar = sidebar_foreground.red > 0.5f
                && sidebar_foreground.green > 0.5f
                && sidebar_foreground.blue > 0.5f;
            passed = smoke_expect (
                dark_sidebar,
                "application dark theme"
            ) && passed;
            passed = smoke_expect (!toolbar.visible, "window toolbar hidden") && passed;
            passed = smoke_expect (terminals.size == 2, "initial tiled terminals") && passed;
            passed = smoke_expect (active_terminal != null, "active terminal selection") && passed;

            if (active_terminal != null) {
                passed = smoke_expect (active_terminal.tab_count == 1, "initial terminal tab") && passed;
                passed = smoke_expect (!active_terminal.tab_bar_visible, "single tab bar hidden") && passed;
                active_terminal.add_tab (active_terminal.environment);
                passed = smoke_expect (active_terminal.tab_count == 2, "terminal tab creation") && passed;
                passed = smoke_expect (active_terminal.tab_bar_visible, "multiple tab bar visible") && passed;
                active_terminal.add_history_for_test ("printf atoms-history");
                passed = smoke_expect (
                    active_terminal.active_history ().contains ("printf atoms-history"),
                    "active terminal history"
                ) && passed;
            }

            add_terminal (environments[2]);
            passed = smoke_expect (terminals.size == 3, "third tiled terminal") && passed;

            if (active_terminal != null) {
                passed = smoke_expect (
                    active_terminal.environment.id == "environment-three",
                    "terminal environment selection"
                ) && passed;

                var added_terminal = active_terminal;
                close_terminal (added_terminal);
                passed = smoke_expect (terminals.size == 2, "terminal close and layout rebuild") && passed;
            }

            while (terminals.size > 0)
                close_terminal (terminals[0]);
            passed = smoke_expect (
                layout_root is Singularity.Widgets.HoverControls,
                "welcome page window controls"
            ) && passed;

            if (passed)
                stdout.printf ("Atoms native smoke test: PASS\n");

            return passed;
        }

        private bool smoke_expect (bool condition, string operation) {
            if (condition)
                return true;

            stderr.printf ("Atoms native smoke test failed: %s\n", operation);
            return false;
        }
    }
}
