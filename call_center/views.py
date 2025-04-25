import os
import sys
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

                print(f"Agent_Id: {self.agent_id} attended the Ticket_Id: {ticket['ticket_id']}")
            except IndexError:
                break


@extend_schema(parameters=[
    OpenApiParameter(name='number_of_agents', type=int, location='query', description='Number of agents available to manage tickets'),
])
@api_view(['GET'])
def management_agents_view(request):
    num_agents_str = request.GET.get('number_of_agents')
    if not num_agents_str or not num_agents_str.isdigit():
        return Response({'error': 'The "number_of_agents" parameter is required and must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
    num_agents = int(num_agents_str)

    is_testing = any('test' in arg for arg in sys.argv)
    results_dir = 'results_tests' if is_testing else 'results'
    data_file = 'data_tests/tickets_test.csv' if is_testing else 'data/tickets_dataset.csv'
    print('Iteration Test')

    try:
        tickets = read_tickets_from_csv(data_file)
        if not tickets:
            return Response({'message': 'No tickets were found to process'}, status=status.HTTP_200_OK)

        sorted_tickets = sorted(tickets, key=lambda x: x['prioridad'], reverse=True)

        ticket_queue = list(sorted_tickets)

        now = datetime.now().strftime("%Y%m%d_%H%M")
        results_filename = f'agents_results_num_{num_agents}_{now}.csv'
        results_filepath = os.path.join(results_dir, results_filename)

        agents = []
        with open(results_filepath, 'w', newline='') as results_csvfile:
            writer = csv.writer(results_csvfile)
            writer.writerow(['id', 'fecha_creacion', 'prioridad', 'agente', 'fecha_asignacion', 'fecha_resolucion'])

            for i in range(num_agents):
                agent = Agent(i + 1, ticket_queue, results_csvfile)
                agents.append(agent)
                agent.start()

            for agent in agents:
                agent.join()

        return Response({'message': f'Management completed with {num_agents} agents. Results saved in {os.path.join(results_dir, results_filename)}'}, status=status.HTTP_201_CREATED)

    except FileNotFoundError:
        return Response({'error': f'File: {data_file} not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'An error occurred during ticket management: {e}. Consult an advisor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
