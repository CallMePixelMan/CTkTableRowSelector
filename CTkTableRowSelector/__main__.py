import itertools

import customtkinter as ctk
from CTkTable import CTkTable

from . import CTkTableRowSelector


themes = itertools.cycle(["dark", "light"])


def switch_theme():
    ctk.set_appearance_mode(next(themes))


value = [
    ["Header" + letter for letter in "ABCDE"],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
]


class PrintSelectionButton(ctk.CTkButton):
    def __init__(self, master, row_selector):
        super().__init__(
            master, text="Print Selection", command=self.print_get(row_selector)
        )

    def print_get(self, row_selector):
        return lambda rs=row_selector: print(rs.get())


root = ctk.CTk()
root.title(__package__ + " demo")


# Top frame
top = ctk.CTkFrame(root)
top.pack(pady=20, padx=20)

ctk.CTkLabel(top, text="Max 2 row, without headers. (Tip: Use CTRL Key)").pack()

max_two_row_table = CTkTable(top, row=5, column=5, values=value)
max_two_row_table.pack(expand=True, fill="both", padx=10, pady=(0, 10))
max_two_row_selector = CTkTableRowSelector(max_two_row_table, max_selection=2)

PrintSelectionButton(top, max_two_row_selector).pack(pady=(0, 10))


# Bottom frame
bottom = ctk.CTkFrame(root)
bottom.pack(pady=20, padx=20)

ctk.CTkLabel(bottom, text="No limit!").pack()

no_limit_table = CTkTable(bottom, row=5, column=5, values=value)
no_limit_table.pack(expand=True, fill="both", padx=10, pady=(0, 10))
no_limit_selector = CTkTableRowSelector(no_limit_table, can_select_headers=True)

PrintSelectionButton(bottom, no_limit_selector).pack(pady=(0, 10))

ctk.CTkButton(root, text="Change theme", command=switch_theme).pack(pady=20)

root.mainloop()
