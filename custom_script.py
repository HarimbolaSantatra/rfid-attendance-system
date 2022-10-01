# Import Django setting is required for Django to recognize all config
import django
from rfid.wsgi import *
from mainapp.models import User, AttendanceRecord

""" ATAOVY ATO IZAY SCRIPT DE TEST """

user_input = input('Enter the AttendanceRecord input: ')

# Check if id_value exists in database: add record instance; else deny access
list_w_card = User.objects.filter(card_id=user_input)
if user_input == list_w_card[0].card_id:
    objet = list_w_card[0]
    print("Object to save: ", objet)
    data_saved = AttendanceRecord(user=objet)
    data_saved.save()
    print("Saved !")
else:
    print("No instance.")
