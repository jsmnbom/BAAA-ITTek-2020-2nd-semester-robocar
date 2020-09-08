#include <Servo.h>
#include <Wire.h>
#include <VL53L1X.h>

#define PIN_MOTORA_IN1 11 //5
#define PIN_MOTORA_IN2 6 //6
#define PIN_MOTORB_IN1 5 //10
#define PIN_MOTORB_IN2 3 //11

#define SERIAL_BAUDRATE 115200
#define I2C_CLOCK 400000

VL53L1X sensor;

// Communication
String inputBuffer = "";
bool inBegin = false;
bool inComplete = false;

Servo myservo;
int pos = 90;
// True = Right
// False = Left     
bool direction = true;
byte step = 10;
byte minPos = 30;
byte maxPos = 60;

unsigned long lastReceived = 0;

unsigned long lastServoWrite = 0;
int lastPos = 30;

void setup()
{
    /* Setup pins */
    pinMode(PIN_MOTORA_IN1, OUTPUT);
    pinMode(PIN_MOTORA_IN2, OUTPUT);
    pinMode(PIN_MOTORB_IN1, OUTPUT);
    pinMode(PIN_MOTORB_IN2, OUTPUT);

    /* Setup commmunication */
    Serial.begin(SERIAL_BAUDRATE);

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
    sensor.setDistanceMode(VL53L1X::Short);
    // 50000 us (50 ms)
    sensor.setMeasurementTimingBudget(25000);

    // Start sensor, read every 50ms
    sensor.startContinuous(25);

    myservo.attach(9);
}

// Honey?
// What?
// WHERE - IS - MY - SUPERLOOP
void loop()
{
    unsigned long now = millis();
    // digitalWrite(PsIN_MOTORA_IN1, HIGH);
    // digitalWrite(PIN_MOTORA_IN2, LOW);
    // delay(2000);
    // digitalWrite(PIN_MOTORA_IN1, LOW);
    // digitalWrite(PIN_MOTORA_IN2, HIGH);
    // delay(2000);
    // digitalWrite(PIN_MOTORA_IN1, LOW);
    // digitalWrite(PIN_MOhttps://prod.liveshare.vsengsaas.visualstudio.com/join?0C888621D787C1CDA324240769E2AF72F4A5TORA_IN2, LOW);
    // delay(2000);
    // while(1);

    // If we have a complete command
    if (inComplete) {
        switch(inputBuffer.charAt(0)) {
            case 'd': {
                // Extract speeds
                byte inLeft = (byte)inputBuffer.charAt(1);
                byte inRight = (byte)inputBuffer.charAt(2);

                setSpeed(PIN_MOTORA_IN1, PIN_MOTORA_IN2, inLeft);
                setSpeed(PIN_MOTORB_IN2, PIN_MOTORB_IN1, inRight);
            } break;
            case 's': {
                byte inMinPos = (byte)inputBuffer.charAt(1);
                byte inMaxPos = (byte)inputBuffer.charAt(2);
                byte inStep = (byte)inputBuffer.charAt(3);

                minPos = inMinPos;
                maxPos = inMaxPos;
                step = inStep;

                pos = (minPos + maxPos) / 2;
                myservo.write(pos);
            }
        }

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
        lastReceived = now;
    }



    if (sensor.dataReady() && lastServoWrite + 3 * abs(pos - lastPos) + 25 < millis()) {
        int sensorData = sensor.read(false);
        Serial.write(':');
        Serial.write(pos);
        // Serial.write('!');
        byte first = sensorData >> 8;
        byte second = sensorData & B11111111;
        Serial.write(second);
        Serial.write(first);

        // Serial.print(sensorData);
        // Serial.print(" first: ");
        // Serial.print(first);
        // Serial.print(" second: ");
        // Serial.print(second);
        Serial.write('\n');

        lastPos = pos;

        if(pos <= minPos || pos >= maxPos){
            direction = !direction;
        }
        if (direction) {
            pos += step;
        } else {
            pos -= step;
        }
        pos = constrain(pos, minPos, maxPos);

        myservo.write(pos);
        // Serial.print("Left: ");
        // Serial.print(inLeft);
        // Serial.print("  right: ");
        // Serial.println(inRight);  
        
        // Serial.println(pos);

        lastServoWrite = millis();
    }
    
    
    if (lastReceived + 10000 >= now) {
        // while(1);
    }


    delay(5);
}

void setSpeed(byte pinIn1, byte pinIn2, byte inByte) {
    if (inByte == 128) {
        analogWrite(pinIn1, 0);
        analogWrite(pinIn2, 0);
    } else if (inByte < 128) {
        digitalWrite(pinIn1, LOW);
        analogWrite(pinIn2, map(inByte, 128, 0, 80, 255));
    } else if (inByte > 128) {
        analogWrite(pinIn1, map(inByte, 128, 255, 80, 255));
        digitalWrite(pinIn2, LOW);
    }
}