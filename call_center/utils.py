import csv
from datetime import datetime


def read_tickets_from_csv(csv_filepath):
    """
    Reads ticket data from a CSV file in the format specified for the input
    Args:
        csv_filepath (str): Path to the CSV file
    Returns:
        list: List of dictionaries, where each dictionary represents a ticket
    """
    tickets = []
    try:
        with open(csv_filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    ticket_id = int(row['id'])
                    creation_date = datetime.strptime(row['fecha_creacion'], '%Y-%m-%d %H:%M')
                    priority = int(row['prioridad'])
                    tickets.append({
                        'ticket_id': ticket_id,
                        'fecha_creacion': creation_date,
                        'prioridad': priority
                    })
                except ValueError as e:
                    print(f"Error processing row: {row}. Error: {e}")
                except KeyError as e:
                    print(f"Error: Missing column '{e}' in CSV file")
    except FileNotFoundError:
        print(f"Error: File {csv_filepath} not found")
    return tickets


def assign_ticket_by_priority(tickets, number_agents):
    """
    Distributes tickets among agents based on priority
    Args:
        tickets (list): List of ticket dictionaries (sorted by priority)
        num_agents (int): Number of available agents
    Returns:
        dict: Dictionary where the keys are the agent IDs and the values ​​are lists of assigned tickets
    """
    assignment = {i + 1: [] for i in range(number_agents)}
    agent_index = 0
    for ticket in tickets:
        agent_id = (agent_index % number_agents) + 1
        assignment[agent_id].append(ticket)
        agent_index += 1
    return assignment
