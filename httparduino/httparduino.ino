#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <SPI.h>
#include <MFRC522.h>

const char* ssid = "Xarala";
const char* password = "H@ckit21";
const char* host = "192.168.1.65";  // Adresse IP de votre serveur Django
const int port = 8000;  // Port utilisé par votre serveur Django

#define SS_PIN D8
#define RST_PIN D3
MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connexion au réseau WiFi
  Serial.println();
  Serial.println("Connexion à " + String(ssid));
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connecté");

  // Initialisation du lecteur RFID
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Lecteur RFID initialisé");
}

void loop() {
  // Lecture RFID
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    String uid = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
      uid += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
      uid += String(rfid.uid.uidByte[i], HEX);
    }
    Serial.print("UID RFID : ");
    Serial.println(uid);
    sendPostRequest(uid);
  }

  delay(1000);  // Attente avant la prochaine itération
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
  delay(10);
}
