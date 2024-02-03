from redminelib import Redmine
import os

def getConnection():
    REDMINE_URL = os.environ.get('REDMINE_URL', '')
    REDMINE_SECRET_KEY = os.environ.get('REDMINE_SECRET_KEY', '')
    redmine = Redmine(REDMINE_URL, key=REDMINE_SECRET_KEY)
    return redmine
