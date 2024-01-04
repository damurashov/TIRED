import * from tired.ux
import os
import pathlib
import tired.fs
import tired.logging


def try_get_env(variable_name, accepted_values=None, panic_if_missing=False, type_=None):
    """
    - accepted_values: if iterable, the value will be checked against those in
      the list. If does not check, an exception will be raised
    - must_be_present: if not, an exception will be raised
    """
    value = os.getenv(variable_name, None)

    if value is None and panic_if_missing:
        message = f'Environment variable "{variable_name}" must be set'
        tired.logging.error(message)

        raise ValueError(message)
    elif accepted_values is not None and value not in accepted_values:
        message = f'Environment variable has value "{value}", but accepted values are: "{accepted_values}"'
        tired.logging.error(message)

        raise ValueError(message)

    if type_ is not None:
        try:
            value = type_(value)
        except ValueError as e:
            tired.logging.error(f'Expected environment variable "{variable_name}" of type {type_}, failed to cast')

            raise e

    if value is not None:
        tired.logging.info(f'Got environment variable {variable_name}="{value}"')
    else:
        tired.logging.info(f'Didn\'t get environment variable "{variable_name}", continuing')

    return value
