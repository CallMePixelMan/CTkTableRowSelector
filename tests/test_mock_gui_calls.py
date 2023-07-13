from typing import Callable

import tkinter

from CTkTableRowSelector import CTkTableRowSelector


def test_ignore_not_ctrl_key(
    ctrl_pressed_callback: Callable[[tkinter.Event], None],
    ctrl_released_callback: Callable[[tkinter.Event], None],
    not_ctrl_keypress_event_mock: tkinter.Event,
    rowselector_clickable_headings: CTkTableRowSelector,
):
    assert not rowselector_clickable_headings.ctrl_pressed

    ctrl_pressed_callback(not_ctrl_keypress_event_mock)
    assert not rowselector_clickable_headings.ctrl_pressed

    ctrl_released_callback(not_ctrl_keypress_event_mock)
    assert not rowselector_clickable_headings.ctrl_pressed


def test_process_ctrl_key(
    ctrl_pressed_callback: Callable[[tkinter.Event], None],
    ctrl_released_callback: Callable[[tkinter.Event], None],
    ctrl_keypress_event_mock: tkinter.Event,
    rowselector_clickable_headings: CTkTableRowSelector,
):
    assert not rowselector_clickable_headings.ctrl_pressed

    ctrl_pressed_callback(ctrl_keypress_event_mock)
    assert rowselector_clickable_headings.ctrl_pressed

    ctrl_released_callback(ctrl_keypress_event_mock)
    assert not rowselector_clickable_headings.ctrl_pressed


def test_click_header(
    first_row_click_mock: dict,
    rowselector_clickable_headings: CTkTableRowSelector,
    rowselector_not_clickable_headings: CTkTableRowSelector,
):
    rowselector_clickable_headings(first_row_click_mock)
    assert rowselector_clickable_headings.get() == [
        ["Header_A", "Header_B", "Header_C"]
    ]

    # Proper corner color
    last_column = rowselector_clickable_headings.table.columns - 1
    assert rowselector_clickable_headings.table.frame[0, 0].cget(
        "background_corner_colors"
    ) == ["", "red", "red", "red"]
    assert rowselector_clickable_headings.table.frame[0, last_column].cget(
        "background_corner_colors"
    ) == ["red", "", "red", "red"]

    rowselector_not_clickable_headings(first_row_click_mock)
    assert rowselector_not_clickable_headings.get() == []


def test_click_lastline(
    last_row_select_mock: dict,
    rowselector_clickable_headings: CTkTableRowSelector,
):
    rowselector_clickable_headings(last_row_select_mock)
    assert rowselector_clickable_headings.get() == [[7, 8, 9]]

    # Proper corner color
    last_row = rowselector_clickable_headings.table.rows - 1
    last_column = rowselector_clickable_headings.table.columns - 1
    assert rowselector_clickable_headings.table.frame[last_row, 0].cget(
        "background_corner_colors"
    ) == ["red", "red", "red", ""]
    assert rowselector_clickable_headings.table.frame[last_row, last_column].cget(
        "background_corner_colors"
    ) == ["red", "red", "", "red"]


def test_click_not_selected_with_ctrl(
    second_row_select_mock: dict,
    third_row_select_mock: dict,
    rowselector_clickable_headings: CTkTableRowSelector,
):
    rowselector_clickable_headings.ctrl_pressed = True

    rowselector_clickable_headings(second_row_select_mock)
    assert rowselector_clickable_headings.get() == [[1, 2, 3]]
    rowselector_clickable_headings(third_row_select_mock)
    assert rowselector_clickable_headings.get() == [[1, 2, 3], [4, 5, 6]]


def test_click_not_selected_without_ctrl(
    second_row_select_mock: dict,
    third_row_select_mock: dict,
    rowselector_clickable_headings: CTkTableRowSelector,
):
    rowselector_clickable_headings.ctrl_pressed = False

    rowselector_clickable_headings(second_row_select_mock)
    assert rowselector_clickable_headings.get() == [[1, 2, 3]]
    rowselector_clickable_headings(third_row_select_mock)
    assert rowselector_clickable_headings.get() == [[4, 5, 6]]


def test_click_selected_with_ctrl(
    second_row_select_mock: dict,
    rowselector_clickable_headings: CTkTableRowSelector,
):
    rowselector_clickable_headings.ctrl_pressed = True

    rowselector_clickable_headings(second_row_select_mock)
    assert rowselector_clickable_headings.get() == [[1, 2, 3]]
    rowselector_clickable_headings(second_row_select_mock)
    assert rowselector_clickable_headings.get() == []


def test_click_selected_without_ctrl(
    second_row_select_mock: dict,
    third_row_select_mock: dict,
    rowselector_clickable_headings: CTkTableRowSelector,
):
    rowselector_clickable_headings.ctrl_pressed = True
    rowselector_clickable_headings(second_row_select_mock)
    rowselector_clickable_headings(third_row_select_mock)
    assert rowselector_clickable_headings.get() == [[1, 2, 3], [4, 5, 6]]

    rowselector_clickable_headings.ctrl_pressed = False
    rowselector_clickable_headings(second_row_select_mock)
    assert rowselector_clickable_headings.get() == [[1, 2, 3]]
