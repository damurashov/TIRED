def select(options, title="", optimize_obvious_selection=True, option_shortcuts=None):
    """
    Shortcuts are one-letter hotkeys
    """
    if option_shortcuts is not None and len(option_shortcuts) == len(options):
        options = list(map(lambda i: f'[{i[0]}] {i[1]}' if len(i[0]) else i[1], zip(option_shortcuts, options)))

    if len(options) == 1 and optimize_obvious_selection:
        return 0

    import simple_term_menu

    return simple_term_menu.TerminalMenu(options, title=title).show()

def multiselect(options, title="", option_shortcuts=None, preselected_entries=list()):
    """ preselected_items -- list of int or str, may be mixed """
    preselected_entries = list(map(lambda i: preselected_entries.index(i) if type(i) is str else i, preselected_entries))

    if option_shortcuts is not None and len(option_shortcuts) == len(options):
        options = list(map(lambda i: f'[{i[0]}] {i[1]}' if len(i[0]) else i[1], zip(option_shortcuts, options)))

    import simple_term_menu

    if option_shortcuts is not None and len(option_shortcuts) == len(options):
        options = list(map(lambda i: f'[{i[0]}] {i[1]}' if len(i[0]) else i[1], zip(option_shortcuts, options)))

    try:
        return simple_term_menu.TerminalMenu(options, title=title, multi_select=True, show_multi_select_hint=True,
                multi_select_select_on_accept=False, preselected_entries=preselected_entries).show()
    except KeyboardInterrupt as e:
        return tuple()


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


def select_map(options_dict: dict, title="", optimize_obvious_selection=True, option_shortcuts=None):
    """
    Offers a user multiple choices, each one is associated w/ a particular
    value, e.g. callback.

    Returns (key, selection) pair.
    """
    options = list(options_dict.keys())
    selected_option_id = select(list(map(str, options)), title=title,
        optimize_obvious_selection=optimize_obvious_selection, option_shortcuts=option_shortcuts)
    key = options[selected_option_id]

    return key, options_dict[key]


def select_callback(options_cb: dict, title=""):
    key, callback = select_map(options_cb, title, optimize_obvious_selection=False)
    callback()


def print_progress(fraction, target=None, round_=1, units='', title="", normalize=True):
    """
    If `target` is None, `current` is used, no percentage.
    - units = '%' will cause normalizing to 100%
    """
    if normalize and target is not None:
        fraction = float(fraction / target)

    if units == '%' and target is not None:
        fraction *= 100.0

    fraction = round(fraction, round_)

    print(f"\r{title} {fraction}{units}", end='', flush=True)


def print_table_line(content, widths=None):
    if widths is None:
        widths = [18 for _ in range(len(content))]

    fmt = ''.join(map(lambda i: f'{{:<{i}}}', widths))

    print(fmt.format(*content))
