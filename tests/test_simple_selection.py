import pytest

from CTkTableRowSelector import CTkTableRowSelector


def test_select_unselect_clear(rowselector_clickable_headings: CTkTableRowSelector):
    assert rowselector_clickable_headings.get() == []

    rowselector_clickable_headings.select(1)
    assert rowselector_clickable_headings.get() == [[1, 2, 3]]
    rowselector_clickable_headings.select(2)
    assert rowselector_clickable_headings.get() == [[1, 2, 3], [4, 5, 6]]

    rowselector_clickable_headings.unselect(2)
    assert rowselector_clickable_headings.get() == [[1, 2, 3]]

    rowselector_clickable_headings.clear_selection()
    assert rowselector_clickable_headings.get() == []


def test_selection_to_much(rowselector_max_2_select: CTkTableRowSelector):
    assert rowselector_max_2_select.get() == []

    rowselector_max_2_select.select(1)
    rowselector_max_2_select.select(2)
    assert rowselector_max_2_select.get() == [[1, 2, 3], [4, 5, 6]]

    rowselector_max_2_select.select(3)
    assert rowselector_max_2_select.get() == [[1, 2, 3], [4, 5, 6]]


def test_selecting_twice(rowselector_clickable_headings: CTkTableRowSelector):
    assert rowselector_clickable_headings.get() == []

    rowselector_clickable_headings.select(1)
    rowselector_clickable_headings.select(1)
    assert rowselector_clickable_headings.get() == [[1, 2, 3]]


def test_unselecting_twice(rowselector_clickable_headings: CTkTableRowSelector):
    assert rowselector_clickable_headings.get() == []

    with pytest.raises(KeyError):
        rowselector_clickable_headings.unselect(0)

    assert rowselector_clickable_headings.get() == []
