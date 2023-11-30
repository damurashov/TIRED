import pathlib
import tired.fs
import tired.logging

class JsonConfigStorage:

    def __init__(self, file_path: str):
        self._


class ApplicationConfig:
    """
    Represents application configuration as a set of key/value pairs.
    """

    def __init__(self, application_name: str,
                config_file_name: str = ".config",
                storage_type: str = "json"):
        """
        storage_type: what is the carrier type. Available values are: "json"
        application_name: string identifier that is used to distinguish between
        various configuration directories
        config_file_name: The name of the config file
        """
        config_directory_path = pathlib.Path(tired.fs.get_platform_config_directory_path()) / application_name
        tired.logging.debug(f'Ensuring directory {config_directory_path} exists')
        config_directory_path.mkdir(parents=True, exist_ok=True)

        if config_storage_type == "json":
            self._config_storage = JsonConfigStorage()

    def set_field(field_name: str, field_value: object):
        """
        Updates a (field,value) pair. If it does not exist, it will be created.
        field_name: unique string identifier
        field_value is any object that is supported by the backend If
        `field_value` type is not supported by the backend, an exception may be
        raised
        """
