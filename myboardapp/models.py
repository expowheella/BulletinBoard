from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# User model
class User(models.Model):
    # inheriting user attributes from standard library
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # returning user name
    def __str__(self):
        return f'{self.user.name.title()}'


# here is a function which will be used as a callable
# it will be called to obtain the upload path
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Bulletins category model
class CategoryModel(models.Model):
    # this field is for creating bulletin category in the admin panel
    category_name = models.CharField(max_length=255,
                                     unique=True,
                                     )

    # we use this function to return the bulletin category of an instance
    def __str__(self):
        return f'{self.category_name}'


# Bulletin model
class Bulletin(models.Model):
    # bulletin has its author
    # if an author is deleted, his bulletins will be deleted too
    # this is One to Many field -> built-in User has its examples which are authors
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # bulletin has content
    content = models.TextField()

    # it is possible to adjust a bulletin with a file
    # file will be saved to -> watch settings.py -> MEDIA_ROOT
    file = models.FileField(models.FileField(upload_to=user_directory_path,
                                             blank=True,
                                             # null=True,
                                             verbose_name='File Upload'))

    def __str__(self):
        return self.file.verbose_name

    # each bulletin related to some category
    # that is why we use Many-To-One field
    bulletin_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    # add bulletin created date
    date_created = models.DateTimeField(default=timezone.now)
