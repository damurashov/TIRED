import meta_other_context
import tired.meta


class ClassContext:

    def callme(self):
        print(tired.meta.get_stack_context_string())


def function_context():
    print(tired.meta.get_stack_context_string())


if __name__ == "__main__":
    # Context of the main module
    c = ClassContext()
    c.callme()
    function_context()
    print(tired.meta.get_stack_context_string())

    # Context of imported module
    c2 = meta_other_context.ClassContext()
    c2.callme()
    meta_other_context.ClassContext.static_call_me()
    meta_other_context.function_context()
