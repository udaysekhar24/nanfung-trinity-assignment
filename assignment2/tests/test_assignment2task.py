import pytest
from assignment2 import Assignment2Task


class TestAssignment2Task:

    def test_assignment2_success1(self):
        with pytest.raises(SystemExit) as test_exit:
            a2t = Assignment2Task.Assignment2Task()
            a2t.run()
            assert test_exit.type == SystemExit
            assert test_exit.value.code == 0


if __name__ == '__main__':
    pytest.main()
