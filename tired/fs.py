def get_directory_content(directory: str):
    """
    Iterate only through directory content
    """
    import os

    content = os.listdir(directory)

    return content


def get_directory_content_directories(directory: str):
    import os

    return filter(
        lambda item: os.path.isdir(item), iterate_directory_content(directory))
