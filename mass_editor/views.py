from django.shortcuts import render, redirect
from .forms import CustomFieldForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .service.updateThread import update
from threading import Thread
import csv
import time


@login_required
def step_one(request):

    if request.method == 'POST':
        form = CustomFieldForm(request.POST)
        if form.is_valid():
            # Hier können Sie die Logik implementieren, um die Auswahl zu speichern
            # Zum Beispiel könnten Sie die ausgewählten Felder in der Session speichern
            request.session['selected_options_identifier'] = form.cleaned_data['options']
            return redirect('step_two')  # Leiten Sie zum nächsten Schritt weiter
    else:
        form = CustomFieldForm()

    return render(request, 'step_one.html', {'form': form})


@login_required
def step_two(request):

    if request.method == 'POST':
        form = CustomFieldForm(request.POST)
        if form.is_valid():
            request.session['selected_options_columns'] = form.cleaned_data['options']
            return redirect('step_three')  # Leiten Sie zum nächsten Schritt weiter
    else:
        form = CustomFieldForm()

    return render(request, 'step_two.html', {'form': form})


@login_required
def step_three(request):
    return render(request, 'step_three.html')

@login_required
def download_data(request):
    # Implementieren Sie hier die Logik für den Download der Daten
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="example.csv"'
    # Schreiben Sie Daten in die Response
    response.write("id,name\n1,Example\n")
    return response

@login_required
def upload_data(request):
    if request.method == 'POST' and request.FILES['file_upload']:
        uploaded_file = request.FILES['file_upload']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(name)
        request.session['uploaded_csv_file_path'] = fs.path(name)  # Speichern des Pfads in der Session
        return redirect('step_four')
    return redirect('step_three')

@login_required
def step_four(request):
    csv_file_path = request.session.get('uploaded_csv_file_path', '')
    csv_headers = []
    csv_rows = []

    if csv_file_path:
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                csv_headers = next(reader)  # Erste Zeile als Header
                csv_rows = list(reader)
        except Exception as e:
            print(f"Fehler beim Lesen der CSV-Datei: {e}")
    else:
        print("Kein Dateipfad in der Session gefunden.")

    return render(request, 'step_four.html', {
        'csv_headers': csv_headers,
        'csv_rows': csv_rows,
    })


@login_required
def step_five(request):
    thread = Thread(target = update, args = (request, ))
    thread.start()

    return render(request, 'step_five.html')

@login_required
def progress(request):
    # Beispiel: Abrufen des Fortschritts aus der Session
    progress = request.session.get('progress', 0)
    print(progress)
    return JsonResponse({'progress': progress})

@login_required
def stop_process(request):
    request.session['stop_requested'] = True
    request.session.save()
    return JsonResponse({'status': 'stop_requested'})
