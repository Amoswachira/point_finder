from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Point
import json

@csrf_exempt
def point_api(request):
    try:
        if request.method == 'POST':
            # Retrieve the JSON payload from the request body
            data = json.loads(request.body)
            coordinates = data.get('coordinates')

            # Validate if coordinates are provided
            if not coordinates:
                return JsonResponse({'error': 'No coordinates provided.'}, status=400)

            # Validate the format of coordinates
            valid_format = all(',' in coord for coord in coordinates.split(';'))
            if not valid_format:
                return JsonResponse({'error': 'Invalid coordinates format.'}, status=400)

            # Find closest points and save the data to the database
            closest_points = find_closest_points(coordinates)
            point = Point(coordinates=coordinates, closest_points=closest_points)
            point.save()

            # Return success response
            return JsonResponse({'message': 'Points saved successfully.'})

        elif request.method == 'GET':
            # Retrieve all points from the database
            points = Point.objects.all()
            data = []
            for point in points:
                data.append({
                    'coordinates': point.coordinates,
                    'closest_points': point.closest_points
                })

            # Return the points data in the response
            return JsonResponse({'points': data})

    except json.JSONDecodeError:
        # Handle JSON decoding error in case of an invalid payload
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    except Exception as e:
        # Log the exception for debugging purposes
        # logger.error(str(e))

        # Return an error response for any other exceptions (500 Internal Server Error)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@csrf_exempt
def get_points(request):
    if request.method == 'GET':
        # Retrieve all points from the database
        points = Point.objects.all()
        data = []
        for point in points:
            data.append({
                'coordinates': point.coordinates,
                'closest_points': point.closest_points
            })

        # Return the points data in the response
        return JsonResponse({'points': data})


def find_closest_points(coordinates):
    if not coordinates:
        return ''

    # Split and parse the coordinates into a list of tuples
    points = [tuple(map(int, coord.split(','))) for coord in coordinates.split(';') if coord]
    closest_points = []
    min_distance = float('inf')

    # Find the closest points by calculating distances between all pairs of points
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = calculate_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_points = [points[i], points[j]]

    # Return the closest points as a semicolon separated string
    return ';'.join([','.join(map(str, point)) for point in closest_points])


def calculate_distance(point1, point2):
    # Calculate the Euclidean distance between two points
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
