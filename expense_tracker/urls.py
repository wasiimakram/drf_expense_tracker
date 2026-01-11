from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/categories/', include('categories.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/income/', include('income.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    # --- Swagger - Documentation Endpoints (drf-spectacular) ---
    # 1. Schema: Generates the raw OpenAPI JSON file (Machine Readable)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # 2. Swagger UI: Interactive Interface for testing APIs (Developer Friendly)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # 3. Redoc: Clean, Organize documentation for reading (User Friendly)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# This is to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
