import tired.command
import tired.logging

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


def get_remote_repository_name(remote_tag="origin"):
    # TODO
    pass
