import tired.command
import tired.logging
import tired.parse


_LOG_CONTEXT = "tired.command"


def get_current_branch_name():
    command_string = "git rev-parse --abbrev-ref HEAD"
    output, code = tired.command.get_output_with_code(command_string)

    if code != 0:
        tired.logging.error(_LOG_CONTEXT, f"Failed to execute command `{command_string}`")

        raise Exception(f"Failed to execute command `{command_string}`, returned {code}")

    return output.strip()


def get_current_commit_hash():
    command_string = "git rev-parse HEAD"
    output, code = tired.command.get_output_with_code(command_string)

    if code != 0:
        tired.logging.error(_LOG_CONTEXT, f"Failed to execute command `{command_string}`")

        raise Exception(f"Failed to execute command `{command_string}`, returned {code}")

    return output.strip()


def get_staged_file_paths(use_relative_paths=False):
    """
    @param use_relative_paths. If true, the returned paths will be relative to PWD
    """
    relative_flag = "--relative" if use_relative_paths else ""
    command_string = f"git diff --name-only --staged {relative_flag}"
    output, code = tired.command.get_output_with_code(command_string)

    if code != 0:
        tired.logging.error(_LOG_CONTEXT, f"Failed to execute command `{command_string}`")

        raise Exception(f"Failed to execute command `{command_string}`, returned {code}")

    output = output.strip()

    return tired.parse.iterate_string_multiline(output)


def get_git_directory_from_nested_context():
    """
    TODO: git rev-parse --show-toplevel
    """
    command_string = f"git rev-parse --show-toplevel"
    output, code = tired.command.get_output_with_code(command_string)

    if code != 0:
        tired.logging.error(f"Failed to execute command `{command_string}`")

        raise Exception(f"Failed to execute command `{command_string}`, returned {code}")

    output = output.strip()

    return output
