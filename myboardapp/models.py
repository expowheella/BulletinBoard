from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# User model
# class UsualUser(models.Model):
#     # inheriting user attributes from standard library
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     # returning user name
#     def __str__(self):
#         return f'{self.user.name.title()}'


# here is a function which will be used as a callable
# # it will be called to obtain the upload path
# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.author.id, filename)


# Bulletins category model
class CategoryModel(models.Model):

    CHOISES = [
        ('Танки', "Танки"),
        ('Хилы', "Хилы"),
        ('ДД', "ДД"),
        ('Торговцы', "Торговцы"),
        ('Гилдмастеры', "Гилдмастеры"),
        ('Квестгиверы', "Квестгиверы"),
        ('Кузнецы', "Кузнецы"),
        ('Кожевники', "Кожевники"),
        ('Зельевары', "Зельевары"),
        ('Мастера заклинаний', "Мастера заклинаний"),
    ]

    # this field is for creating bulletin category in the admin panel
    category_name = models.CharField(max_length=255,
                                     choices=CHOISES,
                                     unique=True,
                                     )

    subscribers = models.ManyToManyField(User, null=True, blank=True, related_name='subscriber')

    # we use this function to return the bulletin category of an instance
    def __str__(self):
        return f'{self.category_name}'
    """ 
    >>> from myboardapp.models import Bulletin
    >>> from myboardapp.models import CategoryModel
    >>> CategoryModel.objects.create(category_name = "Offer")
    <CategoryModel: Offer>
    """


# Bulletin model
class Bulletin(models.Model):
    title = models.CharField(max_length=100, blank=True)
    # bulletin has its author
    # if an author is deleted, his bulletins will be deleted too
    # this is One to Many field -> built-in User has its examples which are authors
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # bulletin has content
    content = models.TextField()

    # it is possible to adjust a bulletin with a file

    # file will be saved to -> watch settings.py -> MEDIA_ROOT
    file = models.FileField(upload_to='files/',
                                             blank=True,
                                             # null=True,
                                             )


    # each bulletin related to some category
    # that is why we use Many-To-One field
    bulletin_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    # add bulletin created date
    date_created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return the full path to a specific post as a string
        # a name of the url-pattern --> 'bulletin-detail'
        # kwargs --> pk - primary key of the self --> bulletin posted
        return reverse('bulletin-detail', kwargs={'pk': self.pk})



class Comment(models.Model):
    # connecting Comment model with Bulletin model
    bulletin = models.ForeignKey(Bulletin, related_name="comments", on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.bulletin.title, self.username)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('comment_create', kwargs={'pk': self.pk})