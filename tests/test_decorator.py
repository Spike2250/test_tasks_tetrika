import pytest
from tasks import strict


@pytest.mark.parametrize("input_data", [
    (1, "two"),
    (1, 2.4),
    (False, 3),
    (5, True),
])
def test_decorator_int_annotations(input_data):
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b

    with pytest.raises(Exception) as e:
        sum_two(*input_data)
        assert e.typename == TypeError
        assert "не соответствует аннотированному!!!" in e.value


@pytest.mark.parametrize("input_data", [
    (1, "two"),
    ("one", 2.4),
    ("one", 3),
    ("one", True),
])
def test_decorator_str_annotations(input_data):
    @strict
    def concatenate_strings(s1: str, s2: str) -> str:
        return s1 + s2

    with pytest.raises(Exception) as e:
        concatenate_strings(*input_data)
        assert e.typename == TypeError
        assert "не соответствует аннотированному!!!" in e.value


@pytest.mark.parametrize("input_data", [
    (1, "two", True),
    (True, False, True, (3,), True),
    (True, (True, ), False),
    (4.6, True),
    (True, 1),
])
def test_decorator_bool_annotations(input_data):
    @strict
    def all_true(flag_1: bool, flag_2: bool, *args) -> bool:
        return all(
            (flag_1, flag_2, *args)
        )

    with pytest.raises(Exception) as e:
        all_true(*input_data)
        assert e.typename == TypeError
        assert "не соответствует аннотированному!!!" in e.value


@pytest.mark.parametrize("input_data", [
    (1, "two"),
    (1, 2.4),
    (False, 3),
    (5, True),
    (3, 2),
])
def test_decorator_multy_annotations(input_data):
    @strict
    def some_func(a: str | float, b: str | float) -> str:
        return f"{a} + {b}"

    with pytest.raises(Exception) as e:
        some_func(*input_data)
        assert e.typename == TypeError
        assert "не соответствует аннотированному!!!" in e.value
