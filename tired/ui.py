def select(options, title="", optimize_obvious_selection=True):
    if len(options) == 1 and optimize_obvious_selection:
        return 0

    import simple_term_menu

    return simple_term_menu.TerminalMenu(options, title=title).show()


def select_yn(title="") -> bool:
    selected_option_id = select(["[n]No", "[y]Yes"], title)

    return bool(selected_option_id)  # bool hack: 0 and 1 match False and True


def get_input_using_temporary_file(file_path=".tmp", editor="vim", initial_message="", force_rewrite_initial_message=True):
    import tired.command
    import os

    # Create file
    if not os.path.isfile(file_path) or force_rewrite_initial_message:
        with open(file_path, 'w') as f:
            f.write(initial_message)

    tired.command.execute(f"{editor} {file_path}")

    with open(file_path, 'r') as f:
        return f.read()


def select_map(options_dict: dict, title="", optimize_obvious_selection=True):
    """
    Offers a user multiple choices, each one is associated w/ a particular
    value, e.g. callback.

    Returns (key, selection) pair.
    """
    options = list(options_dict.keys())
    selected_option_id = select(list(map(str, options)), title=title, optimize_obvious_selection=optimize_obvious_selection)
    key = options[selected_option_id]

    return key, options_dict[key]


def select_callback(options_cb: dict, title=""):
    key, callback = select_map(options_cb, title, optimize_obvious_selection=False)
    callback()

