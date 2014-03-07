#   Copyright 2013 Andreas Riegg
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
#
#
#   Changelog
#
#   1.0    2013/02/28    Initial release
#                        

from webiopi.devices.i2c import *
from webiopi.devices.sensor import Luminosity

class SFH7773(I2C, Luminosity):
    def __init__(self, slave=0x38, name="SFH7773"):
        I2C.__init__(self, toint(slave), name)
        self.writeRegister(0x80, 0x03)
            
    def __getLux__(self):
        ambient = self.readRegisters(0x8c, 2)
        return ambient[1]<<8|ambient[0]