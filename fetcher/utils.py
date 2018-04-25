import time

def timeout(timeout):
    """
    Timeout Decorator
    :timeout: seconds to wait after function call
    """
    def timeout_decorator(function):
        def timeout_wrapper(*args, **kwargs):
            rv = function(*args, **kwargs)
            time.sleep(timeout)
            return rv
        return timeout_wrapper
    return timeout_decorator