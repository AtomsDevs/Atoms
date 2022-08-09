class ClientBridge:
    """
    This class does nothing by default other than wrapping standard methods 
    and then re-executing them. This should be extended and passed to the 
    backend when the toolkit used for the client needs to be adjusted when 
    the backend needs to execute client methods. For example GTK is not 
    thread safe and since Atoms is recommended to be used in conjunction 
    with threading to run async, the backend must perform functions on the 
    main thread only via the appropriate GLib.idle_add method. Since the 
    Atoms backend is not meant to work with a single toolkit, it is not 
    possible to depend on GLib and therefore the GTK client will want to 
    extend this class to make Atoms compatible with the toolkit.
    """

    client_name: str
    client_toolkit: str

    def __init__(self, client_name: str=None, client_toolkit: str=None):
        if client_name is None:
            client_name = ""

        if client_toolkit is None:
            client_toolkit = ""

        self.client_name = client_name
        self.client_toolkit = client_toolkit

    def exec_on_main(func, *args):
        """
        This method should be replaced by the client according to the 
        toolkit used (if needed).
        """
        return func(*args)
