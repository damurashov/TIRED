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
    import os

    return filter(
        lambda item: os.path.isdir(item) and not (exclude_symbolic_links and os.path.islink(item)),
        get_directory_content(directory)
    )
