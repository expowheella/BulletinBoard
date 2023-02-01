<<<<<<< Updated upstream
from django.contrib import admin
from .models import Bulletin

admin.site.register(Bulletin)

=======
from django.contrib import admin
from .models import Bulletin, CategoryModel, Comment

admin.site.register(Bulletin)
admin.site.register(CategoryModel)
admin.site.register(Comment)
>>>>>>> Stashed changes
