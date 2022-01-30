import pigpio
import time
from threading import Thread

class Color():

        def __init__(self,r=0,g=0,b=0) -> None:
                """RGB Color (Range 0-255)"""
                self._r = r
                self._g = g
                self._b = b

                self.subscribers = []
                self.runningThreads = []

        def set(self,r,g,b):
                self.r=r
                self.g=g
                self.b=b

        def subscribe(self,callback):
                """subscribed LedStrips will have this color"""

                if callback not in self.subscribers:
                        self.subscribers.append(callback)

        def unsubscribe(self,callback):
                """removes LedStrip subscribers"""

                newSubscribers = []
                for item in self.subscribers:
                        if item != callback:
                                newSubscribers.append(item)
                self.subscribers=newSubscribers

        def fade(self, targetColor:"Color", transitionSeconds):
                """fades to the targetColor within transitionSeconds"""

                if transitionSeconds <= 0:
                        return
                
                # kill all running fading threads
                for r in self.runningThreads:
                        r.kill = True

                # Start new thread which controls fade
                t = FadingThread(self,targetColor,int(transitionSeconds))
                self.runningThreads.append(t)
                t.start()

        def fadeHelper(self,r,g,b):
                """do not use this function manually"""
                self._r=r
                self._g=g
                self._b=b
                for callback in self.subscribers:
                        callback(self)
        # Handle Color change events

        @property
        def r(self):
                return self._r

        @property
        def g(self):
                return self._g

        @property
        def b(self):
                return self._b

        @r.setter
        def r(self,value):
                if value>255:
                        self._r = 255
                elif value<0:
                        self._r = 0
                else:
                        self._r = int(value)

                # kill fades when color was set manually
                for t in self.runningThreads:
                        t.kill=True
                
                # Apply change to all subscribers
                for callback in self.subscribers:
                        callback(self)

        @g.setter
        def g(self,value):
                if value>255:
                        self._g = 255
                elif value<0:
                        self._g = 0
                else:
                        self._g = int(value)
                
                # kill fades when color was set manually
                for t in self.runningThreads:
                        t.kill=True

                # Apply change to all subscribers
                for callback in self.subscribers:
                        callback(self)

        @b.setter
        def b(self,value):
                if value>255:
                        self._b = 255
                elif value<0:
                        self._b = 0
                else:
                        self._b = int(value)
                
                # kill fades when color was set manually
                for t in self.runningThreads:
                        t.kill=True

                # Apply change to all subscribers
                for callback in self.subscribers:
                        callback(self)

class FadingThread(Thread):

        def __init__(self, sColor:Color, eColor:Color, seconds:int):
                Thread.__init__(self)
                self.sColor = sColor
                self.eColor = eColor
                self.kill = False
                self.seconds = seconds

        def run(self):
                #do fading...
                i = 0
                r = self.sColor.r
                g = self.sColor.g
                b = self.sColor.b
                dr = self.eColor.r - self.sColor.r
                dg = self.eColor.g - self.sColor.g
                db = self.eColor.b - self.sColor.b

                while i< 10*self.seconds:
                        
                        rNew = r + dr*(i/(self.seconds*10))
                        gNew = g + dg*(i/(self.seconds*10))
                        bNew = b + db*(i/(self.seconds*10))
                        self.sColor.fadeHelper(rNew,gNew,bNew)
                        
                        time.sleep(0.1)
                        if self.kill==True:
                                break
                        i += 1

                #remove thread from running threads
                self.sColor.runningThreads.pop(self.sColor.runningThreads.index(self))

class LedStrip():

        def __init__(self,color:Color,pin_r=16,pin_g=20,pin_b=21) -> None:
                self.pin_r = pin_r
                self.pin_g = pin_g
                self.pin_b = pin_b
                self.pins = pigpio.pi()
                self.color = color
                color.subscribe(self.setPWM)
                self.setPWM(self.color)

        def setPWM(self,color:Color):
                self.pins.set_PWM_dutycycle(self.pin_r,color.r)
                self.pins.set_PWM_dutycycle(self.pin_g,color.g)
                self.pins.set_PWM_dutycycle(self.pin_b,color.b)

        def off(self):
                self.color.unsubscribe(self.setPWM)
                self.pins.set_PWM_dutycycle(self.pin_r,0)
                self.pins.set_PWM_dutycycle(self.pin_g,0)
                self.pins.set_PWM_dutycycle(self.pin_b,0)

        def on(self):
                self.color.subscribe(self.setPWM)
                self.pins.set_PWM_dutycycle(self.pin_r,self.color.r)
                self.pins.set_PWM_dutycycle(self.pin_g,self.color.g)
                self.pins.set_PWM_dutycycle(self.pin_b,self.color.b)
        