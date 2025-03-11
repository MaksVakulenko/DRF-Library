from drf_spectacular.utils import OpenApiExample, OpenApiParameter

post_authors_example=[
    OpenApiExample(
        name='authors',
        description='Add new author to the list of library. Make sure to authorize as admin user before trying it.',
        value={
            "first_name": "Arthur",
            "last_name": "Conan Doyle"
        }
    )
]

author_id_parameter=[
    OpenApiParameter(
        name='id',
        description='Get author by id',
        required=True,
        type=int,
        location=OpenApiParameter.PATH,
        examples=[OpenApiExample(
            name='author_id',
            value=1
        )]
    )
]

put_author_example=[
    OpenApiExample(
        name='author put',
        description='Update author by id = 1. Make sure to authorize as admin user before trying it.',
        value=
        {
                "id": 1,
                "first_name": "William",
                "last_name": "Shakespeare"
        }
    )
]

patch_author_example=[
    OpenApiExample(
        name='author patch',
        description="Update first name of author by id = 1. Make sure to authorize as admin user.",
        value={
            "first_name": "WILLIAM",
        }
    )
]

author_id_parameter_to_delete=[
    OpenApiParameter(
        name='id',
        description='Delete author by id',
        required=True,
        type=int,
        location=OpenApiParameter.PATH,
        examples=[OpenApiExample(
            name='author',
        )]
    )
]

author_search_and_ordering_parameters = [
    OpenApiParameter(
        name='search',
        description='Search author by specific parameter.',
        required=False,
        type=str,
        location=OpenApiParameter.QUERY,
        examples=[
            OpenApiExample(
                name="author's first name",
            ),
            OpenApiExample(
                name="author's last name",
            ),
        ]
    ),
    OpenApiParameter(
        name='ordering',
        description='Order author by specific parameter.',
        required=False,
        type=str,
        location=OpenApiParameter.QUERY,
        examples=[
            OpenApiExample(
                name='id ascending',
                value="id"
            ),
            OpenApiExample(
                name='id descending',
                value="-id"
            ),
            OpenApiExample(
                name="author's first name ascending",
                value="first_name"
            ),
            OpenApiExample(
                name="author's first name descending",
                value="-first_name"
            ),
            OpenApiExample(
                name="author's last name ascending",
                value="last_name"
            ),
            OpenApiExample(
                name="author's last name descending",
                value="-last_name"
            ),
        ]
    )
]

book_search_and_ordering_parameters = [
    OpenApiParameter(
        name='search',
        description='Search books by specific parameter.',
        required=False,
        type=str,
        location=OpenApiParameter.QUERY,
        examples=[
            OpenApiExample(
                name='title',
            ),
            OpenApiExample(
                name="author's first name",
            ),
            OpenApiExample(
                name="author's last name",
            ),
        ]
    ),
    OpenApiParameter(
        name='ordering',
        description='Order books by specific parameter.',
        required=False,
        type=str,
        location=OpenApiParameter.QUERY,
        examples=[
            OpenApiExample(
                name='id ascending',
                value="id"
            ),
            OpenApiExample(
                name='id descending',
                value="-id"
            ),
            OpenApiExample(
                name="title ascending",
                value="title"
            ),
            OpenApiExample(
                name="title descending",
                value="-title"
            ),
            OpenApiExample(
                name="author's first name ascending",
                value="primary_author_first_name"
            ),
            OpenApiExample(
                name="author's first name descending",
                value="-primary_author_first_name"
            ),
            OpenApiExample(
                name="author's last name ascending",
                value="primary_author_last_name"
            ),
            OpenApiExample(
                name="author's last name descending",
                value="-primary_author_last_name"
            ),
        ]
    )
]

post_book_example=[
    OpenApiExample(
        name='book',
        description="Add new book to the list of library. Make sure to authorize as admin user.",
        value={
            "id": 41,
            "title": "The Fall of the House of Usher",
            "cover": "HARD",
            "inventory": 4,
            "daily_fee": "5.00",
            "authors": [
                24
            ]
        }
    )
]

book_id_parameter=[
    OpenApiParameter(
        name='id',
        description='Get book by id = 1',
        required=True,
        type=int,
        location=OpenApiParameter.PATH,
        examples=[OpenApiExample(
            name='book_id',
            value=1
        )]
    )
]

put_book_example=[
    OpenApiExample(
        name='book',
        description="Update book by id = 1. Make sure to authorize as admin user.",
        value={
          "id": 1,
          "title": "Hamlet",
          "authors": [
            1
          ],
          "cover": "HARD",
          "inventory": 5,
          "daily_fee": "15.00"
        }
    )
]

patch_book_example=[
    OpenApiExample(
        name='book',
        description="Update cover of book by id. Make sure to authorize as admin user.",
        value={
            "cover": "SOFT",
        }
    )
]

book_id_parameter_delete=[
OpenApiParameter(
        name='id',
        description='Delete book by id',
        required=True,
        type=int,
        location=OpenApiParameter.PATH,
        examples=[OpenApiExample(
            name='book_id',
        )]
    )
]

borrow_id_parameter=[
OpenApiParameter(
        name='id',
        description='Borrowing by id',
        required=True,
        type=int,
        location=OpenApiParameter.PATH,
        examples=[OpenApiExample(
            name='borrowing_id',
        )]
    )
]

borrowing_filter_parameters=[
    OpenApiParameter(
        name="is_active",
        description="Filter borrowings by status of borrowing.",
        required=False,
        type=str,
        examples=[OpenApiExample(
            name='is_active_status_true',
            value='true'
        ),
        OpenApiExample(
            name='is_active_status_false',
            value='false'
        )]
    ),
    OpenApiParameter(
        name="user_id",
        description="Filter borrowings by user id (available only for admin users)",
        required=False,
        type=int,
        examples=[OpenApiExample(
            name='user_id',
        )]
    )
]

borrowing_post_example=[
    OpenApiExample(
        name='borrowing',
        description="Add new borrowing for user.",
        value={
            "expected_return_date": "2025-03-04",
            "book": 1
        }
    )
]

payment_id_parameter=[
    OpenApiParameter(
        name='id',
        description='Get payment id by id',
        required=True,
        type=int,
        location=OpenApiParameter.PATH,
        examples=[OpenApiExample(
            name='payment_id',
        )]
    )
]

my_profile_put_example=[
    OpenApiExample(
        name='my_profile',
        description="Edit your profile.",
        value={
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "my_new_password",
        }
    )
]

my_profile_patch_example=[
    OpenApiExample(
        name='my_profile',
        description="Edit your profile partly.",
        value={
            "last_name": "Smith",
        }
    )
]

registration=[OpenApiExample(
    name='registration',
    description="Register your account.",
    value={
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "password": "john_password",
    }
)]

borrowing_return_example=[
    OpenApiExample(
        name='borrowing_to_return',
        description="Return book. Make sure to authorize as admin user or Caleb Adams from readme.md.",
        value={}
    )
]
