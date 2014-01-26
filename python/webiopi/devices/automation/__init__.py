#   Copyright 2012-2013 Eric Ptak - trouch.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from webiopi import GPIO, deviceInstance
from webiopi.protocols.rest import *
from webiopi.utils import toint
from threading import Thread
import time

class RollerThread(Thread):
    def __init__(self, roller, up):
        Thread.__init__(self)
        self.canceled = False
        self.direction = up
        self.roller = roller
        
    def cancel(self):
        self.canceled = True
        
    def up(self):
        if self.roller.isUp():
            return
        
        self.roller.startUp()
        
        while not (self.roller.isUp() or self.canceled):
            pass
        
        self.roller.stop();
        
    def down(self):
        if self.roller.isDown():
            return
        
        self.roller.startDown()
        
        while not (self.roller.isDown() or self.canceled):
            pass
        
        self.roller.stop()
    
    def run(self):
        if self.direction:
            self.up()
        else:
            self.down()
                
class Roller():
    def __init__(self, upPin, downPin, aPin, bPin, upPort=GPIO, downPort=GPIO, aPort=GPIO, bPort=GPIO):
        self.upPort = GPIO
        self.rollerThread = None
        if upPort!=GPIO :
            self.upPort = deviceInstance(upPort)
        self.upPin = toint(upPin)
        self.upPort.setFunction(self.upPin, GPIO.IN, GPIO.PUD_UP)
            
        self.downPort = GPIO
        if downPort!=GPIO :
            self.downPort = deviceInstance(downPort)
        self.downPin = toint(downPin)
        self.downPort.setFunction(self.downPin, GPIO.IN, GPIO.PUD_UP)
            
        self.aPort = GPIO
        if aPort!=GPIO :
            self.aPort = deviceInstance(aPort)
        self.aPin = toint(aPin)
        self.aPort.setFunction(self.aPin, GPIO.OUT)
            
        self.bPort = GPIO
        if bPort!=GPIO :
            self.bPort = deviceInstance(bPort)
        self.bPin = toint(bPin)
        self.bPort.setFunction(self.bPin, GPIO.OUT)
    
    def __str__(self):
        def port(port):
            if port == GPIO:
                return "GPIO"
            else:
                return port
                
        return "Roller (upPort: %s, upPin: %d, downPort: %s, downPin: %d, aPort: %s, aPin: %d, bPort: %s, bPin: %d)" \
            %(port(self.upPort), self.upPin, port(self.downPort), self.downPin, port(self.aPort), self.aPin, port(self.bPort), self.bPin)
    
    def __family__(self):
        return "Roller"
        
    @request("POST", "up")
    def up(self):
        if self.rollerThread is not None:
            self.rollerThread.cancel()
        self.rollerThread = RollerThread(self, True)
        self.rollerThread.start()
    
    @request("POST", "down")
    def down(self):
        if self.rollerThread is not None:
            self.rollerThread.cancel()
        self.rollerThread = RollerThread(self, False)
        self.rollerThread.start()
        
    def startDown(self):
        self.aPort.digitalWrite(self.aPin, GPIO.LOW)
        self.bPort.digitalWrite(self.bPin, GPIO.HIGH)
        
    def startUp(self):
        self.aPort.digitalWrite(self.aPin, GPIO.HIGH)
        self.bPort.digitalWrite(self.bPin, GPIO.LOW)
        
    def stop(self):
        self.aPort.digitalWrite(self.aPin, GPIO.LOW)
        self.bPort.digitalWrite(self.bPin, GPIO.LOW)
    
    @request("GET", "state")
    @response("%s")
    def state(self):
        if self.isUp():
            return "Up"
        
        if self.isDown():
            return "Down"
            
        if self.aPort.digitalRead(self.aPin) == GPIO.HIGH:
            return "Going up"
        
        if self.bPort.digitalRead(self.bPin) == GPIO.HIGH:
            return "Going down"
            
        return "Unknown"
            
    def isUp(self):
        return self.upPort.digitalRead(self.upPin) == GPIO.LOW
        
    def isDown(self):
        return self.downPort.digitalRead(self.downPin) == GPIO.LOW
        
 class AlarmThread(Thread):
    def __init__(self, alarm):
        Thread.__init__(self)
        self.canceled = False
        self.alarm = alarm
    
    def run(self):
        while not self.canceled:
            if self.alarm.pirState() == GPIO.HIGH
                self.alarm.startAlarm()
            time.sleep(1)
                
    def cancel(self):
        self.canceled = True
    
        
 class Alarm():
    def __init__(self, alarmPin, pirPin, alarmPort=GPIO, pirPort=GPIO):
        self.alarmPin = alarmPin
        self.alarmPort = alarmPort
        self.pirPin = pirPin
        self.pirPort = pirPort
        
    @request("POST", "startAlarm")
    def startAlarm(self):
        self.alarmPort.digitalWrite(alarmPin, GPIO.HIGH)
        
    @request("POST", "stopAlarm")    
    def stopAlarm(self):
        self.alarmPort.digitalWrite(alarmPin, GPIO.LOW)
        
    @request("GET", "pir")
    def pirState(self):
        return self.pirPort.digitalRead(pirPin)
    
    @request("POST", "lock")
    def lock(self):
        if self.locked:
            return
        self.locked = True
        self.worker = AlarmThread(self)
    
    @request("POST", "unlock")
    def unlock(self):
        if self.worker is not None:
            self.worker.cancel()
        self.stopAlarm()
        self.locked = False
        
    @request("GET", "state")
    @response("%s")    
    def state(self):
        if self.locked:
            return "Locked"
        else:
            return "Unlocked"
        
        
    