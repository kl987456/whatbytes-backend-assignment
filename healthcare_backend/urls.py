from django.contrib import admin
from django.urls import path, include  # ✅ This line is required!
from django.http import JsonResponse   # ✅ Required for home_view

def home_view(request):
    return JsonResponse({
        "message": "Welcome to Healthcare API 👨‍⚕️",
        "visit": "/api/",
        "auth": ["/api/auth/register/", "/api/auth/login/"],
        "resources": ["/api/patients/", "/api/doctors/", "/api/mappings/"]
    })

urlpatterns = [
    path('', home_view),  # ✅ Now works
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
