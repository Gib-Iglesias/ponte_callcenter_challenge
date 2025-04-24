import csv
import time
import random
from threading import Thread, Lock
from rest_framework.response import Response
from rest_framework import status
from call_center.utils import read_tickets_from_csv
from datetime import datetime
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter


# Lock para asegurar la escritura segura en el archivo de resultados
results_lock = Lock()


class Agent(Thread):
    def __init__(self, agent_id, ticket_queue, results_file):
        super().__init__()
        self.agent_id = agent_id
        self.ticket_queue = ticket_queue
        self.results_file = results_file

    def run(self):
        while True:
            try:
                ticket = self.ticket_queue.pop(0)
                assignment_time = datetime.now()
                # Manejo del tiempo de atención
                processing_time = random.uniform(2, 3)
                time.sleep(processing_time)
                completion_time = datetime.now()

                with results_lock:
                    writer = csv.writer(self.results_file)
                    writer.writerow([
                        ticket['ticket_id'],
                        ticket['fecha_creacion'].strftime('%Y-%m-%d %H:%M'),
                        ticket['prioridad'],
                        self.agent_id,
                        assignment_time.strftime('%H:%M:%S'),
                        completion_time.strftime('%H:%M:%S')
                    ])

                print(f"Agente {self.agent_id} atendió el ticket {ticket['ticket_id']}")
            except IndexError:
                # No más tickets en la cola
                break


@extend_schema(parameters=[
    OpenApiParameter(name='numero_de_agentes', type=int, location='query', description='Número de agentes disponibles para gestionar tickets'),
])
@api_view(['GET'])
def management_agents_view(request):
    num_agents_str = request.GET.get('numero_de_agentes')
    if not num_agents_str or not num_agents_str.isdigit():
        return Response({'error': 'El parámetro "numero_de_agentes" es requerido y debe ser un número entero.'}, status=status.HTTP_400_BAD_REQUEST)
    num_agents = int(num_agents_str)

    try:
        tickets = read_tickets_from_csv('data/tickets_dataset.csv')
        if not tickets:
            return Response({'message': 'No se encontraron tickets a procesar'}, status=status.HTTP_200_OK)

        # Ordenar los tickets por prioridad
        sorted_tickets = sorted(tickets, key=lambda x: x['prioridad'], reverse=True)
        # Crear una cola de tickets
        ticket_queue = list(sorted_tickets)

        agents = []
        with open('results/agents_results.csv', 'w', newline='') as results_csvfile:
            writer = csv.writer(results_csvfile)
            writer.writerow(['id', 'fecha_creacion', 'prioridad', 'agente', 'fecha_asignacion', 'fecha_resolucion'])

            for i in range(num_agents):
                agent = Agent(i + 1, ticket_queue, results_csvfile)
                agents.append(agent)
                agent.start()

            for agent in agents:
                agent.join()

        return Response({'message': f'Gestión completada con {num_agents} agentes. Resultados guardados en agents_results.csv'}, status=status.HTTP_200_OK)

    except FileNotFoundError:
        return Response({'error': 'El archivo tickets_dataset.csv no fue encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Ocurrió un error durante la gestión de tickets: {e}, Consulte a un asesor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
