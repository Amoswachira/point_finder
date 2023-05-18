from django.test import TestCase, Client
from .models import Point


class PointAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_points(self):
        payload = {
            'coordinates': '2,2;-1,30;20,11;4,5'
        }
        response = self.client.post('/api/points/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Points saved successfully.'})

    def test_create_points_missing_coordinates(self):
        payload = {
            'coordinates': ''
        }
        response = self.client.post('/api/points/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'No coordinates provided.'})

    def test_create_points_invalid_format(self):
        payload = {
            'coordinates': '2,2;-1,30;20,11;4'
        }
        response = self.client.post('/api/points/', data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid coordinates format.'})

    def test_retrieve_points(self):
        Point.objects.create(coordinates='2,2;4,5', closest_points='2,2;4,5')
        Point.objects.create(coordinates='10,10;15,20', closest_points='10,10;15,20')

        response = self.client.get('/api/points/all/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data['points']), 2)
        self.assertEqual(data['points'][0]['coordinates'], '2,2;4,5')
        self.assertEqual(data['points'][0]['closest_points'], '2,2;4,5')
        self.assertEqual(data['points'][1]['coordinates'], '10,10;15,20')
        self.assertEqual(data['points'][1]['closest_points'], '10,10;15,20')
