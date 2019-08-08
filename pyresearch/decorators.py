from functools import wraps
import time

def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("###############  START  ###############")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print("###############  END  ###############")
        elapsed_time = round(elapsed_time, 5)
        print(
            f"{elapsed_time}[sec] elapsed to execute the function:{func.__name__}"
        )
        return result
    return wrapper


def print_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("func:", func.__name__)
        print("args:", args)
        print("kwargs:", kwargs)
        result = func(*args, **kwargs)
        print("result:", result)
        return result
    return wrapper
