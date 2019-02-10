# Project 1

Web Programming with Python and JavaScript
applications.py defines functions as discussed below. The relevant .html pages are defined in the descriptions of the routes: 

/: If logged in, the user is directed to the search page (search.html). If not, the user is directed, via search, the login page (login.html)
/register (register.html) User gets to this route by clicking on 'register' in the navbar. They register here. The password hash is generated with werkzeug.security (we used this in a CS50 project). The code does not allow users to register with a previously used ID. A message to this effect is diplayed on the screen if a user tries. Messages are generated for the user if they do not input a username,or if they don't put the same thing in the password and confirmation input boxes. 
/login: Users login with username and password. Password hashes are checked with werkzeug security.
/logout: clears the session user information (from flask_session) and redirects to login.
/search: The search function first looks for exact matches (eg, if you search for "robot", we're looking for author, ISBN or title called "Robot"). If something is found, the results of this search are returned. If nothing is found, the search is expanded to find something with the word "robot' in the title, ISBN, author. The search term is converted to all lowercase, as are the results from the SQL query to which it is being compared. This way, the search is not case sensitive. After a search is conducted, users are directed to a results page. Another search box is on this page so users can search again here if they don't see the book they anticipated. If there are no results, a message to that effect is rendered on the page.
/reviews: If the user clicks on one of the search results, they are redirected to this page which includes book info, reviews from this site, and data from goodreviews (using the API). In this code, I check whether or not the user has submitted a review for the book. If they have NOT, they will see a form for submitting a review. If they have submitted a review, they won't see the form.
