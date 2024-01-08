import dataclasses
import tired.command
import tired.logging
import tired.parse
import tired.shlex


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


@dataclasses.dataclass
class Staged:
    status: str
    relative_path: str
    new_path: str = None  # Only valid in the case of a rename


def get_staged_status(use_relative_paths=False):
    """
    Iterates through staged files returning the instances of `Staged` class
    """
    relative_flag = "--relative" if use_relative_paths else ""
    command_string = f"git status --short"
    output, code = tired.command.get_output_with_code(command_string)

    if code != 0:
        tired.logging.error(_LOG_CONTEXT, f"Failed to execute command `{command_string}`")

        raise Exception(f"Failed to execute command `{command_string}`, returned {code}")

    if "to be committed" not in output:
        tired.logging.warning(f"Nothing is staged for commit")

    output = filter(lambda s: s[0] in "MARCD", tired.parse.iterate_string_multiline(output))

    for status_line in output:
        parsed_status = tired.shlex.split(status_line)
        status = parsed_status[0]
        path = parsed_status[1]
        new_path = parsed_status[3] if '->' in parsed_status else None

        yield Staged(status, path, new_path)


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
