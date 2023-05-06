import json
from datetime import datetime
from typing import Union


def count_tickets(
        company_name: str,
        denomination: float,
        increment: int,
        ticket_data: dict
):
    """This function counts tickets and stores company, denomination and
        number of tickets inside a datastructure.

    Args:
        company_name: The name of the company issuing the ticket.
        denomination: The value (money) of the ticket.
        increment: The number of tickets you actually want to add/remove.
        ticket_data: The datastructure that contains everything:
            - companies
            - denominations
            - number of each ticket.
    """
    if company_name not in ticket_data:
        ticket_data[company_name] = {}
    if denomination not in ticket_data[company_name]:
        ticket_data[company_name][denomination] = 0
    ticket_data[company_name][denomination] += increment


def produce_report(ticket_data: dict):
    """This function produces a report in french calculating a few key values.

    Args:
        ticket_data: The datastructure that contains everything:
            - companies
            - denominations
            - number of each ticket.

    Returns:
        str: The report produced.
    """
    total_tickets = 0
    total_montant = 0
    rapport_par_societe = ""
    for nom_societe, coupures in ticket_data.items():
        total_tickets_societe = 0
        total_montant_societe = 0
        rapport_par_societe += f"{nom_societe}:\n"
        for coupure, compteur in coupures.items():
            total_tickets += compteur
            total_tickets_societe += compteur
            total_montant_societe += coupure * compteur
            total_montant += coupure * compteur
            rapport_par_societe += f"\t{coupure:.2f} euros: {compteur} tickets\n"
        rapport_par_societe += f"\tTotal tickets: {total_tickets_societe}\n"
        rapport_par_societe += f"\tTotal montant: {total_montant_societe:.2f} euros\n\n"
    rapport = f"Rapport de comptage de tickets restaurant:\n\n{rapport_par_societe}"
    rapport += f"Total tickets: {total_tickets}\n"
    rapport += f"Total montant: {total_montant:.2f} euros\n"

    return rapport


def save_data(filename: str, data: Union[str, dict]):
    """This function saves either:
        - the datastructure into a json file.
        - a text report into a text file.

    Args:
        filename (str): The name of the file that will contain the backup.
        data (str/dict): Either the datastructure used to store companies,
            denominations, and the number of each ticket OR a string containing
            the report.
    """
    with open(filename, "w+") as f:
        if isinstance(data, dict):
            json.dump(data, f)
        else:
            f.write(data)


def restore_data(filename: str, reset_counts: bool = False):
    """This function restores the datastructure from a json file.
        As the denomination were previously converted from float
        to string (to fit the JSON RFC - https://stackoverflow.com/a/5527017),
        we convert those denominations back from string to float.

    Args:
        filename:
        reset_counts:
    """

    with open(filename, "r") as f:
        ticket_data = json.load(f)
    if reset_counts:
        for key in list(ticket_data.keys()):
            for k in list(ticket_data[key].keys()):
                ticket_data[key][float(k)] = ticket_data[key].pop(k)
                ticket_data[key][float(k)] = 0
    else:
        for key, value in ticket_data.items():
            ticket_data[key] = {float(k): v for k, v in value.items()}
    return ticket_data


if __name__ == "__main__":
    # Init
    my_ticket_data = {}

    # Load backup
    my_ticket_data = restore_data("2023_05_03-21_40_56.json", reset_counts=True)
    # my_ticket_data = restore_data("2023_05_03-21_40_56.json")

    # # Counting tickets
    # count_tickets("Sodexo", 1.43, 102, my_ticket_data)
    # count_tickets("Sodexo", 3.25, 45, my_ticket_data)
    # count_tickets("Sodexo", 5.6, 88, my_ticket_data)
    # count_tickets("Sodexo", 9.48, 34, my_ticket_data)
    # count_tickets("Groupe Up", 2.28, 1, my_ticket_data)
    # count_tickets("Groupe Up", 2.28, 101, my_ticket_data)
    # count_tickets("Groupe Up", 3.37, 2, my_ticket_data)
    # count_tickets("Groupe Up", 3.37, 43, my_ticket_data)
    # count_tickets("Groupe Up", 10.02, 34, my_ticket_data)
    # count_tickets("Edenred", 2.00, 5, my_ticket_data)
    # count_tickets("Edenred", 3.87, 80, my_ticket_data)
    # count_tickets("Edenred", 3.87, 1, my_ticket_data)
    # count_tickets("Edenred", 6.2, 88, my_ticket_data)
    # count_tickets("Natixis Intertitres", 5.00, 121, my_ticket_data)
    # count_tickets("Natixis Intertitres", 7.75, 47, my_ticket_data)

    # Report
    report = produce_report(my_ticket_data)
    print(report)

    # # Save data
    # my_filename = datetime.now().strftime("%Y_%m_%d-%H_%M_%S") + ".json"
    # save_data(my_filename, my_ticket_data)
