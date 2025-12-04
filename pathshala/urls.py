from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('course/', include('courses.urls')),
    path('enrollment/', include('enrollments.urls')),
    path('progress/', include('progress.urls')),
    path('interactions/', include('interactions.urls'))
]
