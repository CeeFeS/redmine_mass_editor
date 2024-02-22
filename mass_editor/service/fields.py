from redminelib import Redmine
from .redmine import getConnection

def getAllFields():
    # Definieren der festen Felder als Tupel von (Schlüssel, Menschlich lesbare Bezeichnung)
    fixed_fields = [
        ('ticket_id', 'Ticket ID'),
        ('tracker_id', 'Tracker'),
        ('project_id', 'Project ID'),
        ('subject', 'Subject'),
        ('status_id', 'Status ID'),
        ('description', 'Description'),
    ]
    
    # Initialisieren der Liste der Felder mit den festen Feldern
    fields = fixed_fields.copy()

    # Hinzufügen der benutzerdefinierten Felder aus der Datenbank
    for customField in getConnection().custom_field.all():
        # Annahme: customField hat Attribute 'id' und 'name'
        field_tuple = ("cf_"+str(customField.id), customField.name)
        fields.append(field_tuple)

    return fields

def getFieldNameById(field_id):
    for field in getAllFields():
        if str(field[0]) == str(field_id):  # Konvertieren beider IDs in Strings für den Vergleich
            return field[1]
    return None


def getFieldIdByName(field_name):
    for field in getAllFields():
        if str(field[1]) == str(field_name):  # Konvertieren beider IDs in Strings für den Vergleich
            return field[0]
    return None