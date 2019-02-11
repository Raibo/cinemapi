# cinemapi
Practice rest api project on django. It represents functionality, such as booking and buying tickets to the cinema, viewing movie sessions schedule, movie halls information, etc.

Notes:
  1. The secret key from the settings is stored 'as is'. In general, it is not a good thing to do, and it should be hidden using such methods as django-secrets package. But since it is a practice project, I leave the secret there.
  2. The 'session' endpoint returns all sessions, not filtering by session starting time. In real world application it is not a good thing to do, because users don't need excess information about movie sessions in the past. Such excess and useless information would build up over time, creating problems for both users and the server, but again, since it is a practice project, I leave it to be like that.
