from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('iniciar/', views.login_view, name='iniciar'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('developer/', views.developer, name='developer'),
    path('archivo/<int:archivo_id>/', views.serve_file, name='serve_file'),
    path('generate_chart/<int:archivo_id>/', views.generate_chart, name='generate_chart'),
    path('generate_pie_chart/<int:archivo_id>/', views.generate_pie_chart, name='generate_pie_chart'),
    path('archivo/detail/<int:archivo_id>/', views.archivo_detail, name='archivo_detail'),
    path('delete_archivo/<int:archivo_id>/', views.delete_archivo, name='delete_archivo'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
