import inspect
import re


def override(method):
    """
    Provides functioning @override tag
    https://stackoverflow.com/a/14631397
    """

    stack = inspect.stack()
    base_classes = re.search(r'class.+\((.+)\)\s*\:', stack[2][4][0]).group(1)

    # handle multiple inheritance
    base_classes = [s.strip() for s in base_classes.split(',')]
    if not base_classes:
        raise ValueError('overrides decorator: unable to determine base class')

    # stack[0]=overrides, stack[1]=inside class def'n, stack[2]=outside class def'n
    derived_class_locals = stack[2][0].f_locals

    # replace each class name in base_classes with the actual class type
    for i, base_class in enumerate(base_classes):

        if '.' not in base_class:
            base_classes[i] = derived_class_locals[base_class]

        else:
            components = base_class.split('.')

            # obj is either a module or a class
            obj = derived_class_locals[components[0]]

            for c in components[1:]:
                assert (inspect.ismodule(obj) or inspect.isclass(obj))
                obj = getattr(obj, c)

            base_classes[i] = obj

    assert (any(hasattr(cls, method.__name__) for cls in base_classes))
    return method
