
def select(options, title=""):
    import simple_term_menu

    return simple_term_menu.TerminalMenu(options, title=title).show()


def select_yn(title="") -> bool:
    selected_option_id = select(["[n]No", "[y]Yes"], title)

    return bool(selected_option_id)  # bool hack: 0 and 1 match False and True


def get_input_using_temporary_file(file_path=".tmp", editor="vim", initial_message=""):
    import tired.command

    # Create file
    with open(file_path, 'w') as f:
        f.write(initial_message)

    tired.command.execute(f"{editor} {file_path}")

    with open(file_path, 'r') as f:
        return r.read()
