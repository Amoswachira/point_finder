# Django API for Closest Points

This is a Django application that provides an API to find the closest points on a grid and store them in a database and an Admin dashboard to view the points.

## Prerequisites

- Python 3.9 or higher
- Pip package manager


## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Amoswachira/point_finder.git

   ```

2. Install project dependencies:

    ```bash
        pip install -r requirements.txt
    ```
3. Run database migrations:
    ```bash
    python manage.py migrate
    ```
4. Start the Django development server:
    ```bash
    python manage.py runserver
    ```
5. You will be prompted to log in to the admin interface. Create a superuser account if you haven't     already:
    ```bash
    python manage.py createsuperuser
    ```
 Follow the prompts to enter a username, email (optional), and password.


The API will be accessible at http://localhost:8000.

    Endpoints
    POST /api/points/

    Description: Create a new set of points and find the closest points.
    Request Body: JSON object with the following format:

        {
        "coordinates": "2,2;-1,30;20,11;4,5"
        }
    
    Response: JSON object with a success message if the points are saved successfully.

    GET /api/points/

    Description: Retrieve all points stored in the database.
    Response: JSON object containing the list of points.

6. The ADMIN Interface will be accessible at http://localhost:8000/admin/

7. To run tests run:
    ```bash
    python manage.py test point_api.tests
    ```


