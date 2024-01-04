import * from tired.ux
import os
import pathlib
import tired.fs
import tired.logging


def try_get_env(variable_name, accepted_values=None, panic_if_missing=False):
    """
    - accepted_values: if iterable, the value will be checked against those in
      the list. If does not check, an exception will be raised
    - must_be_present: if not, an exception will be raised
    """
    value = os.getenv(variable_name, None)

    if value is None and panic_if_missing:
        raise ValueError(f'Environment variable "{variable_name}" must be set')
    else if accepted_values is not None and value not in accepted_values:
        raise ValueError(f'Environment variable has value "{value}", but accepted values are: "{accepted_values}"')

    return value
