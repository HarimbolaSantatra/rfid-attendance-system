import serial
import re  # regular expression

# Import Django setting is required for Django to recognize all config
import django
from rfid.wsgi import *
# from mainapp.models import User, AttendanceRecord

# Serial port name
"""
For Windows, mine is COM4.
For Ubuntu, run the command: sudo dmesg | grep tty
de izay misy oe USB tao fotsiny no nojereko: dans ce cas: ttyACM0.
Le izy fichier, noho izany atao sous-forme: /dev/ttyACM0
Avy eo, misy "permission denied", de mila atao 6 ou 7 ny permission ny 'world'
Problème hafa dia very ilay permission rehefa asorina ilay zavatra @le port.
Solution fixe mobla tsy nadramako: ajouter user au groupe 'dialout':
    sudo usermod -a -G dialout santatra
"""

device = '/dev/ttyACM0'
arduino_port = serial.Serial(device, 9600, timeout=30)
print("\n---------------------------------------")
print(f'Connection à {device}... Connected !!')

# Regular Expression: id_pattern est le pattern d'un identifiant
# pour référence: " 0C BD F3 16 " et "33 27 04 03"
id_pattern = re.compile(r"[0-9A-F][0-9A-F]\s[0-9A-F][0-9A-F]\s[0-9A-F][0-9A-F]\s[0-9A-F][0-9A-F]")

while True:
    port_data = arduino_port.readline()
    """
    data est en byte alors il faut convertir. Néanmoins, decode n'enlève pas les escapes sentences
    alors on utilise .strip()
    """
    port_data = port_data.decode('utf-8').strip().strip('\n')

    mo = id_pattern.search(port_data)

    print("\n------------------------------")
    print('OBJECT: ', mo)
    if mo is None:
        print("NO MATCH for ", port_data)
        id_value = None
    else:
        id_value = mo.group()
        print("MATCH !! - ", port_data)
