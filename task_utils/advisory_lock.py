# WARNING: It is a preliminary version.

from fcntl import flock, LOCK_UN
from functools import wraps
import logging

# TODO: Should we use @wrapt.decorator?

class TaskLock:
    def __init__(self, lock_file):
        self.lock_file = lock_file
        # self.sequential = self._sequential()

    def synchronized(self, lock_mode):
        """lock_mode is either LOCK_EX or lock_SH."""
        def sequential_decorator(func):
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                with open(self.lock_file, 'w') as file:
                    logger = logging.getLogger(__name__)
                    logger.debug("Locking a task...")
                    flock(file, lock_mode)
                    try:
                        return func(*args, **kwargs)
                    finally:
                        logger.debug("Unlocking a task...")
                        # unlink(self.lock_file)  # Don't do: http://stackoverflow.com/q/17708885/856090
                        flock(file, LOCK_UN)
                        # unlink(self.lock_file)  # Don't do: open but unlocked file may be deleted.
            return func_wrapper
        return sequential_decorator

    # TODO: Implement `with` locking