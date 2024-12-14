class OutputHandlerRegistry:
    _handlers = {}

    @classmethod
    def register_handler(cls, name, handler):
        """
        Registers a handler by name.

        Parameters
        ----------
        name : str
            The name of the handler.
        handler : callable
            A callable object (e.g., function or method) to handle specific output types.
        """
        cls._handlers[name] = handler

    @classmethod
    def get_handler(cls, name):
        """
        Retrieves a registered handler by name.

        Parameters
        ----------
        name : str
            The name of the handler.

        Returns
        -------
        callable
            The registered handler if found; otherwise, None.
        """
        return cls._handlers.get(name)
