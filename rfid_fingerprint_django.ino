#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

const char* ssid = "Xarala";
const char* password = "H@ckit21";
const char* host = "192.168.1.175";  // Adresse IP de votre serveur Django
const int port = 8000;  // Port utilisé par votre serveur Django

#define SS_PIN D8
#define RST_PIN D3
MFRC522 rfid(SS_PIN, RST_PIN);

#define Finger_Rx 12 //D5
#define Finger_Tx 14 // D6
SoftwareSerial mySerial(12, 14);

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

String Event_Name = "Fingerprint";
String Key = "dn2QeEZAcWFFqwDdAitOyY";
const char* server = "maker.ifttt.com";
String resource = "/trigger/" + Event_Name + "/with/key/" + Key;

const char* NAME; // Variable pour le nom à envoyer à IFTTT
const char* ID;   // Variable pour l'ID à envoyer à IFTTT
// Function prototype for sendPostRequest
void sendPostRequest(String uid, String fingerprintID);


void setup() {
  Serial.begin(115200);
  mySerial.begin(57600);

  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connecté");

  SPI.begin();
  rfid.PCD_Init();
  finger.begin(57600);
  
  if (finger.verifyPassword()) {
    Serial.println("Capteur d'empreintes digitales trouvé !");
  } else {
    Serial.println("Capteur d'empreintes digitales non trouvé :(");
    while (1);
  }

  finger.getTemplateCount();
  Serial.print("Le capteur contient "); Serial.print(finger.templateCount); Serial.println(" templates");
  Serial.println("En attente d'une empreinte digitale valide...");

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
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
    sendPostRequest(uid, ""); // Envoi des données RFID avec ID de l'empreinte vide
  }
  
  String uid= "gfgedyhnb";
  Serial.print("UID RFID : ");
  Serial.println(uid);
  sendPostRequest(uid, ""); // Envoi des données RFID avec ID de l'empreinte vide


  // Lecture des empreintes digitales
  getFingerprintIDez(); // Récupération de l'ID de l'empreinte digitale
  if (finger.fingerID != 0 && finger.confidence >= 60) {
    // Assignation des valeurs NAME et ID en fonction de finger.fingerID
    switch (finger.fingerID) {
      case 1:
        NAME = "khady thiaw";
        ID = "1";
        break;
      case 2:
        NAME = "maguette seye";
        ID = "2";
        break;
      case 3:
        NAME = "MAG";
        ID = "3";
        break;
      case 4:
        NAME = "oumy thiam";
        ID = "4";
        break;
      case 5:
        NAME = "fatima sene";
        ID = "5";
        break;
      default:
        break;
    }
    Serial.println("Attendace Marquée pour : ");
    Serial.println("********************************************************************************************");
    Serial.println(NAME);
    Serial.println("********************************************************************************************");
    Serial.println("Attendace Marquée pour : ");
    makeIFTTTRequest(); // Envoi des données d'empreinte digitale à IFTTT
    sendPostRequest("", String(finger.fingerID)); // Envoi de l'ID de l'empreinte digitale avec UID vide
    finger.fingerID = 0; // Réinitialisation de l'empreinte digitale ID après envoi
  }

  delay(1000);  // Attente avant la prochaine itération
}

void sendPostRequest(String uid, String fingerprintID) {
  WiFiClient client;
  
  if (!client.connect(host, port)) {
    Serial.println("Connexion échouée");
    return;
  }

  String url = "/receive_rfid_data/";
  String postData = "uid=" + uid+ "&fingerprint_id=" + fingerprintID;

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

void makeIFTTTRequest() {
  Serial.print("Connecting to ");
  Serial.print(server);

  WiFiClient client;
  int retries = 5;
  while (!!!client.connect(server, 80) && (retries-- > 0)) {
    Serial.print(".");
  }
  Serial.println();
  if (!!!client.connected()) {
    Serial.println("Failed to connect...");
  }

  Serial.print("Request resource: ");
  Serial.println(resource);

  String jsonObject = String("{\"value1\":\"") + NAME + "\",\"value2\":\"" + ID + "\"}";

  client.println(String("POST ") + resource + " HTTP/1.1");
  client.println(String("Host: ") + server);
  client.println("Connection: close\r\nContent-Type: application/json");
  client.print("Content-Length: ");
  client.println(jsonObject.length());
  client.println();
  client.println(jsonObject);

  int timeout = 5 * 10; // 5 seconds
  while (!!!client.available() && (timeout-- > 0)) {
    delay(100);
  }
  if (!!!client.available()) {
    Serial.println("No response...");
  }
  while (client.available()) {
    Serial.write(client.read());
  }

  Serial.println("\nclosing connection");
  client.stop();
}

uint8_t getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;

  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID;
}

