
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('task.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
]
