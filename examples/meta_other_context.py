import tired.meta

class ClassContext:

    def callme(self):
        print(tired.meta.get_stack_context_string())

    @staticmethod
    def static_call_me():
        print(tired.meta.get_stack_context_string())


def function_context():
    print(tired.meta.get_stack_context_string())
