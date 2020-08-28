#include <Wire.h>
#include <VL53L1X.h>

#define PIN_MOTORA_IN1 5
#define PIN_MOTORA_IN2 6
#define PIN_MOTORB_IN1 10
#define PIN_MOTORB_IN2 11

#define SERIAL_BAUDRATE 115200
#define I2C_CLOCK 400000

VL53L1X sensor;
String inputBuffer = "";
bool inBegin = false;
bool inComplete = false;

void setup()
{
    /* Setup pins */
    pinMode(PIN_MOTORA_IN1, OUTPUT);
    pinMode(PIN_MOTORA_IN2, OUTPUT);
    pinMode(PIN_MOTORB_IN1, OUTPUT);
    pinMode(PIN_MOTORB_IN2, OUTPUT);

    /* Setup commmunication */
    Serial.begin(SERIAL_BAUDRATE);

// Remove for now since we can't test the sensor yet
#if (false)
    Wire.begin();
    Wire.setClock(I2C_CLOCK);

    /* Setup sensor */
    sensor.setTimeout(100);
    if (!sensor.init())
    {
        Serial.println("Failed to detect and initialize sensor!");
        while (1);
    }

    // TODO: Consider which distrance mode to use
    sensor.setDistanceMode(VL53L1X::Medium);
    // 50000 us (50 ms)
    sensor.setMeasurementTimingBudget(50000);

    // Start sensor, read every 50ms
    sensor.startContinuous(50);
#endif
}

// Honey?
// What?
// WHERE - IS - MY - SUPERLOOP
void loop()
{
    // If we have a complete command
    if (inComplete) {
        // Extract speeds
        byte inLeft = (byte)inputBuffer.charAt(0);
        byte inRight = (byte)inputBuffer.charAt(1);

        // Forwards
        // analogWrite(PIN_MOTORX_IN1, x);
        // analogWrite(PIN_MOTORX_IN2, 0);
        // Backwards
        // analogWrite(PIN_MOTORX_IN1, 0);
        // analogWrite(PIN_MOTORX_IN2, x);
        // for x between 0-255

        setSpeed(PIN_MOTORA_IN1, PIN_MOTORA_IN2, inLeft);
        setSpeed(PIN_MOTORB_IN1, PIN_MOTORB_IN2, inRight);

        // Clear out our command
        inputBuffer = "";
        inBegin = false;
        inComplete = false;
    }

    // Receive serial data if there is any and we don't
    // already have a complteed command
    while (Serial.available() && !inComplete) {
        char inChar = (char)Serial.read();
        if (inChar == ':') {
            inBegin = true;
            continue;
        }
        if (inChar == '\n') {
            inComplete = true;
        }
        if (inBegin) {
            inputBuffer += inChar;
        }
    }
    
    // TODO: Spin servo
    // TODO: Send LIDAR data

    delay(5);
}

void setSpeed(byte pinIn1, byte pinIn2, byte inByte) {
    if (inByte == 128) {
        analogWrite(pinIn1, 0);
        analogWrite(pinIn2, 0);
    } else if (inByte < 128) {
        analogWrite(pinIn1, 0);
        analogWrite(pinIn2, map(inByte, 128, 0, 0, 255));
    } else if (inByte > 128) {
        analogWrite(pinIn1, map(inByte, 128, 255, 0, 255));
        analogWrite(pinIn2, 0);
    }
}