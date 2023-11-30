import pathlib
import tired.fs
import tired.logging


class JsonConfigStorage:
    """
    Stores a dict in a JSON file
    @pre it is assumed that the dict is a valid JSON object
    """

    def __init__(self, file_path: str):
        self._file_path = file_path

    def load(self) -> dict:
        import json

        try:
            with open(self._file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return dict()

    def save(self, config: dict) -> None:
        import json

        with open(self._file_path, 'w') as f:
            json.dump(config, f, indent=4)


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
        # Initialize paths
        self._config_directory_path = pathlib.Path(tired.fs.get_platform_config_directory_path()) / application_name
        tired.logging.debug(f'Ensuring directory {self._config_directory_path} exists')
        self._config_directory_path.mkdir(parents=True, exist_ok=True)
        self._config_file_path = self._config_directory_path / config_file_name

        # Create, or load config file

        if storage_type == "json":
            self._config_storage = JsonConfigStorage(str(self._config_file_path))
            self._config = self._config_storage.load()
        else:
            raise Exception(f'Unsupported config type "{storage_type}"')

    def set_field(self, field_name: str, field_value: object):
        """
        Updates a (field,value) pair. If it does not exist, it will be created.
        field_name: unique string identifier
        field_value is any object that is supported by the backend If
        `field_value` type is not supported by the backend, an exception may be
        raised when attempting to save the new config
        """
        self._config[field_name] = field_value

    def get_field(self, field_name: str) -> object:
        """
        May raise `KeyError`
        """
        return self._config[field_name]

    def sync(self):
        self._config_storage.save(self._config)
