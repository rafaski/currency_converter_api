# Currency Converter API
 
## Overview
A currency Converter API allows you to convert any supported currency and perform the following operations: 
- subscribe users
- get all users info
- get all supported currencies
- convert currencies
- fetch a single currency exchange rate
- fetch all currency exchange rate
- get historical data on currency exchange rates

It uses foreign forex API from fastforex.io to fetch currency data. 
Each user can subscribe to our services by providing a valid email and by choosing a subscription plan which will reflect eventually the number of credits they get to make requests and allowed concurrency levels. Each user will be verified and authenticated prior to making API calls and provided with a unique API key.
To minimize the number of foreign API calls, we will store request JSON responses in redis. Forex API calls will be made only if there is no such key in redis cache. 
Most redis keys have expiration dates due to fluctuating nature of the currency conversion data.

The main reason for creating this application was to show off skills in creating production-ready real-world applications. 
It showcases the following skills and features:
- async API calls with fastapi
- async forex requests with httpx
- async redis forex recall response storage
- SQLite user info storage
- user authentification with request headers
- input validation
- custom error handling
- custom decorators
- routers
- unified response model
 
## Dependencies
- fastapi
- uvicorn
- httpx
- redis
- sqlalchemy
- python-dotenv
 
## Setup with Docker
tbc
 
## Setup
tbc

## Database
Both SQL and No-SQL databases were used for this project. 
To limit the number of API calls on external forex API, we store most of the user request recall results in the in-cache redis database with expiration set to 1h if required.
All user info is stored within the sqlite database, which consists of user email, chosen subscription plan, individual API key, amount of credits to make API calls etc.
 
## Endpoints
user related:
- `/subscribe`: subscribe a new user with an email address. Choose your subscription type. Returns individual API key to make API calls
- `/all_users`: returns a list of all signed-up users
currency conversion:
- `/currencies`: fetch a list of all supported currencies
- `/convert`: convert an amount of one currency into another currency
- `/fetch_one`: fetch a single currency exchange rate, from and to any supported currency
- `/fetch_all`: fetch all available currency rates
- `/historical`: get your historical conversion data
 
**Note**: make sure you're sending a valid `email` and `api_key` in the query params whenever you make a request to the API. 
Each converter endpoint has a dependency on verifying signed-up users. Otherwise, you'll get a `401 UNAUTHORIZED`.
 
## Interactive API docs
You can see the automatic interactive API documentation (provided by Swagger UI). Use `/docs` endpoint to access.

## Testing
Testing the behavior of HTTP requests was performed with the built-in Swagger UI /docs endpoint and Insomnia.

![png](https://github.com/rafaski1/currency_converter_api/blob/main/swagger_ui.PNG?raw=true)

