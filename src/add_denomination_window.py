import tkinter as tk


class AddDenominationWindow(tk.Toplevel):
    def __init__(self, company: str, master=None):
        super().__init__(master)
        self.title(f"Add Denomination - {company}")
        self.geometry("350x120")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.result = None

        self.label = tk.Label(self, text="Enter a float value > 0:")
        self.label.pack(padx=10, pady=10)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.pack(padx=10, pady=5)

        self.button_ok = tk.Button(self, text="OK", command=self.ok)
        self.button_ok.pack(side="left", padx=10, pady=5)

        self.button_cancel = tk.Button(self, text="Cancel", command=self.cancel)
        self.button_cancel.pack(side="right", padx=10, pady=5)

        self.entry.bind("<Return>", lambda event: self.button_ok.invoke())
        self.entry.bind("<KP_Enter>", lambda event: self.button_ok.invoke())
        self.entry.bind("<Escape>", lambda event: self.button_cancel.invoke())

        self.entry.focus_set()

    def ok(self):
        try:
            value = float(self.entry_var.get())
            if value > 0:
                self.result = value
                self.destroy()
            else:
                self.label.config(text="Value must be greater than zero")
        except ValueError:
            self.label.config(text="Value must be a float (ex: 3.14)")

    def cancel(self):
        self.destroy()
