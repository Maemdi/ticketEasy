import tkinter as tk
from functools import partial
from datetime import datetime
import tkinter.scrolledtext as scrolledtext
import pyperclip

from src.frontend.add_company_window import AddCompanyWindow
from src.frontend.add_denomination_window import AddDenominationWindow
from src.backend.core import (
    count_tickets,
    produce_report,
    save_data,
    restore_data
)


class TicketCounterApp:
    def __init__(self, master=None):
        if not master:
            master = tk.Tk()
        self.master = master
        master.title("Ticket'Easy")
        master.geometry("800x600")

        # Initialize the ticket data
        self.ticket_data = restore_data("real_data.json", True)

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

        self.remove_button = tk.Button(
            self.header_frame,
            text="Remove",
            command=self.remove_company_frames_and_buttons
        )

        self.remove_button.pack(side="left", padx=5)

        self.add_company_button = tk.Button(self.header_frame,
                                            text="Add Company",
                                            command=self.add_company)

        self.add_company_button.pack(side="left", padx=5)

        self.company_frames = {}
        self.company_buttons = {}

        # Create the company frames
        self.load_company_frames_and_buttons()

    def load_company_frames_and_buttons(self):

        # Create the company frames
        for company in self.ticket_data.keys():
            # Create frame corresponding to the company
            self.company_frames[company] = tk.LabelFrame(
                self.main_frame, text=company, padx=10, pady=10)
            self.company_frames[company].pack(side="left", expand=True,
                                              fill="both")

            # Create the ticket buttons corresponding to the company
            self.company_buttons[company] = self.create_ticket_buttons(
                self.company_frames[company],
                list(self.ticket_data[company].keys())
            )

            # Create the button to add a denomination to the company
            button = tk.Button(
                self.company_frames[company],
                text=f"Add a denomination",
                command=partial(self.add_denomination, company),
                fg="Black", bg="GreenYellow")
            button.pack(side="top", padx=5, pady=5)

    def remove_company_frames_and_buttons(self):
        # Remove buttons
        for one_company_buttons in self.company_buttons.values():
            for button_list in one_company_buttons.values():
                for button in button_list:
                    button.destroy()
        # Remove frames
        for frame in self.company_frames.values():
            frame.destroy()

    def add_denomination(self, company_name: str):
        denomination_window = AddDenominationWindow(company_name)
        denomination_window.wait_window()
        denomination = denomination_window.result
        if denomination is not None:
            print("Value entered:", denomination)
        else:
            print("Window closed or Cancel button pressed")
            return

        # Add denomination in the data structure
        if denomination not in self.ticket_data[company_name]:
            self.ticket_data[company_name][denomination] = 0

        # Refresh gui (frames and buttons)
        self.remove_company_frames_and_buttons()
        self.load_company_frames_and_buttons()

    def add_company(self):
        add_company_window = AddCompanyWindow()
        add_company_window.wait_window()
        company_name = add_company_window.result
        if company_name is not None:
            print("Value entered:", company_name)
        else:
            print("Window closed or Cancel button pressed")
            return

        # Add company in the data structure
        if company_name not in self.ticket_data:
            self.ticket_data[company_name] = {}

        # Refresh gui (frames and buttons)
        self.remove_company_frames_and_buttons()
        self.load_company_frames_and_buttons()

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

        # Create the footer frame
        footer_frame = tk.Frame(new_window)
        footer_frame.pack(side="bottom", fill="x")

        # Create the copy button.
        copy_button = tk.Button(
            footer_frame,
            text="Copy",
            command=partial(
                pyperclip.copy,
                text_area.get("1.0", "end-1c")
            )
        )
        copy_button.pack(side="left")

        # Create the save button.
        save_button = tk.Button(
            footer_frame,
            text="Save",
            command=partial(
                self.save_data,
                text_area.get("1.0", "end-1c")
            )
        )
        save_button.pack(side="left")

        # Launch this window's main event loop.
        new_window.mainloop()

    def run(self):
        self.master.mainloop()

    def save_data(self, input_data=None):
        file_ext = ".txt"
        if not input_data:
            input_data = self.ticket_data
            file_ext = ".json"
        my_filename = datetime.now().strftime("%Y_%m_%d-%H_%M_%S") + file_ext
        save_data(my_filename, input_data)

    def load_data(self):
        self.ticket_data = restore_data(
            "real_data.json",
            reset_counts=False
        )
        self.remove_company_frames_and_buttons()
        # Re-create the company frames
        self.load_company_frames_and_buttons()

    def load_reset_data(self):
        self.ticket_data = restore_data(
            "real_data.json",
            reset_counts=True
        )
        self.remove_company_frames_and_buttons()
        # Re-create the company frames
        self.load_company_frames_and_buttons()

    def create_ticket_buttons(self, frame, denominations):
        buttons = {}
        for denomination in sorted(denominations):
            # We build a subframe to own the minus button and the
            # denomination button
            buttons_subframe = tk.Frame(frame)
            buttons_subframe.pack(side="top", pady=5)

            button_minus = tk.Button(buttons_subframe, text=f" - ",
                                     command=partial(self.count_ticket,
                                                     frame['text'],
                                                     -denomination),
                                     fg="Black", bg="DarkOrange")
            button_minus.pack(side="left", padx=5, pady=5)
            button = tk.Button(buttons_subframe, text=f"{denomination} €",
                               command=partial(self.count_ticket, frame['text'],
                                               denomination))
            button.pack(side="left", padx=5, pady=5)

            # We just add the buttons and not the subframes as even if we
            # need to remove the elements, it seems there is no need to
            # remove the subframes
            buttons[denomination] = [button, button_minus]
        return buttons

    def count_ticket(self, company, denomination):
        """This function is called when a ticket button is pressed.
        It calls the count_tickets() function to update the ticket_data
        dictionary.

        Args:
            company: The name of the company issuing the ticket.
            denomination: The value (money) of the ticket.
        """
        if denomination > 0:
            count_tickets(company, denomination, 1, self.ticket_data)
        else:
            count_tickets(company, abs(denomination), -1, self.ticket_data)
