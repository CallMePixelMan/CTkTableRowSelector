from __future__ import annotations

import tkinter as tk

from CTkTable import CTkTable
import customtkinter


class CTkTableRowSelector:
    CTRL_KEYCODE = 37

    def __init__(
        self,
        table: CTkTable,
        selected_row_color: str | tuple[str, str] | None = None,
        selected_row_text_color: str | tuple[str, str] | None = None,
        max_selection: int | None = None,
        can_select_headers=False,
    ) -> None:
        """
        Lets you select rows in a CTkTable easely, with CTRL key support
        for multiple row selection.

        Note:
            Will add some listeners to the table's window (toplevel or tk).
            Could create some side effects.

        Args:
            table (CTkTable): The table bound to the RowSelector
            selected_row_color (str | tuple[str, str] | None, optional)
                customtkinter supported color used to indicate when a row is selected.
                by default will use the fg_color of the button of your
                customtkinter theme.
            selected_row_text_color (str | tuple[str, str] | None, optional)
                customtkinter supported color, by default will use the table text color.
            can_select_headers (bool, optional): If True, the user can
                select the headers as a row. Defaults to False.
            max_selection (int | None): Maximum number of row selected at the same
                time. Use None for no maximum. Must be greater or equal to 1.
        Todo:
            Missing support for SHIFT Key.
            Missing support for vertical CTkTable.

        Raises:
            NotImplementedError: Not compatible with a non horizontal CTkTable.
            ValueError: max_selection is not None and less than 1.
        """
        if table.orient != "horizontal":
            raise NotImplementedError(
                f"{self.__class__.__name__} is not compatible with a non horizontal CTkTable. Got {table.orient=}."  # noqa
            )
        if max_selection is not None and max_selection < 1:
            raise ValueError(
                f"max_selection must be None, 1 or greater. Got {max_selection=}."
            )

        # CTRL key press binding
        self.ctrl_pressed = False
        root = table.winfo_toplevel()
        root.bind("<KeyPress>", self._set_ctrl_pressed(True), add="+")
        root.bind("<KeyRelease>", self._set_ctrl_pressed(False), add="+")

        # Selection colors
        self.selected_row_color = (
            selected_row_color
            or customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]
        )
        self.selected_row_text_color = selected_row_text_color or table.text_color

        # Selection
        self.table = table
        self.can_select_headers = can_select_headers
        self.max_selection = max_selection or float("inf")
        self.selected_rows = set()

        # Command binding
        table.command = self
        table.draw_table()

    def _set_ctrl_pressed(self, new_state: bool):
        def callback(event: tk.Event):
            if event.keycode == CTkTableRowSelector.CTRL_KEYCODE:
                self.ctrl_pressed = new_state

        return callback

    def _unselected_row_color(self, row: int) -> str:
        return self.table.fg_color if row % 2 == 0 else self.table.fg_color2

    def _colorize_row(self, row_index: int, is_selected: bool) -> None:
        color = (
            self.selected_row_color
            if is_selected
            else self._unselected_row_color(row_index)
        )
        text_color = (
            self.selected_row_text_color if is_selected else self.table.text_color
        )

        self.table.edit_row(row_index, fg_color=color, text_color=text_color)

        last_row_index = self.table.rows - 1
        last_column_index = self.table.columns - 1
        if row_index == 0:
            self.table.frame[row_index, 0].configure(
                background_corner_colors=["", color, color, color]
            )
            self.table.frame[row_index, last_column_index].configure(
                background_corner_colors=[color, "", color, color]
            )
        elif row_index == last_row_index:
            self.table.frame[row_index, 0].configure(
                background_corner_colors=[color, color, color, ""]
            )
            self.table.frame[row_index, last_column_index].configure(
                background_corner_colors=[color, color, "", color]
            )

    def select(self, row_index: int) -> None:
        """
        Adds a row to the selection.
        Adding a row twice has no effect.
        Adding a row while max_selection is reached has no effect.

        Args:
            row_index (int): The index of the row.
        """
        if len(self.selected_rows) >= self.max_selection:
            return

        self.selected_rows.add(row_index)
        self._colorize_row(row_index, True)

    def clear_selection(self) -> None:
        """
        Clears the selection.
        """
        for row in self.selected_rows:
            self._colorize_row(row, False)
        self.selected_rows.clear()

    def unselect(self, row_index: int) -> None:
        """
        Remove a row from the selection.
        Removing a row that is not selected will raise a KeyError.

        Args:
            row_index (int): The index of the row.

        Raises:
            KeyError: row is not selected.
        """
        self.selected_rows.remove(row_index)
        self._colorize_row(row_index, False)

    def __call__(self, click_infos: dict):
        """
        Used by the table as the command to process each cell click.

        Args:
            click_infos (dict): The values given by the CTkTable.
        """
        row = click_infos["row"]

        if not self.can_select_headers and row == 0:
            return

        row_is_already_selected = row in self.selected_rows

        if row_is_already_selected:
            if self.ctrl_pressed:
                self.unselect(row)
            else:
                self.clear_selection()
                self.select(row)

        else:
            if not self.ctrl_pressed:
                self.clear_selection()

            self.select(row)

    def get(self) -> list[list]:
        """
        Returns a list of all the selected rows values.

        Returns:
            list[list]: A list of all the rows.
        """
        return [self.table.get_row(row) for row in self.selected_rows]
