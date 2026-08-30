using Gtk;
using Gee;

namespace Atoms {

    public class EnvironmentCreationDialog : Singularity.Widgets.AppDialog {
        private Singularity.Widgets.ActionRow progress_row;
        private Gtk.Spinner spinner;

        public EnvironmentCreationDialog (Gtk.Application app,
                                          Gtk.Window parent,
                                          Distribution distribution) {
            base (app, true, false);
            transient_for = parent;
            set_title ("Creating %s".printf (distribution.name));
            set_default_size (560, 320);

            var page = new Singularity.Widgets.PreferencesPage ();
            page.margin_start = 16;
            page.margin_end = 16;
            page.margin_bottom = 16;

            var group = new Singularity.Widgets.PreferencesGroup (
                "Environment creation",
                "Atoms will keep this environment and its files between sessions."
            );
            var identity = new Singularity.Widgets.ActionRow (
                distribution.display_name (),
                distribution.origin
            );
            add_environment_icon (
                identity,
                distribution.icon_path,
                "atoms-package-symbolic"
            );
            identity.activatable = false;
            group.add_row (identity);

            progress_row = new Singularity.Widgets.ActionRow (
                "Preparing environment",
                "Waiting for the provider to start",
                "atoms-system-run-symbolic"
            );
            progress_row.activatable = false;
            spinner = new Gtk.Spinner ();
            spinner.spinning = true;
            progress_row.add_suffix (spinner);
            group.add_row (progress_row);
            page.append_group (group);
            content_box.append (page);
        }

        public void set_phase (string message) {
            progress_row.title = "Creating environment";
            progress_row.subtitle = message;
        }

        public void fail (string message) {
            spinner.spinning = false;
            progress_row.title = "Environment creation failed";
            progress_row.subtitle = message;
            progress_row.icon_name = "dialog-error-symbolic";
            closable = true;
        }
    }

    public class EnvironmentSettingsDialog : Singularity.Widgets.AppDialog {
        private Environment profile;
        private Singularity.Widgets.SwitchRow network_row;
        private Singularity.Widgets.SwitchRow home_row;
        private Singularity.Widgets.SwitchRow display_row;
        private Singularity.Widgets.SwitchRow usb_row;
        private Singularity.Widgets.SwitchRow input_row;
        private Singularity.Widgets.SwitchRow host_commands_row;

        public signal void saved (Environment profile);
        public signal void restart_requested (Environment profile);
        public signal void delete_requested (Environment profile);

        public EnvironmentSettingsDialog (Gtk.Application app,
                                          Gtk.Window parent,
                                          Environment profile) {
            base (app, true, true);
            this.profile = profile;
            transient_for = parent;
            set_title ("%s settings".printf (profile.name));
            set_default_size (560, 700);

            var page = new Singularity.Widgets.PreferencesPage ();
            page.margin_start = 16;
            page.margin_end = 16;
            page.margin_bottom = 8;

            var environment_group = new Singularity.Widgets.PreferencesGroup (
                "Environment",
                "Configuration for this Linux environment."
            );
            var environment_row = new Singularity.Widgets.ActionRow (
                profile.display_name (),
                profile.origin
            );
            add_environment_icon (environment_row, profile.icon_path);
            environment_group.add_row (environment_row);
            environment_group.add_row (new Singularity.Widgets.ActionRow (
                "Terminal tabs",
                "Open tabs in the current instance or start an isolated instance.",
                "atoms-terminal-symbolic"
            ));
            page.append_group (environment_group);

            var access_group = new Singularity.Widgets.PreferencesGroup (
                "Permissions",
                "Access is scoped to this environment and can be changed later."
            );

            network_row = new Singularity.Widgets.SwitchRow (
                "Network",
                "Allow outbound network access",
                profile.policy.network
            );
            home_row = new Singularity.Widgets.SwitchRow (
                "Home files",
                "Share selected host home paths",
                profile.policy.home
            );
            display_row = new Singularity.Widgets.SwitchRow (
                "Desktop display",
                "Allow graphical applications",
                profile.policy.display
            );
            usb_row = new Singularity.Widgets.SwitchRow (
                "USB devices",
                "Expose explicitly selected USB devices",
                profile.policy.usb
            );
            input_row = new Singularity.Widgets.SwitchRow (
                "Input devices",
                "Allow keyboard, pointer, and controller access",
                profile.policy.input
            );
            host_commands_row = new Singularity.Widgets.SwitchRow (
                "Host commands",
                "Use commands allowed by the environment provider",
                profile.policy.host_commands
            );

            network_row.sensitive = profile.policy.can_network;
            home_row.sensitive = profile.policy.can_home;
            display_row.sensitive = profile.policy.can_display;
            usb_row.sensitive = profile.policy.can_usb;
            input_row.sensitive = profile.policy.can_input;
            host_commands_row.sensitive = profile.policy.can_host_commands;

            access_group.add_row (network_row);
            access_group.add_row (home_row);
            access_group.add_row (display_row);
            access_group.add_row (usb_row);
            access_group.add_row (input_row);
            access_group.add_row (host_commands_row);
            page.append_group (access_group);

            var lifecycle_group = new Singularity.Widgets.PreferencesGroup (
                "Lifecycle",
                "Restart or remove the selected environment."
            );

            var restart = new Singularity.Widgets.ActionRow (
                "Restart environment",
                "Restart every open terminal for this environment",
                "atoms-view-refresh-symbolic"
            );
            restart.activated.connect (() => {
                restart_requested (profile);
                close_dialog ();
            });
            lifecycle_group.add_row (restart);

            var remove = new Singularity.Widgets.ConfirmRow (
                "Delete environment and its data",
                "Remove private data and saved terminal state",
                "atoms-user-trash-symbolic"
            );
            remove.confirm_label = "Delete";
            remove.cancel_label = "Keep";
            remove.suggested_action = Singularity.Widgets.ConfirmationSuggestedAction.CANCEL;
            remove.confirmed.connect (() => {
                delete_requested (profile);
                close_dialog ();
            });
            lifecycle_group.add_row (remove);
            page.append_group (lifecycle_group);

            var scroll = new Gtk.ScrolledWindow ();
            scroll.hscrollbar_policy = PolicyType.NEVER;
            scroll.vexpand = true;
            scroll.set_child (page);
            content_box.append (scroll);

            var footer = dialog_footer ();
            var cancel = new Gtk.Button.with_label ("Cancel");
            cancel.clicked.connect (close_dialog);
            footer.append (cancel);

            var save = new Gtk.Button.with_label ("Save changes");
            save.add_css_class ("suggested-action");
            save.clicked.connect (save_settings);
            footer.append (save);
            content_box.append (footer);
        }

        private void save_settings () {
            profile.policy.network = network_row.active;
            profile.policy.home = home_row.active;
            profile.policy.display = display_row.active;
            profile.policy.usb = usb_row.active;
            profile.policy.input = input_row.active;
            profile.policy.host_commands = host_commands_row.active;
            saved (profile);
            close_dialog ();
        }
    }

    public class TabCreationDialog : Singularity.Widgets.AppDialog {
        private Gtk.CheckButton same_instance;

        public signal void tab_created (bool new_instance);

        public TabCreationDialog (Gtk.Application app,
                                  Gtk.Window parent,
                                  Environment profile) {
            base (app, true, true);
            transient_for = parent;
            set_title ("New tab");
            set_default_size (500, 400);

            var body = new Gtk.Box (Orientation.VERTICAL, 16);
            body.add_css_class ("atoms-dialog-body");

            var identity = new Singularity.Widgets.ActionRow (
                profile.display_name (),
                profile.origin
            );
            add_environment_icon (identity, profile.icon_path);
            body.append (identity);

            var title = new Gtk.Label ("Choose how this tab connects");
            title.add_css_class ("title-3");
            title.halign = Align.START;
            body.append (title);

            same_instance = new Gtk.CheckButton.with_label (
                "Use the current environment instance"
            );
            same_instance.active = true;
            body.append (same_instance);

            var new_instance = new Gtk.CheckButton.with_label (
                "Start a new instance of the same environment"
            );
            new_instance.set_group (same_instance);
            body.append (new_instance);
            content_box.append (body);

            var footer = dialog_footer ();
            var cancel = new Gtk.Button.with_label ("Cancel");
            cancel.clicked.connect (close_dialog);
            footer.append (cancel);

            var create = new Gtk.Button.with_label ("Open tab");
            create.add_css_class ("suggested-action");
            create.clicked.connect (() => {
                tab_created (!same_instance.active);
                close_dialog ();
            });
            footer.append (create);
            content_box.append (footer);
        }
    }

    public class CatalogueDialog : Singularity.Widgets.AppDialog {
        private Environment[] environments;
        private Distribution[] distributions;
        private bool create_environment;
        private Gtk.Widget? initial_focus;

        public signal void terminal_requested (Environment profile);
        public signal void distribution_requested (Distribution distribution);

        public CatalogueDialog (Gtk.Application app,
                                Gtk.Window parent,
                                bool create_environment,
                                Environment[] environments,
                                Distribution[] distributions) {
            base (app, true, true);
            this.create_environment = create_environment;
            this.environments = environments;
            this.distributions = distributions;
            transient_for = parent;
            set_title (create_environment ? "New environment" : "New terminal");
            set_default_size (700, 600);

            var page = new Singularity.Widgets.PreferencesPage ();
            var group = new Singularity.Widgets.PreferencesGroup ();

            if (create_environment) {
                bool first = true;
                foreach (var distribution in distributions) {
                    var row = distribution_row (distribution, first);
                    if (first)
                        initial_focus = row;
                    group.add_row (row);
                    first = false;
                }
                if (distributions.length == 0) {
                    var empty = new Singularity.Widgets.ActionRow (
                        "No distributions available",
                        "Install or enable an Atoms provider to create an environment.",
                        "atoms-package-symbolic"
                    );
                    empty.activatable = false;
                    group.add_row (empty);
                }
            } else {
                bool first = true;
                foreach (var profile in environments) {
                    var row = environment_row (profile, first);
                    if (first)
                        initial_focus = row;
                    group.add_row (row);
                    first = false;
                }
                if (environments.length == 0) {
                    var empty = new Singularity.Widgets.ActionRow (
                        "No environments yet",
                        "Create an environment before opening a terminal.",
                        "atoms-terminal-symbolic"
                    );
                    empty.activatable = false;
                    group.add_row (empty);
                }
            }
            page.append_group (group);

            var scroll = new Gtk.ScrolledWindow ();
            scroll.hscrollbar_policy = Gtk.PolicyType.NEVER;
            scroll.vexpand = true;
            scroll.set_child (page);
            content_box.append (scroll);
        }

        public override void open_dialog () {
            base.open_dialog ();
            initial_focus?.grab_focus ();
        }

        private Singularity.Widgets.ExpanderRow distribution_row (
            Distribution distribution,
            bool expanded
        ) {
            var row = new Singularity.Widgets.ExpanderRow (
                distribution.name,
                distribution.version
            );
            add_environment_icon (row, distribution.icon_path, "atoms-package-symbolic");
            row.expanded = expanded;
            row.add_row (detail_row (
                "About",
                distribution.description,
                "atoms-information-symbolic"
            ));
            row.add_row (detail_row (
                "Package",
                distribution.origin,
                "atoms-package-symbolic"
            ));

            var create = new Singularity.Widgets.ActionRow (
                "Create environment",
                "Install %s and open its terminal.".printf (distribution.display_name ()),
                "atoms-add-symbolic"
            );
            create.add_suffix (new Gtk.Image.from_icon_name ("atoms-go-next-symbolic"));
            create.activated.connect (() => {
                distribution_requested (distribution);
                close ();
            });
            row.add_row (create);
            return row;
        }

        private Singularity.Widgets.ExpanderRow environment_row (
            Environment profile,
            bool expanded
        ) {
            var row = new Singularity.Widgets.ExpanderRow (
                profile.name,
                profile.version
            );
            add_environment_icon (row, profile.icon_path);
            row.expanded = expanded;
            row.add_row (detail_row (
                "Package",
                profile.origin,
                "atoms-package-symbolic"
            ));

            var open = new Singularity.Widgets.ActionRow (
                "Open terminal",
                "Start a terminal in this environment.",
                "atoms-terminal-symbolic"
            );
            open.add_suffix (new Gtk.Image.from_icon_name ("atoms-go-next-symbolic"));
            open.activated.connect (() => {
                terminal_requested (profile);
                close ();
            });
            row.add_row (open);
            return row;
        }

        private Singularity.Widgets.ActionRow detail_row (
            string title,
            string subtitle,
            string icon_name
        ) {
            var row = new Singularity.Widgets.ActionRow (title, subtitle, icon_name);
            row.activatable = false;
            return row;
        }
    }

    public class ProcessManagerDialog : Singularity.Widgets.AppDialog {
        private Gtk.ListBox process_list;
        private Singularity.Widgets.SelectionRow signal_picker;
        private Gtk.Label feedback;
        private Gtk.Label process_count;
        private Gtk.Label cpu_total;
        private Gtk.Label memory_total;
        private HashMap<Gtk.ListBoxRow, ProcessInfo> processes;
        private Provider provider;
        private Environment profile;

        public ProcessManagerDialog (Gtk.Application app,
                                     Gtk.Window parent,
                                     Environment profile,
                                     Provider provider,
                                     ArrayList<ProcessInfo> initial_processes,
                                     string[] signals) {
            base (app, true, true);
            this.profile = profile;
            this.provider = provider;
            transient_for = parent;
            set_title ("%s processes".printf (profile.name));
            set_default_size (720, 560);
            processes = new HashMap<Gtk.ListBoxRow, ProcessInfo> ();

            var body = new Gtk.Box (Orientation.VERTICAL, 12);
            body.add_css_class ("atoms-dialog-body");

            var summary = new Gtk.Box (Orientation.HORIZONTAL, 8);
            summary.append (metric ("-", "Processes", out process_count));
            summary.append (metric ("-", "CPU", out cpu_total));
            summary.append (metric ("-", "Memory", out memory_total));
            body.append (summary);

            process_list = new Gtk.ListBox ();
            process_list.add_css_class ("boxed-list");
            process_list.selection_mode = SelectionMode.SINGLE;
            body.append (process_list);

            var actions = new Singularity.Widgets.PreferencesGroup (
                "Process actions",
                "Actions apply to the selected process."
            );

            signal_picker = new Singularity.Widgets.SelectionRow (
                "Signal",
                signals,
                contains_signal (signals, "TERM") ? "TERM" : signals[0]
            );
            signal_picker.subtitle = "Choose the event sent by the action below";
            actions.add_row (signal_picker);

            var send = new Singularity.Widgets.ActionRow (
                "Send selected signal",
                "Send the selected event to the process",
                "atoms-system-run-symbolic"
            );
            send.activated.connect (() => send_selected_signal (false));
            actions.add_row (send);

            var kill = new Singularity.Widgets.ConfirmRow (
                "Kill process",
                "Immediately send SIGKILL to the process",
                "atoms-process-stop-symbolic"
            );
            kill.confirm_label = "Kill";
            kill.cancel_label = "Cancel";
            kill.suggested_action = Singularity.Widgets.ConfirmationSuggestedAction.CANCEL;
            kill.confirmed.connect (() => send_selected_signal (true));
            actions.add_row (kill);
            body.append (actions);

            feedback = new Gtk.Label ("Select a process to manage it");
            feedback.add_css_class ("atoms-muted");
            feedback.halign = Align.START;
            body.append (feedback);

            var scroll = new Gtk.ScrolledWindow ();
            scroll.hscrollbar_policy = Gtk.PolicyType.NEVER;
            scroll.vexpand = true;
            scroll.set_child (body);
            content_box.append (scroll);
            populate (initial_processes);
        }

        private Gtk.Widget metric (string value,
                                   string label,
                                   out Gtk.Label value_label) {
            var box = new Gtk.Box (Orientation.VERTICAL, 2);
            box.add_css_class ("atoms-process-metric");
            box.hexpand = true;

            value_label = new Gtk.Label (value);
            value_label.add_css_class ("title-2");
            box.append (value_label);

            var name_label = new Gtk.Label (label);
            name_label.add_css_class ("atoms-muted");
            box.append (name_label);
            return box;
        }

        private void append_process (ProcessInfo process) {
            var row = new Gtk.ListBoxRow ();
            var content = new Gtk.Box (Orientation.HORIZONTAL, 12);
            content.add_css_class ("atoms-process-row");

            var pid = new Gtk.Label (process.pid.to_string ());
            pid.add_css_class ("monospace");
            pid.width_chars = 6;
            pid.halign = Align.START;
            content.append (pid);

            var command = new Gtk.Label (process.command);
            command.add_css_class ("monospace");
            command.hexpand = true;
            command.halign = Align.START;
            command.ellipsize = Pango.EllipsizeMode.END;
            content.append (command);

            var cpu = new Gtk.Label (process.cpu_label ());
            cpu.width_chars = 7;
            content.append (cpu);

            var memory = new Gtk.Label (process.memory_label ());
            memory.width_chars = 9;
            content.append (memory);

            row.set_child (content);
            process_list.append (row);
            processes[row] = process;
        }

        private void send_selected_signal (bool kill) {
            var row = process_list.get_selected_row ();
            if (row == null) {
                feedback.label = "Select a process first";
                return;
            }

            var process = processes[row];
            if (!process.can_signal) {
                feedback.label = "The environment init process cannot be signalled";
                return;
            }
            string signal = kill
                ? "KILL"
                : signal_picker.current_value;
            send_signal.begin (process, signal);
        }

        private async void send_signal (ProcessInfo process, string signal) {
            feedback.label = "Sending %s to PID %d...".printf (signal, process.pid);
            try {
                yield provider.signal_process (profile, process.pid, signal);
                var current = yield provider.list_processes (profile);
                populate (current);
                feedback.label = "%s sent to PID %d".printf (signal, process.pid);
            } catch (Error error) {
                feedback.label = "Could not signal PID %d: %s".printf (
                    process.pid,
                    error.message
                );
            }
        }

        private void populate (ArrayList<ProcessInfo> current) {
            Gtk.Widget? child;
            while ((child = process_list.get_first_child ()) != null)
                process_list.remove (child);
            processes.clear ();

            double cpu = 0;
            uint64 memory = 0;
            foreach (var process in current) {
                append_process (process);
                cpu += process.cpu_percent;
                memory += process.memory_bytes;
            }
            process_count.label = current.size.to_string ();
            cpu_total.label = "%.1f%%".printf (cpu);
            memory_total.label = new ProcessInfo (0, "", 0, memory).memory_label ();
            feedback.label = current.size == 0
                ? "No processes are running"
                : "Select a process to manage it";
        }

        private bool contains_signal (string[] signals, string expected) {
            foreach (var signal in signals) {
                if (signal == expected)
                    return true;
            }
            return false;
        }

    }

    public class FundingDialog : Singularity.Widgets.AppDialog {
        public FundingDialog (Gtk.Application app, Gtk.Window parent) {
            base (app, true, true);
            transient_for = parent;
            set_title ("Support Atoms");
            set_default_size (620, 560);

            var body = new Gtk.Box (Orientation.VERTICAL, 18);
            body.add_css_class ("atoms-dialog-body");

            var hero = new Gtk.Box (Orientation.HORIZONTAL, 18);
            var heart = new Gtk.Image.from_icon_name ("atoms-heart-symbolic");
            heart.pixel_size = 64;
            heart.add_css_class ("atoms-donate-heart");
            hero.append (heart);

            var copy = new Gtk.Box (Orientation.VERTICAL, 4);
            copy.hexpand = true;
            copy.valign = Align.CENTER;
            var title = new Gtk.Label ("Keep Atoms independent");
            title.add_css_class ("title-1");
            title.halign = Align.START;
            copy.append (title);
            var description = new Gtk.Label (
                "Your support pays for development, infrastructure, and maintained distribution packages."
            );
            description.wrap = true;
            description.xalign = 0;
            copy.append (description);
            hero.append (copy);
            body.append (hero);

            var channels = new Gtk.Box (Orientation.VERTICAL, 8);
            channels.add_css_class ("atoms-funding-card");
            channels.append (funding_button (
                "GitHub Sponsors",
                "https://github.com/sponsors/mirkobrombin"
            ));
            channels.append (funding_button (
                "Liberapay",
                "https://liberapay.com/mirkobrombin"
            ));
            channels.append (funding_button (
                "Patreon",
                "https://www.patreon.com/MirkoBrombin"
            ));
            body.append (channels);

            var note = new Gtk.Label (
                "Even sharing Atoms or contributing a distro package helps."
            );
            note.add_css_class ("atoms-muted");
            note.wrap = true;
            body.append (note);
            content_box.append (body);
        }

        private Gtk.Button funding_button (string label, string uri) {
            var button = new Gtk.Button.with_label (label);
            button.add_css_class ("atoms-funding-button");
            button.clicked.connect (() => Gtk.show_uri (this, uri, Gdk.CURRENT_TIME));
            return button;
        }
    }

    private Gtk.Box dialog_footer () {
        var footer = new Gtk.Box (Orientation.HORIZONTAL, 8);
        footer.add_css_class ("atoms-dialog-footer");
        var spacer = new Gtk.Box (Orientation.HORIZONTAL, 0);
        spacer.hexpand = true;
        footer.append (spacer);
        return footer;
    }
}
