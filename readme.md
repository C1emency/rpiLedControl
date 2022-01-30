# Raspberry Pi LED control

## Description
This python module aims to provide an easy way to control RGB LED (strips) from the raspberry pi. Apart from setting fixed RGB colors, a multithreaded fade function enables to fade from the current color to a target color within a given time. Color is set using PWM.It is assumed you have three GPIO pins for red, green and blue.

Default Pin assignment (RPI 3b)
* Red - Pin  16
* Green - Pin 20
* Blue - Pin 21

## Usage Example

```
>>> import led as l
>>>
>>> # Initialization
>>> red = l.Color(255,0,0)
>>> green = l.Color(0,255,0)
>>> blue = l.Color(0,0,255)
>>> stripColor = l.Color(0,0,0)
>>> strip = l.LedStrip(stripColor,pin_r=16,pin_g=20,pin_b=21)
>>>
>>> # Playing around
>>> stripColor.set(10,120,60) # change color instantly
>>> stripColor.g = 0 # change only one component of color
>>> stripColor.fade(red,10) # fade to red in 10 seconds
>>> strip.off() # turn LEDs off
>>> strip.on() # turn LEDS on

```
