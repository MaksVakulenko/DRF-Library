# Library API 📚

Welcome Library! Here you can borrow books to your liking and enjoy a vast collection of literature. Whether you love fiction, non-fiction, or research materials, our library is here to serve you.

## Features of our service

- JWT Authentication
- Email verification
- Telegram bot
- Online payment for your borrowing
- Telegram bot to receive notifications about borrowing

---

## Endpoints available for all users (anonymous, authenticated, admins)

### Authors

`GET /api/library/authors/` - Allows to see all authors of books in our library.

Response example:

```json
[
  {
    "id": 1,
    "first_name": "George",
    "last_name": "Orwell"
  },
  {
    "id": 2,
    "first_name": "Ernest",
    "last_name": "Hemingway"
  }
]
```

`GET /api/library/authors/<int:pk>` - Allows to retrieve information about concrete author.

Response example:

```json
  {
    "id": 1,
    "first_name": "George",
    "last_name": "Orwell"
  }
```

---

### Books

`GET /api/library/books/` - Allows to see all books available in library and price of borrowing.

Response example:

```json
[
  {
    "id": 1,
    "authors": [
      "J.K. Rowling"
    ],
    "title": "Harry Potter and the Sorcerer's Stone",
    "inventory": 10,
    "daily_fee": "5.00"
  },
  {
    "id": 2,
    "authors": [
      "George Orwell"
    ],
    "title": "1984",
    "inventory": 8,
    "daily_fee": "4.00"
  }

]
```

`GET /api/library/books/<int:pk>` - Allows to see all information about specific book.

Response example:

```json

  {
    "id": 1,
    "authors": [
      "J.K. Rowling"
    ],
    "title": "Harry Potter and the Sorcerer's Stone",
    "inventory": 10,
    "daily_fee": "5.00"
  }

```

#### Filtering for books:

`GET /api/library/books/?ordering=id` - Allows order books by id in ascending order.

`GET /api/library/books/?ordering=-id` - Allows order books by id in descending order.

`GET /api/library/books/?ordering=title` - Allows order books by title in ascending order.

`GET /api/library/books/?ordering=-title` - Allows order books by title in descending order.

`GET /api/library/books/?ordering=primary_author_first_name` - Allows order books by author's first name in ascending order.

`GET /api/library/books/?ordering=-primary_author_first_name` - Allows order books by author's first name in descending order.

`GET /api/library/books/?ordering=primary_author_last_name` - Allows order books by author's last name in ascending order.

`GET /api/library/books/?ordering=-primary_author_last_name` - Allows order books by author's last name in descending order.

#### Searching for books:

`GET /api/library/books/?search=1984` - Searching book by title.

`GET /api/library/books/?search=George` - Searching book by author's first name.

`GET /api/library/books/?search=Orwell` - Searching book by author's last name.

---

### Registration

`POST /api/user/register/` - Allows to sing up in our service and then borrow books.

In body of request you should provide such fields:

```json
{
  "email": "user@example.com", /* Required field */
  "first_name": "string", /* Optional field */
  "last_name": "string", /* Optional field */
  "password": "stringst" /* Required field */
}
```

--- 
## Endpoints available for authenticated users (authenticated, admins)

As was described above, we enabled JWT authentication in our service. If you signed up in our service, you can sign in here by obtaining a pair of access and refresh tokens to be able to work with our service.

For better experience we created our own header naming like `Authorize`. To use in browsable api, Postman or Swagger documentation, make sure add prefix `Bearer` before value of access token. For adding header in browser, you can use extension [ModHeader](https://modheader.com/).

Obtain a pair of tokens you can using `POST /api/user/token/`. Make sure provide in body your credentials (email and password).

Response example: 

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDk5Njc3MiwiaWF0IjoxNzQwOTEwMzcyLCJqdGkiOiIwZmVjNDEyOWY4ZmQ0NmUyYmI4MmE5Y2Q4MjYxMmE0MyIsInVzZXJfaWQiOjF9.o9O4nkPuwHtjfJocvxSJTJ2YBhYy7P8FROUYYqwMmN4",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDk0MzcyLCJpYXQiOjE3NDA5MTAzNzIsImp0aSI6IjYyMDRhMTU3MWYwZDQ1YzdiYzJhZTYyZjJiMmEyOTRhIiwidXNlcl9pZCI6MX0.oDjAedU9d1iG5IoUJqrjroLM2DoqMZ7WFTt2felutv8"
}
```

After obtaining this pair of token, you can refresh access token using refresh token. To do it, use this endpoint `POST /api/user/token/refresh/` and make sure provide value of refresh token in body of request.

Response example:

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDk0NTUwLCJpYXQiOjE3NDA5MTAzNzIsImp0aSI6IjM0ZGI2M2M2N2U5ZDQzNmJiZjhiYmMyZDFlYzM5NGFkIiwidXNlcl9pZCI6MX0.8xADPrM3xJW4Pj8Gu4pa5FkzKWj2uxvN3gd29ylYXKM"
}
```

Also, you can verify your tokens via `POST /api/user/token/verify/`. Make sure provide in body of request value of token.

Response example in success:

```json
{}
```
Response example in failure:

```json
{
    "detail": "Token is invalid",
    "code": "token_not_valid"
}
```

To have access to endpoints as authenticated user:

##### In browser use ModHeader:

![mod_header_settings.png](images/mod_header_settings.png)

1) Add header `Authorize`
2) Enable it via checkpoint.
3) Provide value of access token like this: `Bearer access_token_value`.

##### In Postman:

![postman_settings.png](images/postman_settings.png)

1) Go to Headers tab.
2) Add header `Authorize` in key column. It will automatically enable it.
3) Provide value of access token like this: `Bearer access_token_value`. 

### Work with user's profile:

`GET /api/user/me/` - Allows users to see information about their own profile.

Response example:

```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string"
}
```

`PUT /api/user/me/` - Allows users to edit their profile. (Values should be provided for all fields.)

`PATCH /api/user/me/` - Allows users to edit their profile partly. (Users can edit some specific values only or whole info.)

---

### Book borrowing:

`GET /api/library/borrowings/` - here users can see list of all borrowings they did.

Response example:

```json
[
    {
        "id": 2,
        "borrow_date": "2025-03-01",
        "expected_return_date": "2025-03-07",
        "actual_return_date": null,
        "book": "1984",
        "is_active": true
    },
    {
        "id": 1,
        "borrow_date": "2025-03-01",
        "expected_return_date": "2025-03-05",
        "actual_return_date": "2025-03-01",
        "book": "Harry Potter and the Sorcerer's Stone",
        "is_active": false
    }
]
```

`GET /api/library/borrowings/<int:pk>/` - here users can see information about one of their borrowings.

##### Filter borrowing by status
`GET /api/library/borrowings/?is_active=true` - allows to filter borrowings by status. For active borrowings you should provide values like `True`, `true` or `1`. Everything else will be taken as False.

To borrow book, users should use `POST /api/library/borrowings/`. Make sure to provide expected return data and id of book you will borrow in body of request.
As result users will receive redirect url to make payment via Stripe.

Response example:

```json
{
    "redirect_url": "https://checkout.stripe.com/c/pay/cs_test_a1TuKbJHpO90smzdnfrnh48bgysdfnudsoigmdfuugbJHBTYBtrdewtyfyergrey7gtwevrdtrwffdunegftrbytftr5decf"
}
```

When user click on that url, it will redirect them to page like that to make payment:

![stripe_example.png](images/stripe_example.png)

After pay for borrowing, it will redirect you here:

`GET /api/payment/stripe/success/?session_id=cs_test_a1yWuGCysdjfnduigidfngfuihbEhM`

Where you will see information about successful payment:

```json
{
    "message": "Payment successful",
    "borrowing_id": 4
}
```

If you want to cancel payment, go here:

`GET /api/payment/stripe/cancel/?session_id=cs_test_a1yWuGCysdjfnduigidfngfuihbEhM`

And in result you will receive:

```json
{
    "message": "Payment was cancelled. You can try again."
}
```

Provide necessary information to pay for borrowing. (**Attention!** url for payment will be active only 24 hours.)

To return book you should use `POST /api/library/borrowings/<int:pk>/return/`. Make sure provide expected return data and id of book you will borrow in body of request. After that your borrowing will become inactive. If you return book later than expected return data, you should to pay fine for delaying.

---

### Payments:

`GET /api/payment/payments/` here users can see history of their payments.

Response example:

```json
[
    {
        "id": 1,
        "borrowing": 1,
        "session_url": "https://checkout.stripe.com/c/pay/cs_test_askdjfnifiewnfidshuigui4ht4hjdrg348uteufbkdsg783u4tgirh67erpJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl",
        "session_id": "cs_test_a1yWuGCyrgjhrdbyugydhgybhvtrcdjvbydfuugnggvfcr9bEhM",
        "amount_of_money": "6000.00",
        "status": 1,
        "type": 1
    },
    {
        "id": 2,
        "borrowing": 2,
        "session_url": "https://checkout.stripe.com/c/pay/cs_test_a1slfgduhgriuerdjgijrohjiot8itnuir8REIwa2tCcTxEYldnZDFDc0xdVzNATEptNmo2fTVObmY8c1NRaERPclNmNTVvSHFnMXBIZicpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl",
        "session_id": "cs_test_a185W04pn5DiAsdjfdyusfgedngrhtyjVmpCKR",
        "amount_of_money": "6000.00",
        "status": 1,
        "type": 1
    }
]
```

`GET /api/payment/payments/<int:pk>` here users can see information about specific payment.

Response example:

```json
{
        "id": 1,
        "borrowing": 1,
        "session_url": "https://checkout.stripe.com/c/pay/cs_test_askdjfnifiewnfidshuigui4ht4hjdrg348uteufbkdsg783u4tgirh67erpJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl",
        "session_id": "cs_test_a1yWuGCyrgjhrdbyugydhgybhvtrcdjvbydfuugnggvfcr9bEhM",
        "amount_of_money": "6000.00",
        "status": 1,
        "type": 1
    }
```

---

## Endpoints available only for admins

#### Authors:

`POST /api/library/authors/` - allows admins add new authors. Make sure provide first name and last name of author in request body.

`PUT /api/library/authors/<int:pk>/` - allows admins edit information about specific author. (All fields should be provided).

`PATCH /api/library/authors/<int:pk>/` - allows admins edit information about specific author partly (Only fields should be edited should be provided).

`DELETE /api/library/authors/<int:pk>/` - allows admins delete information about specific author.

---

#### Books:

`POST /api/library/books/` - allows admins add new books. Make sure provide information about title, cover, inventory, daily fee and authors in request body.

`PUT /api/library/books/<int:pk>/` - allows admins edit information about specific book. (All fields should be provided).

`PATCH /api/library/books/<int:pk>/` - allows admins edit information about specific book partly (Only fields should be edited should be provided).

`DELETE /api/library/books/<int:pk>/` - allows admins delete information about specific book.

---

#### Borrowings:

Admins can see information about all borrowings here: `GET /api/library/borrowings/`.

They also can filter them by `user_id` like that: `GET /api/library/borrowings/?user_id=1` to see borrowings of concrete user.

---

#### Payments:

Admins can see list of all payments via `GET /api/payment/payments/`

---
## Endpoints of documentation

`GET /api/schema/swagger-ui/` - here is available documentation like that:

![swagger_ui.png](images/swagger_ui.png)

`GET /api/schema/redoc/` - here is available documentation like that:

![redoc_swagger.png](images/redoc_swagger.png)

`GET /api/schema/redoc/` - allows to download .yaml file where is described our api.

---
## Installation

```shell
git clone https://github.com/MaksVakulenko/DRF-Library.git
cd DRF-Library
```

---

### Poetry must be installed

- Activate poetry virtual environment
- Install dependencies using command ```poetry install --no-root```

---

To work with project locally, initialize `.env` file using `.env.sample` as example. Change value of `DJANGO_DB` on `sqlite`.

Then execute such commands:

```shell
cd src
python manage.py migrate
python manage.py loaddata data.json
python manage.py runserver
```

---

Test credentials as admin user:

```
email: admin@admin.com
password: 1234
```
---
Feel free to register as regular user and explore api or use one of those credentials.

```
email: caleb@admans.com
password: caleb_password
```
```
email: kate@smith.com
password: kate_password
```
---
## Dockerized

## Overview

- **Database**: The project now uses PostgreSQL (via the `psycopg-binary` package) as the primary database. The connection settings are specified in the environment variables.
- **Docker Configuration**:  
  - A single Docker Compose file is used to build and run containers for the backend and PostgreSQL.
  - Volumes have been configured for persistent storage of static files, media, and database data.
- **Environment Variables**:  
  - The `.env` file now includes settings for PostgreSQL.
  - The database selection is controlled by the `DJANGO_DB` variable.
- **Initialization Script (`init.sql`)**:  
  - This script creates the PostgreSQL database and grants privileges to the specified user.
- **Healthchecks**:  
  - The backend container now have special endpoint for healthcheck
- **Docker Compose Override**:  
  - (Optional) A secondary Compose file (`docker-compose-local.yaml`) may be used for local development or debugging with postgres in docker.

---

## Changes Introduced

### 1. Environment Variables (`.env`)
- **Database Settings**:
  - `DJANGO_DB` is now set to `postgresql` (comment out `sqlite`).
  - PostgreSQL connection variables (`POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB_PORT`) are defined.


> **Note:**  
> Make sure to update your `.env` file with the correct values before running the project.

### 2. Docker Configuration
- **docker-compose.yaml**:  
  The Compose file defines the following services:
  - **db**: Uses the official PostgreSQL 16.0 image. The container name is set to `library-postgres`, and it mounts `init.sql` to automatically initialize the database.
  - **backend**: Builds the backend image using `./docker/backend/Dockerfile`, mounts the source code from `./src`, and sets up volumes for static files and media.
  - **Volumes & Networks**:  
    Volumes are configured for static files, media, and database data. A custom Docker network (`library-network`) is created.

### 3. Database Initialization (`init.sql`)
- The `init.sql` script is automatically executed by the PostgreSQL container. It performs the following actions:
  - Creates the database (`library_db`).
  - Grants all privileges on all tables in the public schema to the `admin` user.
  
> **Example `init.sql`:**
```
CREATE DATABASE library_db;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
```

### 4. Backend Entrypoint Script
- **server-entrypoint.sh**:
  - Changes to the backend directory.
  - Runs Django migrations.
  - Collects static files.
  - Finally, starts the Django development server (or Gunicorn for production).
  

### 5. Healthcheck Configuration
- The backend service in `docker-compose.yaml` includes a healthcheck that pings the `/api/health/` endpoint.
- If you wish to disable continuous healthchecks after startup, adjust the `interval`, `timeout`, or `retries` values accordingly.

---

## How to Use the Changes

### Running the Project with Docker

1. **Update Environment Variables:**
   - Copy `.env.sample` to `.env` and update the values as needed:
     ```bash
     cp .env.sample .env
     ```

2. **Build and Start Containers:**
   - Run the following command to build the images and start all containers:
     ```bash
     docker-compose up --build
     ```

3. **Database Initialization:**
   - The PostgreSQL container will execute the `init.sql` file on startup to create the database and set permissions.


### Using the Alternative Docker Compose File
- If you want to use Django Project from IDE with postgres from docker, please use docker-compose-local and specify this file for docker-compose commands,
ex:
  ```bash
  docker-compose -f docker-compose-local.yaml up --build
  ```

## Overview of Changes

1. **Environment Variables and Database Selection**  
   - The project now supports both SQLite and PostgreSQL backends.  
   - The `DJANGO_DB` environment variable controls which database is used:
     - Set `DJANGO_DB=sqlite` for a local SQLite database.
     - Set `DJANGO_DB=postgresql` for a PostgreSQL database.
### Database Host Selection for PostgreSQL

- **If using setup DB + Django from Docker**: Set `POSTGRES_HOST=library-postgres` (the container name).
- **If running Django locally and DB in docker**: Set `POSTGRES_HOST=localhost`.
```ini
# Django:
SECRET_KEY=_eSHIGrn*@OSo!H1hDISxl4hH8wj90La

# Stripe:
STRIPE_SECRET_KEY='your_secret_key'
STRIPE_PUBLISHABLE_KEY='your_publishable_key'

# Database selection:
# Please specify which database you would like to use and comment out the other option:
#DJANGO_DB=sqlite
DJANGO_DB=postgresql

# PostgreSQL (for Docker deployment):
POSTGRES_HOST=library-postgres      # This is the container name for the PostgreSQL service
POSTGRES_DB=library_db                # Database name
POSTGRES_USER=admin
POSTGRES_PASSWORD=some_password
POSTGRES_DB_PORT=5432
```
