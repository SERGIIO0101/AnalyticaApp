from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('archivo/<int:archivo_id>/', views.serve_file, name='serve_file'),
    path('generate_chart/<int:archivo_id>/', views.generate_chart, name='generate_chart'),
]
