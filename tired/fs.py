import os
import pathlib
import tired.logging


def get_directory_content(directory: str):
    """
    Iterate only through directory content
    """
    import os

    real_path = pathlib.Path(directory).resolve()
    content = os.listdir(str(real_path))

    return content


def get_directory_content_directories(directory: str, exclude_symbolic_links=False):
    """
    List-out everything but directories
    """
    import os

    directory_path_object = pathlib.Path(directory).resolve()

    for item in get_directory_content(directory):
        absolute_path_string = str(directory_path_object / item)

        if os.path.isdir(absolute_path_string) \
                and not (exclude_symbolic_links and os.path.islink(absolute_path_string)):
            yield item


def find(glob_pattern: str, root: str = None, is_recursive: bool = True, is_file: bool = None, is_symlink: bool = None, is_directory: bool = None):
    """
    Finds an item in a directory. Additional constraints (is_recursive,
    is_file, is_link) may be imposed, `None` for "doesn't matter".
    "is_recursive" will make it traverse the directory in a recursive fashion.
    Uses pathlib.Path().glob or pathlib.Path().rglob.
    """
    def find_filter(path):
        return (is_file and path.is_file() or is_file is None) and \
            (is_directory == path.is_dir() or is_directory is None) and \
            (is_symlink == path.is_symlink() or is_symlink is None)

    if root is None:
        root = os.getcwd()

    path = pathlib.Path(root)

    if is_recursive:
        iterator = path.rglob(glob_pattern)
    else:
        iterator = path.glob(glob_pattern)

    filtered_iterator = filter(find_filter, iterator)

    return filtered_iterator


def find_up(glob_pattern: str, root: str = None, is_file: bool = None, is_symlink: bool = None, is_directory: bool = None):
    if root is None:
        root = pathlib.Path(os.getcwd()).resolve()
    else:
        root = pathlib.Path(root).resolve()

    n_steps = len(root.parts)

    while n_steps > 0:
        yield from find(glob_pattern, root, False, is_file, is_symlink, is_directory)
        n_steps -= 1
        root = root.parent


def find_unique(*args, **kwargs):
    """
    Finds exactly one item matching the request, or raises an exception
    """
    result = None
    result = list(find(*args, **kwargs))
    tired.logging.debug("result", str(result))

    if len(result) == 0:
        tired.logging.error("Failed to find file")

        raise FileNotFoundError("Failed to find file")
    elif len(result) > 1:
        tired.logging.error("More than 1 file matches the query")

        raise FileNotFoundError("More than 1 file matches the query")


    return result[0]


def get_platform_config_directory_path():
    import appdirs

    return str(appdirs.user_config_dir())


def append_or_create(path):
    try:
        return open(path, 'r+')
    except FileNotFoundError:
        return open(path, 'w')


class _FilePrependWrapper:

    def __init__(self, instance):
        self._instance = instance
        self._content = self._instance.read()
        self._instance.seek(0)

    def __enter__(self):
        return self._instance.__enter__()

    def __exit__(self, type_, value, traceback):
        self.close()

    def get_content(self):
        return self._content

    def close(self):
        self._instance.write(self._content)
        self._instance.close()


def prepend_or_create(path):
    f = append_or_create(path)

    return _FilePrependWrapper(f)
