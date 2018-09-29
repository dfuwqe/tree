#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    60
#define BRIGHTNESS  64
#define LED_TYPE    WS2812
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];
uint8_t brightness[NUM_LEDS];
String lastCommand;

CRGBPalette16 currentPalette;
//extern const TProgmemPalette256 palette PROGMEM;

void setup() {
    Serial.begin(250000);
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.setBrightness(  BRIGHTNESS );     
    currentPalette = RainbowColors_p;
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
      int c = int(colorCommands[i]);
//      Serial.print(c);
      if(c == 0)
        leds[i] = CRGB::Black;
      else{ 
        if(colorCommands[i]==lastCommand[i]){
          if(brightness[i]<32)
            brightness[i] = 0;
          else
            brightness[i]-=32;
        }
        else
          brightness[i] = 255;
        leds[i] = ColorFromPalette( currentPalette, c,brightness[i],LINEARBLEND);
      }
    }
    lastCommand = colorCommands;
//    Serial.print("\n");
}

