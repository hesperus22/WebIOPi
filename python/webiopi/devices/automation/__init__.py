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

class Roller():
	def __init__(self, upPin, downPin, aPin, bPin, upPort=GPIO, downPort=GPIO, aPort=GPIO, bPort=GPIO):
		self.upPort = GPIO
		if upPort!=GPIO :
			self.upPort = deviceInstance(upPort)
		self.upPin = upPin
		self.upPort.setFunction(upPin, GPIO.IN, GPIO.PUD_UP)
			
		self.downPort = GPIO
		if downPort!=GPIO :
			self.downPort = deviceInstance(downPort)
		self.downPin = downPin
		self.downPort.setFunction(downPin, GPIO.IN, GPIO.PUD_UP)
			
		self.aPort = GPIO
		if aPort!=GPIO :
			self.aPort = deviceInstance(aPort)
		self.aPin = aPin
		self.aPort.setFunction(aPin, GPIO.IN, GPIO.PUD_UP)
			
		self.bPort = GPIO
		if bPort!=GPIO :
			self.bPort = deviceInstance(bPort)
		self.bPin = bPin
		self.bPort.setFunction(bPin, GPIO.IN, GPIO.PUD_UP)
		
	@request("POST", "up")
	def up(self):
		if self.isUp():
			return
		
		self.aPort.digitalWrite(self.aPin, GPIO.HIGH)
		self.bPort.digitalWrite(self.bPin, GPIO.LOW)
		
		while not self.isUp():
			pass
		
		self.aPort.digitalWrite(self.aPin, GPIO.LOW)
		
	
	@request("POST", "down")
	def down(self):
		if self.isDown():
			return
		
		self.aPort.digitalWrite(self.aPin, GPIO.LOW)
		self.bPort.digitalWrite(self.bPin, GPIO.HIGH)
		
		while not self.isDown():
			pass
		
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
			
	def isUp(self):
		return self.upPort.digitalRead(self.upPin) == GPIO.LOW
		
	def isDown(self):
		return self.downPort.digitalRead(self.downPin) == GPIO.LOW