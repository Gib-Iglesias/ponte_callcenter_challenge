import os
import csv
import shutil
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from datetime import datetime


class ManagementAgentsAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_data_dir = 'data_tests'
        self.test_results_dir = 'results_tests'

        if os.path.exists(self.test_results_dir):
            shutil.rmtree(self.test_results_dir)
        os.makedirs(self.test_results_dir, exist_ok=True)

        os.makedirs(self.test_data_dir, exist_ok=True)
        with open(os.path.join(self.test_data_dir, 'tickets_test.csv'), 'w', newline='') as f:
            f.write("id,fecha_creacion,prioridad\n")
            f.write("1,2024-01-01 09:00,8\n")
            f.write("2,2024-01-15 14:30,3\n")
            f.write("3,2024-01-03 11:15,9\n")
            f.write("4,2024-01-16 13:00,3\n")
            f.write("5,2024-01-04 17:45,4\n")
            f.write("6,2024-01-17 10:10,5\n")
            f.write("7,2024-01-05 12:00,8\n")
            f.write("8,2024-01-18 18:20,8\n")
            f.write("9,2024-01-06 11:10,6\n")
            f.write("10,2024-01-19 15:30,5\n")
            f.write("11,2024-01-07 13:45,3\n")
            f.write("12,2024-01-20 14:15,2\n")
            f.write("13,2024-01-08 08:00,4\n")
            f.write("14,2024-01-09 07:45,5\n")
            f.write("15,2024-01-10 10:00,5\n")

        self.read_tickets_patch = patch('call_center.views.read_tickets_from_csv', self.mock_read_tickets_from_csv)
        self.read_tickets_mock = self.read_tickets_patch.start()


    def tearDown(self):
        if os.path.exists(self.test_results_dir):
            shutil.rmtree(self.test_results_dir)

        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        self.read_tickets_patch.stop()


    def mock_read_tickets_from_csv(self, csv_filepath):
        tickets_test = []
        with open(os.path.join(self.test_data_dir, 'tickets_test.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tickets_test.append({
                    'ticket_id': int(row['id']),
                    'fecha_creacion': datetime.strptime(row['fecha_creacion'], '%Y-%m-%d %H:%M'),
                    'prioridad': int(row['prioridad'])
                })
        return tickets_test


    def test_management_agents_endpoint_invalid_agent_number(self):
        url = reverse('call_center:management_agents')

        response = self.client.get(url, {'number_of_agents': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

        response = self.client.get(url, {'number_of_agents': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())


    def test_management_agents_endpoint_no_tickets(self):
        with patch('call_center.views.read_tickets_from_csv', return_value=[]) as mock_read:
            url = reverse('call_center:management_agents')
            response = self.client.get(url, {'number_of_agents': 10})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('message', response.json())
            self.assertEqual(response.json()['message'], 'No tickets were found to process')
            mock_read.assert_called_once_with(os.path.join(self.test_data_dir, 'tickets_test.csv'))


    def test_management_agents_endpoint_multiple_agents(self):
        agent_numbers = [6, 8, 10]
        for num_agents in agent_numbers:
            url = reverse('call_center:management_agents')
            response = self.client.get(url, {'number_of_agents': num_agents})

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('message', response.json())
            self.assertIn(str(num_agents), response.json()['message'])

            results_files = [
                f for f in os.listdir(self.test_results_dir)
                if f.startswith('agents_results_num_') and f'_{num_agents}_' in f and f.endswith('.csv')
            ]
            self.assertEqual(len(results_files), 1, f"The expected result file was not found for {num_agents} agents")

            filepath = os.path.join(self.test_results_dir, results_files[0])
            with open(filepath, 'r') as f:
                lines = f.readlines()
                self.assertGreater(len(lines), 1)
