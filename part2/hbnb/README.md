![images (1)](https://github.com/user-attachments/assets/85e63b62-e403-4953-8fd7-21b3a47dd634)

## Description

This part of HBnB consists of setting up the initial HBnB project, with a clean separation of concerns, including three layers: Presentation, Business Logic, and Persistence.

## Projet Structure
```
hbnb/
├── app/
│   ├── __init__.py                  # Initializes the Flask app
│   ├── api/
│   │   ├── __init__.py              # API package initializer
│   │   ├── v1/
│   │       ├── __init__.py          # API v1 initializer
│   │       ├── users.py             # Users API endpoint
│   │       ├── places.py            # Places API endpoint
│   │       ├── reviews.py           # Reviews API endpoint
│   │       ├── amenities.py         # Amenities API endpoint
│   ├── models/
│   │   ├── __init__.py              # Models package initializer
│   │   ├── user.py                  # User model definition
│   │   ├── place.py                 # Place model definition
│   │   ├── review.py                # Review model definition
│   │   ├── amenity.py               # Amenity model definition
│   ├── services/
│   │   ├── __init__.py              # Services package initializer
│   │   ├── facade.py                # Facade pattern implementation
│   ├── persistence/
│   │   ├── __init__.py              # Persistence package initializer
│   │   ├── repository.py            # In-memory repository
├── run.py                           # Flask application entry point
├── config.py                        # Application configuration
├── requirements.txt                 # List of dependencies
├── README.md                        # Project documentation

```
## Explanation 

- app/: Core application folder, containing the Flask setup, API endpoints, models, services (Facade pattern), and persistence logic.

- api/: Contains the API endpoint implementations, currently grouped under ``v1/``.

- models/: Defines the business logic classes for the entities like ``User``, ``Place``, ``Review``, and ``Amenity``.

- services/: Implements the Facade pattern, acting as an intermediary between the API, models, and persistence layer.

- persistence/: In-memory repository to handle data storage and validation. This will be replaced by a database solution in future phases.

- run.py: The entry point to start the Flask web application.

- config.py: Configures application settings such as environment-specific configurations.

- requirements.txt: Lists all the necessary Python dependencies for the project.


## Project Layers

###  Presentation Layer (API)
- The API endpoints are defined in ``app/api/v1/``. Currently, placeholder files are created for users, places, reviews, and amenities.

### Business Logic Layer (Models)
- Business entities such as ``User``, ``Place``, ``Review``, and ``Amenity`` are defined in ``app/models/``.

### Persistence Layer (In-Memory Repository)

- The persistence layer is set up to use an in-memory repository that handles storage and validation of objects. The ``InMemoryRepository`` in ``app/persistence/repository.py`` provides methods for adding, retrieving, updating, and deleting objects.

### Facade Pattern

- The Facade pattern is implemented in ``app/services/facade.py``, where ``HBnBFacade`` manages communication between the API, models, and persistence layer.  API calls will use this facade to abstract the complexity of multiple layers.

### Configuration

- Application settings are managed in ``config.py``. This file defines configurations such as the secret key and debug mode.

### Requirements

-  will list all the Python packages needed for the project.

## Setup and instal Required Packages

### Clone the repository and change directory
```
git clone https://github.com/S1even/holbertonschool-hbnb

cd holbertonschool-hbnb
```

### In the ``requirements.txt`` file, list the Python packages needed for the project:

```
flask
flask-restx
```

### Install the dependencies using:

```
pip install -r requirements.txt
```

###  Test the Initial Setup
```
python run.py
```
- The application will be accessible at ``http://127.0.0.1:5000/``

## Authors

- [Dylan](https://github.com/Bruqui)
- [Steven](https://github.com/S1even)
