from django.shortcuts import render, get_object_or_404, redirect
from facility.models import Facilities, Availability
from reservation.models import Reservation
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import User
from .forms import FacilityForm, RestrictionForm
from django.contrib import messages
from django.http import JsonResponse
from datetime import time
from django.contrib import messages
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from datetime import datetime
# Create your views here.
@staff_member_required
def adminsite(request):
    facilities = Facilities.objects.all()
    reservas = Reservation.objects.all()
    users = User.objects.all()

    context = {
        'facilities': facilities,
        'reservas': reservas,
        'users': users
    }

    return render(request, 'adminsite.html', context)

@staff_member_required 
def crear_espacio(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()  
            return redirect('adminsite') 
    else:
        form = FacilityForm()
    return render(request, 'crear_espacio.html', {'form': form})

@staff_member_required
def restringir_acceso(request, facility_id):
    facility = get_object_or_404(Facilities, idFacility=facility_id)

    if request.method == 'POST':
        if 'time_slot' in request.POST:
            selected_date = request.POST.get('date')
            form = RestrictionForm(request.POST, facility_id=facility_id, date=selected_date)

            if form.is_valid():
                selected_time_slot = form.cleaned_data['time_slot']
                selected_date = form.cleaned_data['date']

                if selected_time_slot:
                    Availability.objects.filter(facilities_id=facility_id, date=selected_date, id=selected_time_slot).update(is_restricted=True)
                    messages.success(request, 'Acceso restringido con éxito para el horario seleccionado.')
                    return redirect('restringir_acceso', facility_id=facility_id)

        elif 'enable_time_slot' in request.POST:
            time_slot_id = request.POST.get('enable_time_slot')
            try:
                Availability.objects.filter(id=time_slot_id).update(is_restricted=False)
                messages.success(request, 'Acceso habilitado con éxito para el horario seleccionado.')
            except Availability.DoesNotExist:
                messages.error(request, 'No se pudo encontrar el horario para habilitar.')
            return redirect('restringir_acceso', facility_id=facility_id)

    else:
        form = RestrictionForm(facility_id=facility_id)

    restricted_timeslots = Availability.objects.filter(facilities_id=facility_id, is_restricted=True)

    return render(request, 'restringir_acceso.html', {'facility': facility, 'form': form, 'restricted_timeslots': restricted_timeslots})

@staff_member_required
def mostrarGraficas(request):
    matplotlib.use('Agg')
    fechahoy = datetime.now()
    # Mirar las fechas de todas las reservas activas
    activas = Reservation.objects.filter(date__gte=fechahoy).order_by("date").values_list("date",flat=True)
    # Crear un diccionario para almacenar la cantidad de reservas
    reservas_porFecha = {}
    for date in activas:
        if date in reservas_porFecha:
            reservas_porFecha[date] += 1
        else:
           reservas_porFecha[date] = 1
    print(reservas_porFecha)
    print(type(reservas_porFecha))
    # Ancho de las barras
    bar_width = 0.5 
    # Separación entre las barras
    bar_spacing = 0.5 
    # Posiciones de las barras
    bar_positions = range(len(reservas_porFecha))
    # Crear la gráfica de barras
    plt.bar(bar_positions, reservas_porFecha.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Cantidad de reservas por dia')
    plt.xlabel('Fecha')
    plt.ylabel('Número de reservas')
    plt.xticks(bar_positions, reservas_porFecha.keys())
    max_reservas = max(reservas_porFecha.values())
    plt.yticks(range(1, max_reservas + 1)) 
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Segunda
    fechahoy = datetime.now()
    # Obtener las reservas activas agrupadas por espacio
    activas = Reservation.objects.filter(date__gte=fechahoy).values_list("facilities__name", flat=True)
    
    # Crear un diccionario para almacenar la cantidad de reservas por espacio
    reservas_porEspacio = {}
    for espacio in activas:
        if espacio in reservas_porEspacio:
            reservas_porEspacio[espacio] += 1
        else:
            reservas_porEspacio[espacio] = 1
    print("Segunda grafica")
    print(reservas_porEspacio)
    print(type(reservas_porEspacio))
    
    # Extraer los nombres de los espacios y las cantidades de reservas
    espacios = reservas_porEspacio.keys()
    reservas = reservas_porEspacio.values()
    
    # Crear un gráfico circular
    plt.figure(figsize=(6, 6))  # Ajustar el tamaño de la figura
    plt.pie(reservas, labels=espacios, autopct='%1.1f%%', startangle=90, counterclock=False)
    
    # Personalizar el gráfico
    plt.title('Porcentaje de Reservas por Espacio')
    plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo
    
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    
    buffer.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    pastel = base64.b64encode(image_png)
    pastel = pastel.decode('utf-8')

    return render(request, 'analiticas.html',{'graphic':graphic,'pastel':pastel})

@staff_member_required
def eliminar_espacio(request, facility_id):
    facility = get_object_or_404(Facilities, idFacility=facility_id)
    
    if request.method == 'POST':
        facility.delete()  
        messages.success(request, 'Espacio eliminado con éxito.')
        return redirect('adminsite')  
    
    return render(request, 'eliminacion.html', {'facility': facility})

@staff_member_required
def eliminar_reservacion(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.delete()  
        messages.success(request, 'Reservación eliminada con éxito.')
        return redirect('adminsite') 
    
    return render(request, 'eliminacion_reservacion.html', {'reserva': reservation})
