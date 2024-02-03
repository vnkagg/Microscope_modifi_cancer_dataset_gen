#include <Adafruit_DotStarMatrix.h>
#include <Adafruit_DotStar.h>
#include <Fonts/TomThumb.h>

#define DATAPIN    5
#define CLOCKPIN   6
#define BRIGHTNESS_PIN A0  // Analog pin for brightness control

Adafruit_DotStarMatrix matrix = Adafruit_DotStarMatrix(
                                  12, 6, DATAPIN, CLOCKPIN,
                                  DS_MATRIX_BOTTOM     + DS_MATRIX_LEFT +
                                  DS_MATRIX_ROWS + DS_MATRIX_PROGRESSIVE,
                                  DOTSTAR_BGR);

const uint16_t adaColors[] = {
  matrix.Color(255, 0, 0),   // Red
  matrix.Color(0, 255, 0),   // Green
  matrix.Color(0, 0, 255)    // Blue
};

char adafruit[] = "ADAFRUIT!";
int x = matrix.width();
int brightness = 128;
bool constantColorMode = false;

void setup() {
  Serial.begin(115200);
  matrix.begin();
  matrix.setFont(&TomThumb);
  matrix.setTextWrap(false);
}
int interval = 0;
String colorCode = "";
String intervalStr;  // Declare intervalStr outside of the switch
void loop() {
  // Check for serial input
  
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'W': // Constant color mode
        colorCode = Serial.readStringUntil('\n');
        constantColorMode = true;
        break;
      case 'B': // Blink mode
        intervalStr = Serial.readStringUntil('\n'); 
        interval = intervalStr.toInt();
        constantColorMode = false;
        break;
      case 'L':
        brightness = Serial.readStringUntil('\n').toInt();
        setBrightness(brightness);
        break;
    }
  }

  // Update based on the mode
  if (constantColorMode) {
    constantColor(colorCode);
  } else {
    blinkRGB(interval);
  }
}

void constantColor(String colorCodeHex) {
  long number = strtol(&colorCodeHex[1], NULL, 16); // Convert hex to long
  int r = number >> 16;  // Extract the red component
  int g = number >> 8 & 0xFF; // Extract the green component
  int b = number & 0xFF;  // Extract the blue component

  uint32_t color = matrix.Color(r, g, b);
  matrix.fillScreen(color);
  matrix.show();
}

void blinkRGB(int interval) {
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();
  static int i = 0;  // Static variable to remember the current color index

  if (currentMillis - previousMillis >= interval * 1000) {
    previousMillis = currentMillis;
    uint32_t color = adaColors[i];  // Get the current color
    matrix.fillScreen(color);
    matrix.show();

    i = (i + 1) % 3;  // Rotate to the next color (Red -> Green -> Blue)
  }
}

void setBrightness(int brightness) {
//  brightness = map(level, 0, 9, 0, 255);
  matrix.setBrightness(brightness);
  matrix.show();
}
