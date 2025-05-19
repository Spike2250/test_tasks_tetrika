from tasks import get_category_counts, save_to_csv

import pytest
import pandas as pd

from pathlib import Path

from typing import Dict


TEST_URL = "https://ru.wikipedia.org/wiki/Категория:Естественные_науки"
TEST_FILEPATH = "my_test_csv.csv"
TEST_DATA = {
    "А": 4,
    "В": 12,
    "Г": 6,
    "Я": 3,
    "F": 1,
}


def test_get_category_counts():
    data = get_category_counts(TEST_URL)

    assert isinstance(data, Dict)
    assert data.get("Х", 0) == 1
    assert data.get("Е", 0) == 2
    assert data.get("Ф", 0) == 1
    assert data.get("А", 0) == 0


@pytest.mark.parametrize("add_zero_counts, only_russian_letters", [
    (True, True),
    (False, True),
    (False, False),
    (True, False),
])
def test_save_to_csv(add_zero_counts, only_russian_letters):

    df = save_to_csv(
        TEST_DATA, TEST_FILEPATH,
        add_zero_counts=add_zero_counts,
        only_russian_letters=only_russian_letters
    )
    assert isinstance(df, pd.DataFrame)
    output_file = Path(TEST_FILEPATH)
    assert output_file.is_file()

    russian_letters_num = 32  # ввиду отсутствия буквы Ё
    if add_zero_counts:
        if only_russian_letters:
            assert len(df) == russian_letters_num
        else:
            assert len(df) == russian_letters_num + 1
    else:
        if only_russian_letters:
            assert len(df) == len(TEST_DATA) - 1
        else:
            assert len(df) == len(TEST_DATA)

    # удаляем файл
    output_file.unlink()
