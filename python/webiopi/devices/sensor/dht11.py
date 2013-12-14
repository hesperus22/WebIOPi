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

from webiopi.devices.sensor import Temperature, Humidity
import dhtreader

class DHT11(Temperature, Humidity):
    def __init__(self, pin=17, type=11):
        self.port = pin
        self.type = type
        dhtreader.init()
        
    def __str__(self):
        return "DHT11(pin=17, type=11)"
        
    def __family__(self):
        return [Temperature.__family__(self), Humidity.__family__(self)]
    
    def __getKelvin__(self):
        return self.Celsius2Kelvin()

    def __getCelsius__(self):
        return self.readDht11()[1]
    
    def __getFahrenheit__(self):
        return self.Celsius2Fahrenheit()

    def __getHumidity__(self):
        return self.readDht11()[0]
        
    def readDht11(self):
        res = None
        
        while res is None:
            res = dhtreader.read(self.type, self.port)
        
        return res
        