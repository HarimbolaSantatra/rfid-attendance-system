import serial
import re  # regular expression

# Import Django setting is required for Django to recognize all config
import django
from rfid.wsgi import *
from mainapp.models import User, AttendanceRecord

# Serial port name
device = '/dev/ttyACM0'
"""
For Windows, mine is COM4.
For Ubuntu, run the command: sudo dmesg | grep tty
de izay misy oe USB tao fotsiny no nojereko: dans ce cas: ttyACM0.
Le izy fichier, noho izany atao sous-forme: /dev/ttyACM0
Avy eo, misy "permission denied", de mila atao 6 ou 7 ny permission ny 'world':
        sudo chmod 666 :dev/ttyACM0
Problème hafa dia very ilay permission rehefa asorina ilay zavatra @le port.
Solution fixe mobla tsy nadramako: ajouter user au groupe 'dialout':
    sudo usermod -a -G dialout santatra
"""

arduino_port = serial.Serial(device, 9600, timeout=30)
print("\n---------------------------------------")
print(f'Connection à {device}... Connected !!')

# Regular Expression: id_pattern est le pattern d'un identifiant
# pour référence: " 0C BD F3 16 " et "33 27 04 03"
id_pattern = re.compile(r"[0-9A-F][0-9A-F]\s[0-9A-F][0-9A-F]\s[0-9A-F][0-9A-F]\s[0-9A-F][0-9A-F]")

# Liste des ID acceptés
accepted_id_dict = list(User.objects.filter(status='a').values('card_id'))  # Forme: list de dict

# Liste des cards
cards_id_list = list(User.objects.values('card_id'))  # Format: list de dict
cards_list = []
for dict_element in cards_id_list:
    for k, v in dict_element.items():
        cards_list.append(v)

while True:
    port_data = arduino_port.readline()
    """
    data est en byte alors il faut convertir. Néanmoins, decode n'enlève pas les escapes sentences
    alors on utilise .strip()
    """
    port_data = port_data.decode('utf-8').strip().strip('\n')

    # mo: match object; for regex match
    mo = id_pattern.search(port_data)

    print("\n------------------------------")
    print('OBJECT: ', mo)
    if mo is None:
        # if there's no match for an ID
        print("NO MATCH for: ", port_data)
        id_value = None
    else:
        # id_value est l'id du carte extrait du port seriel
        id_value = mo.group()

        """"
        cards_list contient un liste des objets User où le card_id = id_value.
        Il ne doit y avoir qu'un seul exemplaire s'il existe,
        alors on prend le premier element du list.
        cards_list peut être vide.
        """

        # Verifier si ID extrait est dans la liste des ID accepté
        if id_value in cards_list:
            # objet est le premier object dans le liste des object ayant comme id=id_value
            # On a pris le premier car si plusieurs objets de même ID existe, ces objets osnt considérés les mêmes
            objet = User.objects.filter(card_id=id_value)[0]
            print("Saving to database ...", end='')
            data_saved = AttendanceRecord(user=objet)
            data_saved.save()
            print("Saved!")
        else:
            print("Card not in the database !")
            user_saved = User(
                name="Unknown",
                card_id=id_value,
                status='r',
            )
            user_saved.save()
            data_saved = AttendanceRecord(user=user_saved)
            data_saved.save()
            print("Saved!")

