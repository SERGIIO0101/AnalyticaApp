from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Archivo, Grafica
from .forms import ArchivoForm
from django.http import FileResponse
from django.conf import settings
import os
import openpyxl
import matplotlib.pyplot as plt
import numpy as np

# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('welcome')
    return render(request, 'accounts/register.html')

@login_required
def welcome(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.usuario = request.user
            archivo.save()
            return redirect('welcome')
    else:
        form = ArchivoForm()
    archivos = Archivo.objects.filter(usuario=request.user)
    return render(request, 'accounts/welcome.html', {'form': form, 'archivos': archivos})

@login_required
def serve_file(request, archivo_id):
    archivo = Archivo.objects.get(id=archivo_id)
    file_path = os.path.join(settings.MEDIA_ROOT, archivo.archivo.name)
    return FileResponse(open(file_path, 'rb'))

def generate_chart(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)
    
    # Ruta al archivo XLSX en el sistema de archivos
    file_path = archivo.archivo.path
    
    # Abrir el archivo XLSX
    wb = openpyxl.load_workbook(file_path)
    
    # Seleccionar la primera hoja de cálculo (puedes ajustar esto según tu archivo)
    sheet = wb.active
    
    # Leer los datos del archivo y convertirlos en una lista
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    
    # Procesar los datos para la gráfica (aquí necesitarías adaptar esto a tus datos)
    labels = [row[0] for row in data[1:]]  # Suponiendo que las etiquetas están en la primera columna
    values = [row[1] for row in data[1:]]  # Suponiendo que los valores están en la segunda columna
    
    # Generar la gráfica de barras
    plt.bar(np.arange(len(labels)), values)
    plt.xticks(np.arange(len(labels)), labels, rotation=45)
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.title('Bar Chart')
    
    # Guardar la gráfica en un archivo en el sistema de archivos
    chart_file_path = f'grafica_{archivo_id}.png'
    plt.savefig(os.path.join(settings.MEDIA_ROOT, chart_file_path))
    
    # Crear una instancia de Grafica y guardarla en la base de datos
    Grafica.objects.create(
        archivo=archivo, 
        tipo_grafica='bar', 
        parametros={},  # Aquí puedes guardar cualquier parámetro adicional que necesites
        imagen_grafica=chart_file_path
    )
    
    # Redirigir a la página de bienvenida
    return redirect('welcome')

@login_required
def serve_file(request, archivo_id):
    archivo = Archivo.objects.get(id=archivo_id)
    file_path = os.path.join(settings.MEDIA_ROOT, archivo.archivo.name)
    return FileResponse(open(file_path, 'rb'))