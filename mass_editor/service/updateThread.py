from time import sleep
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .fields import getFieldIdByName
import pandas as pd
from .redmine import getConnection



def filterTicket(identifierKeys, identifierValues):
    if len(identifierKeys) != len(identifierValues):
        raise ValueError("Arrays 'identifierKeys' und 'identifierValues' müssen die gleiche Länge haben")

    if "ticket_id" in identifierKeys:
        issues = getConnection.issue.get(34441, include=['children', 'journals', 'watchers'])
    else:
        filter_dict = {}
        for key, value in zip(identifierKeys, identifierValues):
            filter_dict[key] = value

    # Verwenden des filter_dict, um Issues zu filtern
        issues = getConnection.issue.filter(**filter_dict)

    return issues

def prepare_filter_conditions(df, selected_options):
    # Extrahieren der Spaltennamen (Identifier Keys) aus der DataFrame
    identifierKeys = list(df.columns)
    
    # Initialisieren der Liste für die Identifier Values, die für jede Zeile gefüllt wird
    identifierValues = []
    
    # Iterieren durch die DataFrame und Sammeln der Werte für die nicht ausgewählten Felder
    for index, row in df.iterrows():
        # Filtern der Werte basierend auf den nicht ausgewählten Identifier Keys
        row_values = [str(row[key]) for key in identifierKeys if key not in selected_options]
        identifierValues.append(row_values)
    
    return identifierValues



def update(request):
    csv_file_path = request.session.get('uploaded_csv_file_path', '')
    request.session['stop_requested'] = False
    identifierKeys = request.session.get('selected_options_identifier', [])
    print(csv_file_path)
    if not csv_file_path:
        return redirect('step_three')

    try:
        # Lesen der CSV-Datei mit Pandas
        df = pd.read_csv(csv_file_path, delimiter=';', encoding='utf-8')

        print(df)

        csvSize = len(df)
        progressedRows = 0

        identifierValuesList = prepare_filter_conditions(df, identifierKeys)

        for identifierValues in identifierValuesList:
            # Prüfen, ob ein Stopp angefordert wurde
            if request.session.get('stop_requested', False):
                print("Stopp angefordert, beende die Verarbeitung.")
                break  # Beendet die Schleife, wenn Stopp angefordert wurde
            
            # Filtern der Tickets basierend auf der aktuellen Zeile (Identifier Values)
            # Hinweis: Ersetzen Sie 'filterTicket' durch Ihre eigentliche Funktion und Logik

            #TODO: Funktioniert noch nicht
            print(identifierValues)
            #filterTicket(identifierKeys, identifierValues)

            progressedRows += 1
            progress = progressedRows * 100 / csvSize

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






