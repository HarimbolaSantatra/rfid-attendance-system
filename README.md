# RFID based attendance system
A RFID based attendance system is a automatic attendance system which use RFID card to save a person identity in a database when he/she enter an area.

RFID (__Radio-Frequency Identification__) uses electromagnetic fields to identify an object.

We're using an Arduino micro controller here to obtain the data from the RFID card and sends it to the sofware.

Data in an RFID card is unique. In our case, it's in the format __XX XX XX XX__ where X is an integer.

## Screenshots
(Sorry for the french language in the screenshots ) :sweat_smile:
![screenshot_1][login]
![screenshot_2][homepage]
![screenshot_3][add_user]
![screenshot_4][attendance_list]

## RFID System
I won't explain the full functionality of an RFID based system here because I'm more focused on the software side :sweat_smile: and because everyone can design the electrical part as they want. I'll just explain what I did briefly. 

There are some useful resources at the end of this document for these who want to dig deeper. :wink:

A basic system is shown here:

![rfid_system][rfid_system]

From upper-left, the data from the RFID reader is read by the Arduino. Next, the Arduino send it to the Django application. Finally, a user interact with our system via a web interface.

## Electrical circuit
We use Arduino Uno for this project but any Arduino board will do.

Of course, we need a RFID card reader. We just use a popular Arduino module for this: the [MFRC522][3].

![mfrc_522][mfrc_522]

Finally, here's the full circuit (made with Proteus):

![circuit][circuit]
  
## Serial Port
The file **serial_rfid_test.py** is to test if the Arduino board successfully play as an intermediate between the RFID and the software.
So before everything, we must know the name of the port where the Arduino is plugged in. We can use the Arduino's IDE for this.
For Windows, the port's name is in COM* format, where \* is an integer (e.g: COM4).

For Ubuntu, run the command: 

	sudo dmesg | grep tty

and just look at the result which contains USB in it. For example, mine is in the format ttyACM0. In Ubuntu, the file is at */dev/ttyACM0*.

When we found it, we must alter its permission so the the board can read/write to it.

	sudo chmod 776 /dev/ttyACM0

Note that the last configuration we just did will be lost if the board is disconnected. So to permanently fix this, you can add the current user to the 'dialout' group. (Note that I haven't test it myself ! :sweat_smile: )

	sudo usermod -a -G dialout <username>

## Installation
Install all the necessary python package:

	pip install -r requirements.txt

Clone this repository:
	
	git clone https://github.com/HarimbolaSantatra/rfid-attendance-system.git

Launch Django

	cd rfid-attendance-system
	python manage.py runserver

## Database
We use SQLite, which is built inside Django.

## Files
### serial_rfid_test.py
As I said, its purpose is to test the connection Arduino-RFID-application. 

After the line:

	port_data = arduino_port.readline()

*port_data* contains data in bytes, so we must decode it to UTF-8. 

	port_data = port_data.decode('utf-8').strip().strip('\n')	

The *decode* method doesn't remove escape sentences, so we must use the *strip* method.

Everything we do after this is to use regular expression to extract the XX XX XX XX pattern.

### list_rfid.txt
Contains an list of the card id that will be accepted or refused. It's all example we use in this program so you can recognize it.

### main/main.ino
This is the Arduino file for the program inside it.

## Resources:
For Python & Django:
- Read/Write data to serial port in Python using pySerial: [pySerial Short Introduction][1] 
- [Django documentation][2] (Very good ! :grin:)

For RFID tutorials:
- [RFID][6] - Wikipedia
- [Security Access using MFRC522 RFID][4]
- [Interfacing RFID Reader With Arduino][5]

## License
This project is licensed under the terms of the MIT license.


[1]: https://pyserial.readthedocs.io/en/latest/shortintro.html
[2]: https://docs.djangoproject.com/en/4.1/
[3]: https://github.com/miguelbalboa/rfid
[4]: https://randomnerdtutorials.com/security-access-using-mfrc522-rfid-reader-with-arduino/
[5]: https://circuitdigest.com/microcontroller-projects/interfacing-rfid-reader-module-with-arduino
[6]: https://en.wikipedia.org/wiki/Radio-frequency_identification

[rfid_system]: img_readme/rfid_system.jpg
[login]:  img_readme/login_page.png
[homepage]:  img_readme/homepage.png
[add_user]:  img_readme/add_user.png
[attendance_list]:  img_readme/attendance_list.png
[mfrc_522]: img_readme/rc522.JPG
[circuit]: img_readme/circuit.JPG
