import signal
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

@contextmanager
def hard_timeout(seconds: int):
    def _handle(signum, frame):
        raise TimeoutError(f"Operation exceeded {seconds}s hard timeout")
    old = signal.signal(signal.SIGALRM, _handle)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
