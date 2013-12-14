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

class RollerThread(Thread):
	def __init__(self, roller, up):
		self.canceled = false
		self.up = up
		
	def run(self):
		
		
class Roller():
    def __init__(self, upPin, downPin, aPin, bPin, upPort=GPIO, downPort=GPIO, aPort=GPIO, bPort=GPIO):
        self.upPort = GPIO
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
		return "Roller (upPort: %s, upPin: %d, downPort: %s, downPin: %d, aPort: %s, aPin: %d, bPort: %s, bPin: %d)" \
			%(self.upPort, self.upPin, self.downPort, self.downPin, self.aPort, self.aPin, self.bPort, self.bPin)
    
    def __family__(self):
        return "Roller"
        
    @request("POST", "up")
    def up(self):
		def __up__():
			if self.isUp():
				return
			
			self.aPort.digitalWrite(self.aPin, GPIO.HIGH)
			self.bPort.digitalWrite(self.bPin, GPIO.LOW)
			
			while not self.isUp():
				pass
			
			self.aPort.digitalWrite(self.aPin, GPIO.LOW)
        
		Thread(__up__).start()
    
    @request("POST", "down")
    def down(self):
		def __down__():
			if self.isDown():
				return
        
			self.aPort.digitalWrite(self.aPin, GPIO.LOW)
			self.bPort.digitalWrite(self.bPin, GPIO.HIGH)
        
			while not self.isDown():
				pass
        
			self.bPort.digitalWrite(self.bPin, GPIO.LOW)
		
		Thread(__down__).start()
    
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