import csv
from datetime import datetime


def read_tickets_from_csv(csv_filepath):
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
    assignment = {i + 1: [] for i in range(number_agents)}
    agent_index = 0
    for ticket in tickets:
        agent_id = (agent_index % number_agents) + 1
        assignment[agent_id].append(ticket)
        agent_index += 1
    return assignment
