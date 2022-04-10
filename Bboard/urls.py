from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # including my application - 'myboardapp' urls into the main project
    path('', include('myboardapp.urls')),
]
