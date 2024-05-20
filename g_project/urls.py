from django.contrib import admin
from django.urls import path
from pd_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_folder, name='upload_folder'),
    path('result/', views.result, name='result'),
]
