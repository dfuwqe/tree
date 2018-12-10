#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    300
#define BRIGHTNESS  128
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS] ={CRGB::Black};
//uint8_t brightness[NUM_LEDS];
//String lastCommand;

CRGBPalette16 currentPalette;
//extern const TProgmemPalette256 palette PROGMEM;

char buf[2*NUM_LEDS];
void setup() {
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.setBrightness(  BRIGHTNESS );
    FastLED.setMaxPowerInVoltsAndMilliamps(5,5000);
    Serial.begin(250000);     
    currentPalette = RainbowColors_p;
    FastLED.show(); 
}


void loop()
{
    int remaining = 2*NUM_LEDS;
    int recved = 0;
    //On receiving serial input change color, otherwise remain same.
//     while (!Serial.available()) {}
     if(Serial.available() > 0) {
        while(remaining > 0){
           recved = Serial.readBytes(buf,remaining);
           remaining -= recved;
        }
        
        FillLEDsFromPaletteColors(buf);
        FastLED.show();   
//        Serial.print("\n");
     }
}

void FillLEDsFromPaletteColors( char* colorCommands)
{
    char t1, t2;
    int c1,c2;
    for( int i = 0; i < NUM_LEDS; i++) {
       t1 = colorCommands[2*i];
       t2 = colorCommands[2*i+1];
       c1 = (int) t1;
       c2 = (int) t2;
      if(c1 == 0 ||c1 == 99|| c1 == 255){
        leds[i] = CRGB::Black;
      }
      else if(c1 <= 32){
        leds[i] = CRGB::Azure;
        leds[i].fadeToBlackBy(250);
      }
      else{
        leds[i] = ColorFromPalette( currentPalette, c2,192,LINEARBLEND);
        fadeTowardColor(leds[i], CRGB::Azure, 8*(64-c1)); //color gradient
      }
    }
}

// Blend one CRGB color toward another CRGB color by a given amount.
// Blending is linear, and done in the RGB color space.
// This function modifies 'cur' in place.
CRGB fadeTowardColor( CRGB& cur, const CRGB& target, uint8_t amount)
{
  nblendU8TowardU8( cur.red,   target.red,   amount);
  nblendU8TowardU8( cur.green, target.green, amount);
  nblendU8TowardU8( cur.blue,  target.blue,  amount);
  return cur;
}

// Helper function that blends one uint8_t toward another by a given amount
void nblendU8TowardU8( uint8_t& cur, const uint8_t target, uint8_t amount)
{
  if( cur == target) return;
  
  if( cur < target ) {
    uint8_t delta = target - cur;
    delta = scale8_video( delta, amount);
    cur += delta;
  } else {
    uint8_t delta = cur - target;
    delta = scale8_video( delta, amount);
    cur -= delta;
  }
}

