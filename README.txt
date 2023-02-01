working with DATABASE

>>> from myboardapp.models import Bulletin
>>> from django.contrib.auth.models import User
>>> user = User.objects.all().last()
>>> bulletin_1 = Bulletin(title = 'My second offer', content = 'Buy my product', author=user)
>>> bulletin_1.save()

Adding CATEGORY into the DATABASE
>>> from myboardapp.models import CategoryModel
>>> cat = CategoryModel(category_name = 'Offer')
>>> cat.save()

To see all posts of certain user
>>> user.bulletin_set.all()
