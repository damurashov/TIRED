def get_directory_content(directory: str):
    """
    Iterate only through directory content
    """
    import os
    import pathlib

    real_path = pathlib.Path(directory).resolve()
    content = os.listdir(str(real_path))

    return content


def get_directory_content_directories(directory: str, exclude_symbolic_links=False):
    """
    List-out everything but directories
    """
    import os
    import pathlib

    directory_path_object = pathlib.Path(directory).resolve()

    for item in get_directory_content(directory):
        absolute_path_string = str(directory_path_object / item)

        if os.path.isdir(absolute_path_string) \
                and not (exclude_symbolic_links and os.path.islink(absolute_path_string)):
            yield item


def find(glob_pattern: str, is_recursive: bool = True, is_file: bool = None, is_link: bool = None, is_directory: bool = None):
    """
    Finds an item in a directory. Additional constraints (is_recursive,
    is_file, is_link) may be imposed, `None` for "doesn't matter".
    "is_recursive" will make it traverse the directory in a recursive fashion.
    Uses pathlib.Path().glob or pathlib.Path().rglob.
    """
    def find_filter(path):
        return (is_file and path.is_file() or is_file is None) and \
            (is_directory == path.is_dir() or is_directory is None) and \
            (is_link == path.is_link() or is_link is None)

    path = pathlib.path(glob_pattern)

    if is_recursive:
        iterator = path.rglob(glob_pattern)
    else:
        iterator = path.rlob(glob_pattern)

    filtered_iterator = filter(find_filter, iterator)

    return filtered_iterator


def find_unique(*args, **kwargs):
    """
    Finds exactly one item matching the request, or raises an exception
    """
    counter = 2
    result = None
    find_iterator = find(*args, **kwargs)
    result = next(find_iterator)

    try:
        result = next(find_iterator)
    except StopIteration as e:
        return result

    raise Exception("The requested pattern does not match to a unique response")


def get_platform_config_directory_path():
    import appdirs

    return str(appdirs.user_config_dir())
