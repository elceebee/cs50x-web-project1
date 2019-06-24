# BookClub Project

This application is a platform for users to review and read reviews of books. It uses a publically available API from <https://www.goodreads.com/api> so users are presented with star ratings and review data from this external source. The application also allows users to query for book details via my own API.

The project was part of CS50W: Web Programming with Python and JavaScript. For more information about this course, see: <https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript>

## The brief

"In this project, you’ll build a book review website. Users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API."

## Technologies used

- Python
- Flask
- Werkzeug
- Jinja
- PostgresSQL
- Heroku
- Sass
- Bootstrap
- External API from (<https://www.goodreads.com/api>)

## Approach

This application is rendered serverside. The client side logic is embedded into the HTML using Jinja (see here for an example [templates/reviews.html#L31](https://github.com/elceebee/cs50x-web-project1/blob/cd9fbd67fb08949097e67668957656bd38a9d59e/templates/reviews.html#L31))

### API from www.goodreads.com

I make a request to an API available through www.goodreads.com to see render reviews information. See here for the code: [application.py#L228](https://github.com/elceebee/cs50x-web-project1/blob/cd9fbd67fb08949097e67668957656bd38a9d59e/application.py#L228)

### Database, PostrgresSQL

Book data: The course leader provided a csv file with book information. Here is the file for importing the data into the SQL database: [import.py#L1](https://github.com/elceebee/cs50x-web-project1/blob/cd9fbd67fb08949097e67668957656bd38a9d59e/import.py#L1)

When a user adds a review, it is added to the database: [application.py#L183](https://github.com/elceebee/cs50x-web-project1/blob/cd9fbd67fb08949097e67668957656bd38a9d59e/application.py#L183)

### Passwords and registered users

When users register, their user credentials are stored in the database and the passwords are encrypted using Werkzeug. See [application.py#L55](https://github.com/elceebee/cs50x-web-project1/blob/cd9fbd67fb08949097e67668957656bd38a9d59e/application.py#L55).
