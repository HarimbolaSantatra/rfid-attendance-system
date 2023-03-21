/*
 
 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 *
  Utilisé pour tester le fonctionnement du module MFRC522 avec l'interface Seriel
 */

#include <SPI.h>
#include <MFRC522.h>
#include <Ethernet.h>

#define RST_PIN 9          // Configurable, see typical pin layout above
#define SS_PIN 10         // Configurable, see typical pin layout above
#define RED_LED 2
#define GREEN_LED 4

// Access 
  /*
   ID de nos RFID: mena et carte fotsy
   0C BD F3 16
   33 27 04 03
  */
String access_table[] = {" 0C BD F3 16", " 33 27 04 03"};
int len = 2;

MFRC522 rfid(SS_PIN, RST_PIN);  // Create MFRC522 instance

byte id[4];

void allowAccess(){
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, HIGH);
  delay(2000);
  digitalWrite(GREEN_LED, LOW);
  }
  
void denyAccess(){
  digitalWrite(RED_LED, HIGH);
  digitalWrite(GREEN_LED, LOW);
  delay(2000);
  digitalWrite(RED_LED, LOW);
  }

void blipTest(){
  digitalWrite(RED_LED, HIGH);
  delay(200);
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, HIGH);
  delay(200);
  digitalWrite(GREEN_LED, LOW);
}

bool isElementPresent(String table[], String element){
  for(int i=0; i<len; i++){
    if(element == table[i]){
      return true;
      break;
    }
  }
  return false;
}

void setup() {
  Serial.begin(9600);   // Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
  SPI.begin();      // Init SPI bus
  rfid.PCD_Init();   // Init MFRC522
  delay(20);       // Optional delay. Some board do need more time after init to be ready;
  rfid.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details

  // LED
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);

  blipTest();

}

void loop() {
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Enregistrement
  for (byte i = 0; i<4; i++){
    id[i] = rfid.uid.uidByte[i];
  }

  String content = "";
  byte letter;
  for (byte i = 0; i < rfid.uid.size ; i++){
    content.concat(String(rfid.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(rfid.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  
  
  if( isElementPresent(access_table, content) ){
    Serial.println(content);
    allowAccess();
  }
  else{
    Serial.println(content);
    denyAccess();
    }
  
  delay(2000); // delai de 2 secondes pour eviter les duplicata
  
  // RE-init RFID
  rfid.PICC_HaltA(); // Halt PICC
  rfid.PCD_StopCrypto1(); // Stop encryption on PCD
  
}
