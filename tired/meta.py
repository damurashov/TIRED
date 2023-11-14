def module_file_as_module_object(module_file):
    """
    Example:

    ```
    module = tired.meta.module_file_as_module_object(__file__)
    ```
    """

    #TODO
    pass


def get_module_functions(module_object):
    # TODO
    pass


def get_current_context_string():
    """
    Builds the caller's context using instrospection based on "inspect". The
    format is this:

    <MODULE>.<CLASS_NAME_INCLUDING_NESTED_ONES>.<FUNCTION_NAME>

    README: Implementation guidelines

    Get nested class name

    ```
    import inspect

    def get_caller_class_name():
        stack = inspect.stack()
        caller_frame = stack[1]
        caller_class_name = caller_frame[0].f_locals.get("self", None).__class__.__name__
        return caller_class_name
    ```

    Getting function name from that is obvious

    """
    # TODO
    pass
