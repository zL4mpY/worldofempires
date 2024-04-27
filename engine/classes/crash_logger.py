himamont = 1
import traceback

def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name_

try:
    himamont += zhopas
except Exception as e:
    error = e
    tb_str = ''.join(traceback.format_exception(None, error, error.__traceback__))
    print(tb_str)
print(1)