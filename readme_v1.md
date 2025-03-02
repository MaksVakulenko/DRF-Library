# Library API 📚

Welcome Library! Here you can borrow books to your liking and enjoy a vast collection of literature. Whether you love fiction, non-fiction, or research materials, our library is here to serve you.

## Features of our service

- JWT Authentication
- Online payment for your borrowing
- Telegram bot to receive notifications about borrowing

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

![img.png](img.png)

1) Add header `Authorize`
2) Enable it via checkpoint.
3) Provide value of access token like this: `Bearer access_token_value`.

##### In Postman:

![img_1.png](img_1.png)

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

![img_2.png](img_2.png)

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

## Endpoints available only for admins

#### Authors:

`POST /api/library/authors/` - allows admins add new authors. Make sure provide first name and last name of author in request body.

`PUT /api/library/authors/<int:pk>/` - allows admins edit information about specific author. (All fields should be provided).

`PATCH /api/library/authors/<int:pk>/` - allows admins edit information about specific author partly (Only fields should be edited should be provided).

`DELETE /api/library/authors/<int:pk>/` - allows admins delete information about specific author.

#### Books:

`POST /api/library/books/` - allows admins add new books. Make sure provide information about title, cover, inventory, daily fee and authors in request body.

`PUT /api/library/books/<int:pk>/` - allows admins edit information about specific book. (All fields should be provided).

`PATCH /api/library/books/<int:pk>/` - allows admins edit information about specific book partly (Only fields should be edited should be provided).

`DELETE /api/library/books/<int:pk>/` - allows admins delete information about specific book.

#### Borrowings:

Admins can see information about all borrowings here: `GET /api/library/borrowings/`.

They also can filter them by `user_id` like that: `GET /api/library/borrowings/?user_id=1` to see borrowings of concrete user.

#### Payments:

Admins can see list of all payments via `GET /api/payment/payments/`

## Endpoints of documentation

`GET /api/schema/swagger-ui/` - here is available documentation like that:

![img_3.png](img_3.png)

`GET /api/schema/redoc/` - here is available documentation like that:

![img_4.png](img_4.png)

`GET /api/schema/redoc/` - allows to download .yaml file where is described our api.

## Installation

```shell
git clone https://github.com/MaksVakulenko/DRF-Library.git
cd DRF-Library
```

To work with project locally, initialize `.env` file using `.env.sample` as example. Change value of `DJANGO_DB` on `sqlite`.

Then execute such commands:

```shell
cd src
python manage.py migrate
python manage.py loaddata data.json
python manage.py runserver
```

Test credentials as admin user:

```
email: admin@admin.com
password: 1234
```

Feel free to register as regular user and explore api.

