import pytest
from assignment1 import Assignment1Task


class TestAssignment1Task:

    def test_assignment1_success1(self):
        with pytest.raises(SystemExit) as test_exit:
            a1t = Assignment1Task.Assignment1Task()
            a1t.run()
            assert test_exit.type == SystemExit
            assert test_exit.value.code == 0


if __name__ == '__main__':
    pytest.main()
