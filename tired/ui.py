def select(options, title=""):
    import simple_term_menu

    return simple_term_menu.TerminalMenu(options, title=title).show()


def select_yn(title="") -> bool:
    selected_option_id = select(["[n]No", "[y]Yes"], title)

    return bool(selected_option_id)  # bool hack: 0 and 1 match False and True
