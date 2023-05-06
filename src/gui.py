import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from functools import partial
from datetime import datetime
import tkinter.scrolledtext as scrolledtext
import pyperclip

from src.backend import count_tickets, produce_report, save_data, restore_data


class TicketCounterApp:
    def __init__(self, master=None):
        if not master:
            master = tk.Tk()
        self.master = master
        master.title("Ticket'Easy")
        master.geometry("800x600")

        # Initialize the ticket data
        self.ticket_data = restore_data("2023_05_03-21_40_56.json", True)

        # Create the main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(expand=True, fill="both")

        # Create the header frame
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(side="top", fill="x")

        # Create the header buttons
        self.save_button = tk.Button(self.header_frame, text="Save",
                                     command=self.save_data)
        self.save_button.pack(side="left", padx=5)

        self.load_button = tk.Button(self.header_frame, text="Load",
                                     command=self.load_data)
        self.load_button.pack(side="left", padx=5)

        self.load_reset_button = tk.Button(self.header_frame,
                                           text="Load & Reset",
                                           command=self.load_reset_data)
        self.load_reset_button.pack(side="left", padx=5)

        self.print_report_button = tk.Button(self.header_frame,
                                             text="Print Report",
                                             command=self.create_report_window)

        self.print_report_button.pack(side="left", padx=5)

        # Create the company frames
        self.sodexo_frame = tk.LabelFrame(self.main_frame, text="Sodexo",
                                          padx=10, pady=10)
        self.sodexo_frame.pack(side="left", expand=True, fill="both")

        self.edenred_frame = tk.LabelFrame(self.main_frame, text="Edenred",
                                           padx=10, pady=10)
        self.edenred_frame.pack(side="left", expand=True, fill="both")

        self.groupe_up_frame = tk.LabelFrame(self.main_frame, text="Groupe Up",
                                             padx=10, pady=10)
        self.groupe_up_frame.pack(side="left", expand=True, fill="both")

        self.natixis_intertitres_frame = tk.LabelFrame(self.main_frame,
                                                       text="Natixis "
                                                            "Intertitres",
                                                       padx=10, pady=10)
        self.natixis_intertitres_frame.pack(side="left", expand=True,
                                            fill="both")

        # Create the ticket buttons
        self.sodexo_buttons = self.create_ticket_buttons(
            self.sodexo_frame,
            list(self.ticket_data["Sodexo"].keys())
        )

        self.edenred_buttons = self.create_ticket_buttons(
            self.edenred_frame,
            list(self.ticket_data["Edenred"].keys())
        )

        self.up_buttons = self.create_ticket_buttons(
            self.groupe_up_frame,
            list(self.ticket_data["Groupe Up"].keys())
        )

        self.cheque_dejeuner_buttons = self.create_ticket_buttons(
            self.natixis_intertitres_frame,
            list(self.ticket_data["Natixis Intertitres"].keys())
        )
        # self.load_data = restore_data

    def create_report_window(self):
        # Create report string
        report_string = produce_report(self.ticket_data)

        # Create the report window
        new_window = tk.Toplevel()
        new_window.title("Report")

        # Create the text area
        text_area = scrolledtext.ScrolledText(new_window, height=20,
                                              wrap=tk.WORD)
        text_area.insert(tk.END, report_string)
        text_area.config(state=tk.DISABLED)
        text_area.pack()

        # Create the copy button.
        copy_button = tk.Button(
            new_window,
            text="Copy",
            command=partial(
                pyperclip.copy,
                text_area.get("1.0", "end-1c")
            )
        )
        copy_button.pack()

        # Launch this window's main event loop.
        new_window.mainloop()

    def run(self):
        self.master.mainloop()

    def save_data(self):
        my_filename = datetime.now().strftime("%Y_%m_%d-%H_%M_%S") + ".json"
        save_data(my_filename, self.ticket_data)

    def load_data(self):
        self.ticket_data = restore_data(
            "2023_05_03-21_40_56.json",
            reset_counts=False
        )

    def load_reset_data(self):
        self.ticket_data = restore_data(
            "2023_05_03-21_40_56.json",
            reset_counts=True
        )

    def create_ticket_buttons(self, frame, denominations):
        buttons = {}
        for denomination in denominations:
            button = tk.Button(frame, text=f"{denomination} €",
                               command=partial(self.count_ticket, frame['text'],
                                               denomination))
            button.pack(side="top", pady=5)
            buttons[denomination] = button
        return buttons

    def count_ticket(self, company, denomination):
        """This function is called when a ticket button is pressed.
        It calls the count_tickets() function to update the ticket_data
        dictionary.

        Args:
            company: The name of the company issuing the ticket.
            denomination: The value (money) of the ticket.
        """
        count_tickets(company, denomination, 1, self.ticket_data)


app = TicketCounterApp()
app.run()
