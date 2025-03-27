import time
from traceback import format_exc
from typing import Callable

class TimerContext:
    def __init__(self, propagate_exc: bool,
                 func: Callable | None,
                 *args, **kwargs):
        self.propagate_exc = propagate_exc    # propagate the exception outside if True.
        self.func = func                      # The callable to execute.
        self.args = args                      # Positional arguments for the callable.
        self.kwargs = kwargs                  # Keyword arguments for the callable.
        self.elapsed_s = 0                    # To store elapsed time.
        self.result = None                    # To store the function’s result.
        self.exception = None                 # To store any exception raised.

    def __enter__(self):
        self.start = time.perf_counter()  # Start the timer.
        return self  # Return self so the caller can invoke .execute().

    def execute(self):
        # only execute self.func if self.func is provided, otherwise simply record the time elapsed inside the context
        if self.func:

            try:
                self.result = self.func(*self.args, **self.kwargs)

            except Exception as e:
                self.exception = e
                _traceback = format_exc(chain=False)
                print(f'Found an exception while execution your function: \n{_traceback}')
                if self.propagate_exc:
                    raise Exception(_traceback)

            return self.result

        else:
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        # Always capture the elapsed time.
        self.elapsed_s = time.perf_counter() - self.start
        # If an exception occurred outside of execute(), let it propagate.
        if exc_type is not None:
            return False  # Propagate unexpected exceptions.
        return True  # Otherwise, suppress exceptions (if any were caught in execute).


if __name__ == '__main__':
    def my_function(x, y):
        time.sleep(1)
        return x / y

    # Successful execution, without exception propagation and without a func
    with TimerContext(False, None) as t:
        result = my_function(10,2)
    print(f'Result: {result}, Stored execution time: {t.elapsed_s:.4f} seconds')

    # Successful execution, without exception propagation
    with TimerContext(False, my_function, 10, 2) as t:
        t.execute()
    print(f'Result: {t.result}, Stored execution time: {t.elapsed_s:.4f} seconds')

    # Execution that raises an exception, without exception propagation
    with TimerContext(False, my_function, 10, 0) as t:
        t.execute()
    if t.exception:
        print(f'An error occurred: {t.exception}')
    print(f'Stored execution time: {t.elapsed_s:.4f} seconds')

    print('MANUAL assessment required ! Exceptions should not propagate outside of the context manager up until this point.')

    # Execution that raises an exception, with exception propagation
    time.sleep(3)
    print('MANUAL assessment required ! An exception should show outside the context manager in a few seconds.')
    time.sleep(3)
    with TimerContext(True, my_function, 10, 0) as t:
        t.execute()
    if t.exception:
        print(f'An error occurred: {t.exception}')
    print(f'Stored execution time: {t.elapsed_s:.4f} seconds')