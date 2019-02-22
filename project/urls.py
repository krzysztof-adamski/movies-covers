from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('api/', include('movies.urls')),
    path('admin/', admin.site.urls),
]
