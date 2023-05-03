import json
from datetime import datetime


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


if __name__ == "__main__":
    # Init
    my_ticket_data = {}

    # Counting tickets
    count_tickets("sodexo", 1.43, 102, my_ticket_data)
    count_tickets("sodexo", 3.25, 45, my_ticket_data)
    count_tickets("sodexo", 5.6, 88, my_ticket_data)
    count_tickets("sodexo", 9.48, 34, my_ticket_data)
    count_tickets("Groupe Up", 2.28, 1, my_ticket_data)
    count_tickets("Groupe Up", 2.28, 101, my_ticket_data)
    count_tickets("Groupe Up", 3.37, 2, my_ticket_data)
    count_tickets("Groupe Up", 3.37, 43, my_ticket_data)
    count_tickets("Groupe Up", 10.02, 34, my_ticket_data)
    count_tickets("Edenred", 2.00, 5, my_ticket_data)
    count_tickets("Edenred", 3.87, 80, my_ticket_data)
    count_tickets("Edenred", 3.87, 1, my_ticket_data)
    count_tickets("Edenred", 6.2, 88, my_ticket_data)
    count_tickets("Natixis Intertitres", 5.00, 121, my_ticket_data)
    count_tickets("Natixis Intertitres", 7.75, 47, my_ticket_data)

    # Report
    report = produce_report(my_ticket_data)
    print(report)
