import pytest

import customtkinter as ctk
from CTkTable import CTkTable

from CTkTableRowSelector import CTkTableRowSelector


def test_invalid_table_orientation():
    root = ctk.CTk()
    table = CTkTable(root, orientation="veritical")

    with pytest.raises(NotImplementedError):
        CTkTableRowSelector(table, "")


def test_invalid_max_selection():
    root = ctk.CTk()
    table = CTkTable(root)

    with pytest.raises(ValueError):
        CTkTableRowSelector(table, "red", max_selection=-1)

    with pytest.raises(ValueError):
        CTkTableRowSelector(table, "red", max_selection=-1)
