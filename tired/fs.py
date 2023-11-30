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


def get_platform_config_directory_path():
    import appdirs

    return str(appdirs.user_config_dir())
