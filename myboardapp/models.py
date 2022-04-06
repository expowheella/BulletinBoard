from django.contrib.auth.models import User
from django.db import models


# User model
class User(models.Model):
    # inheriting user attributes from standard library
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # returning user name
    def __str__(self):
        return f'{self.user.name.title()}'

# Bulletin model
class Bulletin(models.Model):
    # bulletin has its author
    # if an author is deleted, his bulletins will be deleted too
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # bulletin has content
    content = models.TextField()

