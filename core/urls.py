from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from core.views import GeneratePdf

urlpatterns = [
    path('', views.home, name='home'),
    path('tables/', views.tables, name='tables'),
    path('register/', views.registration, name='registration'),
    path('file-upload/', views.upload, name='file-upload'),
    path('pdf-download/', GeneratePdf.as_view(), name='pdf-download'),
    path('file-delete/', views.file_delete, name='file-delete'),
    path('file-download/', views.download, name='file-download'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
