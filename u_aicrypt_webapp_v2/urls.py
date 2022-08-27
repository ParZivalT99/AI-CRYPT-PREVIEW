
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("tz_detect/", include("tz_detect.urls")),
    path('',include('applications.dashboard_app.urls')),
    path('admin/', admin.site.urls),
]
