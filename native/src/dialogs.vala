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
            set_title (_("Creating %s").printf (distribution.name));
            set_default_size (560, 320);

            var page = new Singularity.Widgets.PreferencesPage ();
            page.margin_start = 16;
            page.margin_end = 16;
            page.margin_bottom = 16;

            var group = new Singularity.Widgets.PreferencesGroup (
                _("Environment creation"),
                _("Atoms will keep this environment and its files between sessions.")
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
                _("Preparing environment"),
                _("Waiting for the provider to start"),
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
            progress_row.title = _("Creating environment");
            progress_row.subtitle = message;
        }

        public void fail (string message) {
            spinner.spinning = false;
            progress_row.title = _("Environment creation failed");
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
        private Singularity.Widgets.SwitchRow audio_row;
        private Singularity.Widgets.SwitchRow usb_row;
        private Singularity.Widgets.SwitchRow input_row;
        private Singularity.Widgets.SwitchRow host_commands_row;

        public signal void saved (Environment profile);
        public signal void restart_requested (Environment profile);
        public signal void delete_requested (Environment profile);
        public signal void update_requested (Environment profile);
        public signal void applications_requested (Environment profile);

        public EnvironmentSettingsDialog (Gtk.Application app,
                                          Gtk.Window parent,
                                          Environment profile,
                                          GLib.Settings settings) {
            base (app, true, true);
            this.profile = profile;
            transient_for = parent;
            set_title (_("%s settings").printf (profile.name));
            set_default_size (560, 700);

            var page = new Singularity.Widgets.PreferencesPage ();
            page.margin_start = 16;
            page.margin_end = 16;
            page.margin_bottom = 8;

            var environment_group = new Singularity.Widgets.PreferencesGroup (
                _("Environment"),
                _("Configuration for this Linux environment.")
            );
            var environment_row = new Singularity.Widgets.ActionRow (
                profile.display_name (),
                profile.origin
            );
            add_environment_icon (environment_row, profile.icon_path);
            environment_group.add_row (environment_row);
            environment_group.add_row (new Singularity.Widgets.ActionRow (
                _("Terminal tabs"),
                _("Open tabs in the current instance or start an isolated instance."),
                "atoms-terminal-symbolic"
            ));
            page.append_group (environment_group);

            var access_group = new Singularity.Widgets.PreferencesGroup (
                _("Permissions"),
                _("Access is scoped to this environment and can be changed later.")
            );

            network_row = new Singularity.Widgets.SwitchRow (
                _("Network"),
                _("Allow outbound network access"),
                profile.policy.network
            );
            home_row = new Singularity.Widgets.SwitchRow (
                _("Home files"),
                _("Share selected host home paths"),
                profile.policy.home
            );
            display_row = new Singularity.Widgets.SwitchRow (
                _("Desktop display"),
                _("Allow graphical applications"),
                profile.policy.display
            );
            audio_row = new Singularity.Widgets.SwitchRow (
                _("Audio"),
                _("Allow applications to play and record audio"),
                profile.policy.audio
            );
            usb_row = new Singularity.Widgets.SwitchRow (
                _("USB devices"),
                _("Expose explicitly selected USB devices"),
                profile.policy.usb
            );
            input_row = new Singularity.Widgets.SwitchRow (
                _("Input devices"),
                _("Allow keyboard, pointer, and controller access"),
                profile.policy.input
            );
            host_commands_row = new Singularity.Widgets.SwitchRow (
                _("Host commands"),
                _("Use commands allowed by the environment provider"),
                profile.policy.host_commands
            );

            network_row.sensitive = profile.policy.can_network;
            home_row.sensitive = profile.policy.can_home;
            display_row.sensitive = profile.policy.can_display;
            audio_row.sensitive = profile.policy.can_audio;
            usb_row.sensitive = profile.policy.can_usb;
            input_row.sensitive = profile.policy.can_input;
            host_commands_row.sensitive = profile.policy.can_host_commands;

            access_group.add_row (network_row);
            access_group.add_row (home_row);
            access_group.add_row (display_row);
            access_group.add_row (audio_row);
            access_group.add_row (usb_row);
            access_group.add_row (input_row);
            access_group.add_row (host_commands_row);
            page.append_group (access_group);

            var appearance_group = new Singularity.Widgets.PreferencesGroup (
                _("Appearance"),
                _("Apply a color scheme to the terminal and the Atoms window.")
            );
            var schemes = new Singularity.Widgets.ColorSchemeRow (
                _("Color scheme"),
                Singularity.Core.TerminalThemes.get_all (),
                settings.get_string ("color-scheme")
            );
            schemes.scheme_selected.connect ((scheme) => {
                settings.set_string ("color-scheme", scheme);
            });
            appearance_group.add_row (schemes);
            page.append_group (appearance_group);

            var tools_group = new Singularity.Widgets.PreferencesGroup (
                _("Environment tools"),
                _("Update packages or expose installed applications to the desktop.")
            );
            var update = new Singularity.Widgets.ActionRow (
                _("Update environment"),
                _("Upgrade the installed packages"),
                "atoms-view-refresh-symbolic"
            );
            update.activated.connect (() => {
                update_requested (profile);
                close_dialog ();
            });
            tools_group.add_row (update);
            var applications = new Singularity.Widgets.ActionRow (
                _("Applications"),
                _("Choose applications shown in the host application menu"),
                "atoms-package-symbolic"
            );
            applications.activated.connect (() => {
                applications_requested (profile);
                close_dialog ();
            });
            tools_group.add_row (applications);
            page.append_group (tools_group);

            var lifecycle_group = new Singularity.Widgets.PreferencesGroup (
                _("Lifecycle"),
                _("Restart or remove the selected environment.")
            );

            var restart = new Singularity.Widgets.ActionRow (
                _("Restart environment"),
                _("Restart every open terminal for this environment"),
                "atoms-view-refresh-symbolic"
            );
            restart.activated.connect (() => {
                restart_requested (profile);
                close_dialog ();
            });
            lifecycle_group.add_row (restart);

            var remove = new Singularity.Widgets.ConfirmRow (
                _("Delete environment and its data"),
                _("Remove private data and saved terminal state"),
                "atoms-user-trash-symbolic"
            );
            remove.confirm_label = _("Delete");
            remove.cancel_label = _("Keep");
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
            var cancel = new Gtk.Button.with_label (_("Cancel"));
            cancel.clicked.connect (close_dialog);
            footer.append (cancel);

            var save = new Gtk.Button.with_label (_("Save changes"));
            save.add_css_class ("suggested-action");
            save.clicked.connect (save_settings);
            footer.append (save);
            content_box.append (footer);
        }

        private void save_settings () {
            profile.policy.network = network_row.active;
            profile.policy.home = home_row.active;
            profile.policy.display = display_row.active;
            profile.policy.audio = audio_row.active;
            profile.policy.usb = usb_row.active;
            profile.policy.input = input_row.active;
            profile.policy.host_commands = host_commands_row.active;
            saved (profile);
            close_dialog ();
        }
    }

    public class ApplicationExportDialog : Singularity.Widgets.AppDialog {
        private Environment profile;
        private Provider provider;
        private HashMap<string, DesktopApplication> applications;
        private HashMap<string, Singularity.Widgets.SwitchRow> rows;
        private HashMap<string, bool> initial;
        private Gtk.Label feedback;
        private Gtk.Button save;

        public signal void saved ();

        public ApplicationExportDialog (Gtk.Application app,
                                        Gtk.Window parent,
                                        Environment profile,
                                        Provider provider,
                                        ArrayList<DesktopApplication> available) {
            base (app, true, true);
            this.profile = profile;
            this.provider = provider;
            applications = new HashMap<string, DesktopApplication> ();
            rows = new HashMap<string, Singularity.Widgets.SwitchRow> ();
            initial = new HashMap<string, bool> ();
            transient_for = parent;
            set_title (_("%s applications").printf (profile.name));
            set_default_size (560, 620);

            var page = new Singularity.Widgets.PreferencesPage ();
            page.margin_start = 16;
            page.margin_end = 16;
            page.margin_bottom = 8;
            var group = new Singularity.Widgets.PreferencesGroup (
                _("Applications"),
                _("Choose which applications appear in the host application menu.")
            );
            if (available.size == 0) {
                group.add_row (new Singularity.Widgets.ActionRow (
                    _("No applications found"),
                    _("Install a graphical application in this environment first."),
                    "atoms-package-symbolic"
                ));
            } else {
                foreach (var application in available) {
                    var row = new Singularity.Widgets.SwitchRow (
                        application.name,
                        application.description,
                        application.exported
                    );
                    row.icon_name = "atoms-package-symbolic";
                    applications[application.id] = application;
                    rows[application.id] = row;
                    initial[application.id] = application.exported;
                    group.add_row (row);
                }
            }
            page.append_group (group);

            var scroll = new Gtk.ScrolledWindow ();
            scroll.hscrollbar_policy = PolicyType.NEVER;
            scroll.vexpand = true;
            scroll.set_child (page);
            content_box.append (scroll);

            feedback = new Gtk.Label ("");
            feedback.halign = Align.START;
            feedback.wrap = true;
            feedback.add_css_class ("atoms-muted");
            content_box.append (feedback);

            var footer = dialog_footer ();
            var cancel = new Gtk.Button.with_label (_("Cancel"));
            cancel.clicked.connect (close_dialog);
            footer.append (cancel);
            save = new Gtk.Button.with_label (_("Save changes"));
            save.add_css_class ("suggested-action");
            save.sensitive = available.size > 0;
            save.clicked.connect (() => save_changes.begin ());
            footer.append (save);
            content_box.append (footer);
        }

        private async void save_changes () {
            save.sensitive = false;
            feedback.label = _("Updating application menu...");
            try {
                foreach (var entry in applications.entries) {
                    bool exported = rows[entry.key].active;
                    if (exported == initial[entry.key])
                        continue;
                    yield provider.set_application_exported (
                        profile,
                        entry.value,
                        exported
                    );
                }
                saved ();
                close_dialog ();
            } catch (Error error) {
                feedback.label = _("Could not update application menu: %s").printf (
                    error.message
                );
                save.sensitive = true;
            }
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
            set_title (_("New tab"));
            set_default_size (500, 400);

            var body = new Gtk.Box (Orientation.VERTICAL, 16);
            body.add_css_class ("atoms-dialog-body");

            var identity = new Singularity.Widgets.ActionRow (
                profile.display_name (),
                profile.origin
            );
            add_environment_icon (identity, profile.icon_path);
            body.append (identity);

            var title = new Gtk.Label (_("Choose how this tab connects"));
            title.add_css_class ("title-3");
            title.halign = Align.START;
            body.append (title);

            same_instance = new Gtk.CheckButton.with_label (
                _("Use the current environment instance")
            );
            same_instance.active = true;
            body.append (same_instance);

            var new_instance = new Gtk.CheckButton.with_label (
                _("Start a new instance of the same environment")
            );
            new_instance.set_group (same_instance);
            body.append (new_instance);
            content_box.append (body);

            var footer = dialog_footer ();
            var cancel = new Gtk.Button.with_label (_("Cancel"));
            cancel.clicked.connect (close_dialog);
            footer.append (cancel);

            var create = new Gtk.Button.with_label (_("Open tab"));
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
                                Distribution[] distributions,
                                string distribution_error = "") {
            base (app, true, true);
            this.create_environment = create_environment;
            this.environments = environments;
            this.distributions = distributions;
            transient_for = parent;
            set_title (create_environment ? _("New environment") : _("New terminal"));
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
                        _("No distributions available"),
                        distribution_error == ""
                            ? _("Install or enable an Atoms provider to create an environment.")
                            : distribution_error,
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
                        _("No environments yet"),
                        _("Create an environment before opening a terminal."),
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
                _("About"),
                distribution.description,
                "atoms-information-symbolic"
            ));
            row.add_row (detail_row (
                _("Package"),
                distribution.origin,
                "atoms-package-symbolic"
            ));

            var create = new Singularity.Widgets.ActionRow (
                _("Create environment"),
                _("Install %s and open its terminal.").printf (distribution.display_name ()),
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
                _("Package"),
                profile.origin,
                "atoms-package-symbolic"
            ));

            var open = new Singularity.Widgets.ActionRow (
                _("Open terminal"),
                _("Start a terminal in this environment."),
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
            summary.append (metric ("-", _("Processes"), out process_count));
            summary.append (metric ("-", _("CPU"), out cpu_total));
            summary.append (metric ("-", _("Memory"), out memory_total));
            body.append (summary);

            process_list = new Gtk.ListBox ();
            process_list.add_css_class ("boxed-list");
            process_list.selection_mode = SelectionMode.SINGLE;
            body.append (process_list);

            var actions = new Singularity.Widgets.PreferencesGroup (
                _("Process actions"),
                _("Actions apply to the selected process.")
            );

            signal_picker = new Singularity.Widgets.SelectionRow (
                _("Signal"),
                signals,
                contains_signal (signals, "TERM") ? "TERM" : signals[0]
            );
            signal_picker.subtitle = _("Choose the event sent by the action below");
            actions.add_row (signal_picker);

            var send = new Singularity.Widgets.ActionRow (
                _("Send selected signal"),
                _("Send the selected event to the process"),
                "atoms-system-run-symbolic"
            );
            send.activated.connect (() => send_selected_signal (false));
            actions.add_row (send);

            var kill = new Singularity.Widgets.ConfirmRow (
                _("Kill process"),
                _("Immediately send SIGKILL to the process"),
                "atoms-process-stop-symbolic"
            );
            kill.confirm_label = _("Kill");
            kill.cancel_label = _("Cancel");
            kill.suggested_action = Singularity.Widgets.ConfirmationSuggestedAction.CANCEL;
            kill.confirmed.connect (() => send_selected_signal (true));
            actions.add_row (kill);
            body.append (actions);

            feedback = new Gtk.Label (_("Select a process to manage it"));
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
                feedback.label = _("Select a process first");
                return;
            }

            var process = processes[row];
            if (!process.can_signal) {
                feedback.label = _("The environment init process cannot be signalled");
                return;
            }
            string signal = kill
                ? "KILL"
                : signal_picker.current_value;
            send_signal.begin (process, signal);
        }

        private async void send_signal (ProcessInfo process, string signal) {
            feedback.label = _("Sending %s to PID %d...").printf (signal, process.pid);
            try {
                yield provider.signal_process (profile, process.pid, signal);
                var current = yield provider.list_processes (profile);
                populate (current);
                feedback.label = _("%s sent to PID %d").printf (signal, process.pid);
            } catch (Error error) {
                feedback.label = _("Could not signal PID %d: %s").printf (
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
                ? _("No processes are running")
                : _("Select a process to manage it");
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
            set_title (_("Support Atoms"));
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
            var title = new Gtk.Label (_("Keep Atoms independent"));
            title.add_css_class ("title-1");
            title.halign = Align.START;
            copy.append (title);
            var description = new Gtk.Label (
                _("Your support pays for development, infrastructure, and maintained distribution packages.")
            );
            description.wrap = true;
            description.xalign = 0;
            copy.append (description);
            hero.append (copy);
            body.append (hero);

            var channels = new Gtk.Box (Orientation.VERTICAL, 8);
            channels.add_css_class ("atoms-funding-card");
            channels.append (funding_button (
                _("GitHub Sponsors"),
                "https://github.com/sponsors/mirkobrombin"
            ));
            channels.append (funding_button (
                _("Liberapay"),
                "https://liberapay.com/mirkobrombin"
            ));
            channels.append (funding_button (
                _("Patreon"),
                "https://www.patreon.com/MirkoBrombin"
            ));
            body.append (channels);

            var note = new Gtk.Label (
                _("Even sharing Atoms or contributing a distro package helps.")
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
