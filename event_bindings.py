def bind_events(root, save_file_callback):
    """Bind all events."""
    root.bind('<Control-s>', save_file_callback)
    # root.protocol("WM_DELETE_WINDOW", on_closing_callback)