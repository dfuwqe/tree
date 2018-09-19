#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    60
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];


void setup() {
    Serial.begin(250000);
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.setBrightness(  BRIGHTNESS );   
}


void loop()
{
    //On receiving serial input change color, otherwise remain same.
     if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
//        Serial.println(input);
        FillLEDsFromPaletteColors(input);
        FastLED.show();
        
     }
}

void FillLEDsFromPaletteColors( String colorCommands)
{
 
    for( int i = 0; i < NUM_LEDS; i++) {
        switch (colorCommands[i]){
          case '0':
            leds[i] = CRGB::Black;
            break;
          case '1':
            leds[i] = CRGB::Green;
            break;
          case '2':
            leds[i] = CRGB::Red;
        }
    }
}

