#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>  // Pour les écrans LCD I2C
#include <LiquidCrystal_I2C.h>

const char* ssid = "Xarala"; //"Soxna maguette";
const char* password = "H@ckit21"; //"eeeeeeee";
const char* host = "192.168.1.146";
const int port = 8000;

#define SS_PIN D8
#define RST_PIN D3
#define BUZZER_PIN D4  // Broche pour le buzzer

MFRC522 rfid(SS_PIN, RST_PIN);

// Pour un écran LCD I2C
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Adresse I2C, nombre de colonnes, nombre de lignes

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(BUZZER_PIN, OUTPUT);  // Définir le buzzer comme sortie

  // Initialisation de l'écran LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Initialisation...");
  
  Serial.println();
  Serial.println("Connexion à " + String(ssid));
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connecté");

  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Lecteur RFID initialisé");
  lcd.clear();
  lcd.print("Prêt");
}

void loop() {
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    String uid = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
      uid += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
      uid += String(rfid.uid.uidByte[i], HEX);
    }
    Serial.print("UID RFID : ");
    Serial.println(uid);

    // Afficher l'UID sur l'écran LCD
    lcd.clear();
    lcd.print("UID RFID:");
    lcd.setCursor(0, 1);
    lcd.print(uid);

    // Activer le buzzer
    tone(BUZZER_PIN, 1000, 500);  // Son de 500ms

    sendPostRequest(uid);
  }

  // delay(1000);
}

void sendPostRequest(String uid) {
  WiFiClient client;
  
  if (!client.connect(host, port)) {
    Serial.println("Connexion échouée");
    return;
  }

  String url = "/receive_rfid_data/";
  String postData = "uid=" + uid;

  Serial.println("Envoi de la requête HTTP POST");
  client.println("POST " + url + " HTTP/1.1");
  client.println("Host: " + String(host));
  client.println("Content-Type: application/x-www-form-urlencoded");
  client.println("Content-Length: " + String(postData.length()));
  client.println();
  client.println(postData);

  while (client.available()) {
    String response = client.readStringUntil('\r');
    Serial.println(response);
  }
  delay(1000);
}
