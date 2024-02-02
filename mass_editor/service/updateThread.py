from time import sleep
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import csv

def update(request):
    csv_file_path = request.session.get('uploaded_csv_file_path', '')
    request.session['stop_requested'] = False
    print(csv_file_path)
    if not csv_file_path:
        return redirect('step_three')

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            csv_headers = next(reader)  # Erste Zeile als Header
            csv_rows = list(reader)

            csvSize = len(csv_rows)
            print(csvSize)
            progressedRows = 0
            for row in csv_rows:
                # Prüfen, ob ein Stopp angefordert wurde
                if request.session.get('stop_requested', False):
                    print("Stopp angefordert, beende die Verarbeitung.")
                    break  # Beendet die Schleife, wenn Stopp angefordert wurde

                print(row)
                sleep(1)  # Simuliert eine langsame Verarbeitung jeder Zeile
                progressedRows += 1
                progress = progressedRows * 100 / csvSize
                print(progress)

                # Aktualisieren des Fortschritts in der Session
                request.session['progress'] = progress
                request.session.save()

    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")
        return HttpResponse("Ein Fehler ist aufgetreten", status=500)
    
    # Bereinigung
    del request.session['uploaded_csv_file_path']
    del request.session['progress']
    request.session.save()






