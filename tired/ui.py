def select(options, title=""):
    import simple_term_menu

    return simple_term_menu.TerminalMenu(options, title=title).show()
