import unittest
from fcntl import LOCK_SH, LOCK_EX
from task_utils.advisory_lock import TaskLock

lock = TaskLock("test.lock")

class TestTaskLock(unittest.TestCase):
    @lock.synchronized(LOCK_SH)
    def my_func1(self):
        return 123

    @lock.synchronized(LOCK_EX)
    def my_func2(self):
        return 456

    def test_passthrough(self):
        self.assertEqual(self.my_func1(), 123)
        self.assertEqual(self.my_func2(), 456)

if __name__ == '__main__':
    unittest.main()