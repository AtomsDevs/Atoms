using Gee;

namespace Atoms {

    public class TerminalTab : Object {
        public string id { get; construct; }
        public string label { get; set; }
        public Vte.Terminal terminal { get; construct; }
        public Environment environment { get; set; }
        public string[]? argv_override { get; construct; }
        public int shell_pid { get; set; default = 0; }
        public int background_processes { get; set; default = 0; }
        public bool closing { get; set; default = false; }
        public Cancellable spawn_cancellable { get; private set; }
        public ArrayList<string> history { get; private set; }

        public TerminalTab (string id,
                            string label,
                            Vte.Terminal terminal,
                            Environment environment,
                            string[]? argv_override = null) {
            Object (
                id: id,
                label: label,
                terminal: terminal,
                environment: environment,
                argv_override: argv_override
            );
            spawn_cancellable = new Cancellable ();
            history = new ArrayList<string> ();
        }
    }
}
