# Currency Converter API
This application was built for educational purposes and is not intended for production use.

## Overview
This is a subscription based currency converter API. 

### Motives
The main reason for creating this application was to learn new technologies 
and build a real-world application from scratch. 

Main features:
- FastAPI framework
- async HTTP requests using `httpx` library
- caching with async Redis using `aioredis` library
- database operations using SQLite and `sqlalchemy`
- authentication via request headers
- use of `pydantic` for data models and validation
- custom error handling
- credit deduction with middleware functions
- unified API call response model

### Currency converter
Currency rates are provided by an external API https://www.fastforex.io/. 

Supported operations are:
- Fetch all supported currencies
- Fetch a single exchange rate
- Fetch all exchange rates
- Currency conversion (including historical data)

Each currency conversion operation is charged 1 credit.

### Subscriptions
The API offers several subscription plans:

| Subscription plan  | Credits | Concurrency | 
| ------------- | ------------- | ------------- |
| Basic  | 100  | 1 |
| Hobby  | 500  | 3 |
| Pro  | 10.000  | 10 |
| Enterprise  | 50.000  | 15 |

Each user can subscribe to the service by providing a valid email address. 
After successful subscription the user receives an API key that is required
to use the currency converter endpoints. API also provides several internal 
endpoints for subscription administration purposes.

### Authentication
Only subscribed users can use the API. To authenticate incoming requests, we 
check the `api_key` header.
 
## Get started
To run the API you will need an API key from `https://www.fastforex.io/`.
Create the `.env` file (use the `.env.dist` for reference) and add the 
Fast Forex API key.

### Dependencies
Dependency management is handled using `requirements.txt` file. 

### Docker setup

1. Build a docker image: `docker build -t currency_converter_api .`
2. Start redis server with : `docker-compose up`
3. Create a running container: `docker run -p 80:80 currency_converter_api`

### Local setup

1. Install dependencies from `requirements.txt` file
2. Run the app: `uvicorn currency_converter_api:app --reload`

## Documentation
Once the application is up and running, you can access FastAPI automatic docs 
at `/docs` endpoint.

### Currency converter endpoints

| Method | Endpoint  | Description |
| ------------- | ------------- | ------------- |
| GET | /currencies  | fetch a list of all supported currencies |
| GET | /convert  | convert one currency into another currency |
| GET | /fetch_one  | fetch a single exchange rate |
| GET | /fetch_all  | fetch all available exchange rates |
| GET | /historical  | get historical exchange rates|

### Admin endpoints

| Method | Endpoint  | Description |
| ------------- | ------------- | ------------- |
| POST | /subscribe  | create a new subscription |
| GET | /all_users  | list all signed-up users |

## Status codes

| Status code  | Description |
| ------------- | ------------- |
| 200  | success |
| 400  | bad request, please check your request |
| 401  | user unauthorized, check your API key |
| 424  | external dependency failed |
| 429  | rate limit violation |
| 500  | internal server error, application failed |

## Examples

_TODO: provide CURL examples - add CURL command + response in JSON format_