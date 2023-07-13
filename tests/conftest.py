import pytest
import tkinter

import customtkinter as ctk
from CTkTable import CTkTable

from CTkTableRowSelector import CTkTableRowSelector


@pytest.fixture
def rowselector_clickable_headings():
    root = ctk.CTk()
    table = CTkTable(
        root,
        values=[
            ["Header_A", "Header_B", "Header_C"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ],
    )
    return CTkTableRowSelector(table, "red", can_select_headers=True)


@pytest.fixture
def rowselector_not_clickable_headings():
    root = ctk.CTk()
    table = CTkTable(
        root,
        values=[
            ["Header_A", "Header_B", "Header_C"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ],
    )
    return CTkTableRowSelector(table, "red", can_select_headers=False)


@pytest.fixture
def rowselector_max_2_select():
    root = ctk.CTk()
    table = CTkTable(
        root,
        values=[
            ["Header_A", "Header_B", "Header_C"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ],
    )
    return CTkTableRowSelector(table, "red", max_selection=2, can_select_headers=False)


@pytest.fixture
def ctrl_keypress_event_mock():
    event = tkinter.Event()
    event.keycode = 37
    return event


@pytest.fixture
def not_ctrl_keypress_event_mock():
    event = tkinter.Event()
    event.keycode = 36
    return event


@pytest.fixture
def first_row_click_mock():
    return {"row": 0}


@pytest.fixture
def second_row_select_mock():
    return {"row": 1}


@pytest.fixture
def third_row_select_mock():
    return {"row": 2}


@pytest.fixture
def last_row_select_mock():
    return {"row": 3}


@pytest.fixture
def ctrl_pressed_callback(rowselector_clickable_headings):
    return rowselector_clickable_headings._set_ctrl_pressed(True)


@pytest.fixture
def ctrl_released_callback(rowselector_clickable_headings):
    return rowselector_clickable_headings._set_ctrl_pressed(False)
