/* 
*  Mashed together by George in 2014.
*  
*  Vast majority of this is ripped straight from here:
*  https://www.openhomeautomation.net/wireless-relay-arduino-wifi/
*  
*  which uses the brilliant API here:
*  https://github.com/marcoschwartz/aREST
*  
*  With some bits taken from here:
*  https://learn.adafruit.com/rgb-led-strips/overview
*  
*  Particularly this very useful wiring diagram:
*  https://learn.adafruit.com/rgb-led-strips/usage
*  
*/

// Include required libraries
#include <Adafruit_CC3000.h>
#include <SPI.h>
#include <CC3000_MDNS.h>
#include <aREST.h>

// Define CC3000 chip pins
#define ADAFRUIT_CC3000_IRQ   3
#define ADAFRUIT_CC3000_VBAT  5
#define ADAFRUIT_CC3000_CS    10

// WiFi network (change with your settings !)
#define WLAN_SSID       "FibreOptipus"
#define WLAN_PASS       "boondoghotcakes"
#define WLAN_SECURITY   WLAN_SEC_WPA2

// The port to listen for incoming TCP connections 
#define LISTEN_PORT           80

// Create CC3000 instances
Adafruit_CC3000 cc3000 = Adafruit_CC3000(ADAFRUIT_CC3000_CS, ADAFRUIT_CC3000_IRQ, ADAFRUIT_CC3000_VBAT,
                                         SPI_CLOCK_DIV2);                                                                         

// Server instance
Adafruit_CC3000_Server restServer(LISTEN_PORT);

// DNS responder instance
MDNSResponder mdns;

// Create aREST instance
aREST rest = aREST();

#define REDPIN 6
#define GREENPIN 8
#define BLUEPIN 9

int pins[] = {REDPIN, GREENPIN, BLUEPIN};

// Relay pin

int setRGBVals(String rgbVals) {
  Serial.println("setting RGB to: ");
  Serial.println(rgbVals);
  for(int i=0;i<=3;i++){
      String v = rgbVals.substring(i*3,(i+1)*3);
      analogWrite(pins[i], v.toInt());
  }
  return 1;
}

void setup() {
  
  // Initialize Serial 
  Serial.begin(115200);
  Serial.println(F("Begin..."));

  // Set name & ID
  rest.set_name("relay_control");
  rest.set_id("1");
  rest.function("setRGBVals", setRGBVals);



  // Define RGB pins as output

  for(int i=0;i<=3;i++){
      pinMode(pins[i], OUTPUT);
      analogWrite(pins[i], 10);
  }
  
  // Set up CC3000 and get connected to the wireless network.
  if (!cc3000.begin())
  {
    while(1);
  }
  Serial.println(F("cc3000 begin done..."));

  
  if (!cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY)) {
    while(1);
  }

  Serial.println(F("Connected to AP.."));

  while (!cc3000.checkDHCP())
  {
    delay(100);
  }

  Serial.println(F("Connected, printing IP..."));

  // Print CC3000 IP address
  while (! displayConnectionDetails()) {
    delay(1000);
  }

  Serial.println(F("Begin DNS responder..."));

  // Start multicast DNS responder
  if (!mdns.begin("arduino", cc3000)) {
    while(1); 
  }

  Serial.println(F("Start server..."));
  
  // Start server
  restServer.begin();
  Serial.println(F("Listening for connections..."));

}

void loop() {
  
  // Handle any multicast DNS requests
  mdns.update();
  
  // Handle REST calls
  Adafruit_CC3000_ClientRef client = restServer.available();
  rest.handle(client);

}

// Print connection details of the CC3000 chip
bool displayConnectionDetails(void)
{
  uint32_t ipAddress, netmask, gateway, dhcpserv, dnsserv;
  
  if(!cc3000.getIPAddress(&ipAddress, &netmask, &gateway, &dhcpserv, &dnsserv))
  {
    Serial.println(F("Unable to retrieve the IP Address!\r\n"));
    return false;
  }
  else
  {
    Serial.print(F("\nIP Addr: ")); cc3000.printIPdotsRev(ipAddress);
    Serial.print(F("\nNetmask: ")); cc3000.printIPdotsRev(netmask);
    Serial.print(F("\nGateway: ")); cc3000.printIPdotsRev(gateway);
    Serial.print(F("\nDHCPsrv: ")); cc3000.printIPdotsRev(dhcpserv);
    Serial.print(F("\nDNSserv: ")); cc3000.printIPdotsRev(dnsserv);
    Serial.println();
    return true;
  }
}
