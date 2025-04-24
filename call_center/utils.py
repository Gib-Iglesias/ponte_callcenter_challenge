import csv
from datetime import datetime


def read_tickets_from_csv(csv_filepath):
    """
    Lee los datos de los tickets desde un CSV con el formato especificado para el input

    Args:
        csv_filepath (str): ruta al archivo CSV
    Returns:
        list: lista de diccionarios, donde cada diccionario representa un ticket
    """
    tickets = []
    try:
        with open(csv_filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    ticket_id = int(row['id'])
                    fecha_creacion = datetime.strptime(row['fecha_creacion'], '%Y-%m-%d %H:%M')
                    prioridad = int(row['prioridad'])
                    tickets.append({
                        'ticket_id': ticket_id,
                        'fecha_creacion': fecha_creacion,
                        'prioridad': prioridad
                    })
                except ValueError as e:
                    print(f"Error al procesar la fila: {row}. Error: {e}")
                except KeyError as e:
                    print(f"Error: Falta la columna '{e}' en el archivo CSV.")
    except FileNotFoundError:
        print(f"Error: El archivo {csv_filepath} no fue encontrado.")
    return tickets


def assign_ticket_by_priority(tickets, num_agents):
    """
    Distribuye los tickets entre los agentes basándose en la prioridad

    Args:
        tickets (list): lista de diccionarios de tickets (ordenados por prioridad).
        num_agents (int): número de agentes disponibles.
    Returns:
        dict: diccionario donde las claves son los IDs de los agentes y los valores son listas de tickets asignados.
    """
    assignment = {i + 1: [] for i in range(num_agents)}
    agent_index = 0
    for ticket in tickets:
        agent_id = (agent_index % num_agents) + 1
        assignment[agent_id].append(ticket)
        agent_index += 1
    return assignment
