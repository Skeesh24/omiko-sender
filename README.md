# Omiko Store Web Application - Email sender
## Overview
email sender service for the omiko application architecture. used with the pair of message broker, to access message independently from the server

## Setup
### Requirements
1. python3.11

### Installation

Clone the repository:

```bash
git clone https://github.com/skeesh24/omiko-sender.git
```

### Install dependencies:

```bash
python3.11 -m venv venv && venv/Script/activate && pip install -r requirements.txt
```

## Features
- OAuth 2.0: Processes your application and provides you with a pair of tokens upon registration: an access token and a refresh token.
- REST: The application's API provides a simple HTTP route that implements the REST specification.
- Storage: Data is stored in the postgresql database, and Google's FireStore cloud storage was used in the debugging process.
- Cache: Caching is represented by saving user data to reduce the number of database accesses.
- Password Recovery: There is a way to restore your account through the recovery process implemented by the email sender.
- Message broker: An API and an email sender have been connected via the message broker.
- Proxy Gateway: There is an implementation of the API Gateway pattern that provides a persistent route for the user to access the various microservices.
- Interface Segragation: Throughout the application you can easily replace modules, for example redis cache with Memcached, due to the use of dedicated interfaces and low cohesion of system components.

## Technologies Used
- Python:3.11.5-bookworm
- FastAPI
- SQLAlchemy
- JWT
- Postgres
- FireStore
- Redis
- Memcached
- Docker
  
## Application Deployment

The project was deployed as a Render.com blueprint:
https://

## Running the Software

1. Navigate to the root directory. Execute the software:
```bash
venv/Script/python src/main.py
