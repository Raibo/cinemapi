# cinemapi
Practice rest api django project. It represents functionality, such as booking and buying tickets to the cinema, viewing movie sessions schedule, movie halls information, etc.

How to launch:
  1. clone repository
  2. docker-compose up (you may need to try twice if db would still be starting up on django startup)
  3. connect using port 8000

Notes:
  1. The secret key from the settings is stored 'as is'. In general, it is not a good thing to do, and it should be hidden using such methods as django-secrets package. But since it is a practice project, I leave the secret there.
  2. The 'session' endpoint returns all sessions, not filtering by session starting time and no user filter available. Similar with tickets and movies, no filtering. In real world application it is not a good thing to do, because users don't need excess information about movie sessions in the past. Such excess and useless information would build up over time, creating problems for both users and the server, but again, since it is a practice project, I leave it to be like that.
  3. The 'session' endpoint returns tickets list, showing row and seat for each one, meaning that user recieves list of booked seats, not available seats. This should not be a problem, since api meant to work with some gui software. Such software would mark all the seats as available and booked anyway. Meanwhile, api does not perform excess computations, which seems good.

API description:

register/ 
POST.
  registers new user (username is required by jwt)
body example:
{
    "username": "user",
    "email": "user@mail.ru",
    "password": "testing321"
}

token/
POST.
  jwt tokens
body example:
{
    "username": "user",
    "password": "testing321"
}

token/refresh/
POST.
  new access token
body example:
{
    "refresh": "(refresh token)"
}

current_user/
GET.
  user info of the caller

user/\[id/\]
GET.
  user info of all or specified user

hall/\[id/\]
GET.
  cinema halls info

movie/\[id/\]
GET, POST, PATCH, PUT, DELETE.
  get, set, modify or delete info about movies

session/\[id/\]
GET, POST, PATCH, PUT, DELETE.
  get, set, modify or delete info about movie sessions

ticket/\[id/\]
GET, DELETE.
  get all tickets for current user, both booked and paid. If user is staff, includes tickets for all users

book/
POST.
  creates a ticket for specified session and seat with status "booked"
body example:
{
	"session":1,
	"row":2,
	"seat":3,
	"user":4
}

pay/(id)/
PATCH.
  modify ticket status to "paid"
