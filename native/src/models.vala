using Gee;

namespace Atoms {

    public class TerminalTab : Object {
        public string id { get; construct; }
        public string label { get; set; }
        public Vte.Terminal terminal { get; construct; }
        public Environment environment { get; set; }
        public int shell_pid { get; set; default = 0; }
        public int background_processes { get; set; default = 0; }
        public ArrayList<string> history { get; private set; }

        public TerminalTab (string id,
                            string label,
                            Vte.Terminal terminal,
                            Environment environment) {
            Object (
                id: id,
                label: label,
                terminal: terminal,
                environment: environment
            );
            history = new ArrayList<string> ();
        }
    }
}
