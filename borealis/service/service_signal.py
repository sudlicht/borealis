class ServiceSignal:
    """
    Signal class used for communication in service
    back to main thread for a signal.
    """

    signal: str
    """
    The name of the signal being emitted
    """

    args: list
    """
    Positional arguments to be emitted by this signal to callbacks
    """

    def __init__(self, signal: str, *args):
        self.args = args
        self.signal = signal
