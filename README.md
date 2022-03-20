# mrdflib
mRDFLib is a fork and port of [RDFLib](https://github.com/RDFLib/rdflib) for micropython. It is a library for working with RDF. 
It is a work in progress and the goal is to make the code and memory footprint as small as possible. 
Currently several functionalities like XML, isodate, Decimal (and thus _XSD_DECIMAL, _XSD_DATETIME, _XSD_DATE, etc.) are not working. Notation3 parser needs some more debugging.

mRDFLib has been tested by compiling [micropython](https://github.com/micropython/micropython) on Linux and ESP32 (with 4MB PSRAM for example esp32-one, ESP32 cam, ESP32-S3 with PSRAM etc. Note that ESP32-S3 is new and needs a separate firmware compilation.).

## Prerequisites
To test it quickly, one either needs linux with python3 or ESP32 with 4MB of SPIRAM. 
For testing over ESP32, one needs to install [IDF (tested with v4.0.2)](https://github.com/espressif/esp-idf) as well as tools like adafruit-ampy, picocom The last two can be installed using `sudo apt-get install adapfruit-ampy picocom`. For installing IDF one has to follow instructions provided in the README.md file in micropython/ports/esp32/ folder of micropython.

## Linux 
To test it on Linux, please compile the [micropython](https://github.com/micropython/micropython) with all REGEX options supported by micropython. This can be done by modifying the file micropython/ports/unix/mpconfigport.h

and adding the following (after `#ifndef MICROPY_UNIX_MINIMAL` for example)

```
#define MICROPY_PY_URE_SUB 40
#define MICROPY_PY_URE_MATCH_GROUPS         (1)
#define MICROPY_PY_URE_MATCH_SPAN_START_END (1)
```
Then compile micropython following the README.md instructions in the folder micropython/ports/unix.

## ESP32
For quick test, you may flash ESP32 with the firmware that was already compiled and is [available here](https://github.com/ksingh25/Files). Mostly firmware.bin is needed. One needs to flash ESP32 with this firmware. In this case one may skip the instructions 
for compilation provided in this section.

To compile micropython and test it on ESP32, please first install [IDF (tested with v4.0.2)](https://github.com/espressif/esp-idf).

After that please download [micropython code](https://github.com/micropython/micropython) 
cd to `micropython/ports/esp32` directory and then compile and flash the firware
check some intial steps [here](https://github.com/micropython/micropython/tree/master/ports/esp32/README.md)

Some steps are given here :
```
$ cd micropython
$ make -C mpy-cross
```

Then to build MicroPython for the ESP32 run (assuming IDF is already installed):

```
$ cd ports/esp32
```
modify mpconfigport.h and add the following (after `#ifndef MICROPY_UNIX_MINIMAL` for example)

```
#define MICROPY_PY_URE_SUB 40
#define MICROPY_PY_URE_MATCH_GROUPS         (1)
#define MICROPY_PY_URE_MATCH_SPAN_START_END (1)
```

Then compile micropython firmware and flash the ESP32.

```
$ make submodules
$ make BOARD=GENERIC_SPIRAM
$ idf.py -D MICROPY_BOARD=GENERIC_SPIRAM -B build-GENERIC_SPIRAM  -p /dev/ttyUSB0 -b 460800 erase_flash
$ idf.py -D MICROPY_BOARD=GENERIC_SPIRAM -B build-GENERIC_SPIRAM  -p /dev/ttyUSB0 -b 460800 flash
```

## Upload mRDFLib files on ESP32
You may skip this step if you just need to test it on Linux with micropython.
The step is to upload the files on ESP32. 
```
$ git clone https://github.com/ksingh25/mrdflib.git
$ cd mRDFLib
```
Upload all the files manually or use the copy.py script or WebREPL over WiFi. 
**Uploading files over UART takes around 7 to 10 minutes.** In future, baudrate may be increased.  
mRDFLib is around 800KB and thus we will also reduce its size.

Assuming that the port is /dev/ttyUSB0:

`$ python3 copy.py /dev/ttyUSB0`

or copy them one by one using ampy:
```
$ ampy --port /dev/ttyUSB0 --baud 115200 put wlan.py
...
```


## Test some examples
You may enter the terminal using picocom.
**Note that first import and first script takes several seconds to run.**
After that it is much faster.
One may try directly uploading the compiled .pyc files for better execution speed.

`$ picocom -b 115200 /dev/ttyUSB0`

1. Add some facts to the graph and serialize them in different formats.
```
>>> execfile('example_serialize.py')
--- printing raw triples ---
N2cd597acdbf84ff7bc6c6df8380d3888 http://xmlns.com/foaf/0.1/name Jack Jack
N636a33fe2c9946e7a53228e5a3ae15e4 http://xmlns.com/foaf/0.1/nick donna
N636a33fe2c9946e7a53228e5a3ae15e4 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://xmlns.com/foaf/0.1/Person
N2cd597acdbf84ff7bc6c6df8380d3888 http://xmlns.com/foaf/0.1/nick jack
N636a33fe2c9946e7a53228e5a3ae15e4 http://xmlns.com/foaf/0.1/name Donna Fales
N2cd597acdbf84ff7bc6c6df8380d3888 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://xmlns.com/foaf/0.1/Person

--- printing mboxes ---

RDF Serializations:
--- start: turtle ---
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

[] a foaf:Person ;
    foaf:name "Jack Jack" ;
    foaf:nick "jack"@en .

[] a foaf:Person ;
    foaf:name "Donna Fales" ;
    foaf:nick "donna"@foo .


--- end: turtle ---
...
```

2. Input a string containing RDF triples, add triples to the RDF store, serialize the graph to JSON-LD format 

```
>>> execfile('example_sosa.py')
Warning: parser.py BytesIOWrapper not supported
absolutize namespacemanager <NamespaceManager object at 3f8f5ab0>
Warning namespace.py absolutize: getcwd is different on linux vs other platforms
Graph length 12
--- start: JSON-LD ---
[{"@id": "file:///.%2f/sensor/philips/HJC42XB/bulb","@type": ["http://www.w3.org/ns/sosa#Sensor"],"http://www.w3.org/ns/sosa#observes": [{"@id": "file:///.%2f/philips/46N7743619/light"}],"http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "Philips E27 Bulb - HJC42XB - Read Lumen","@language": "en"}]},{"@id": "file:///.%2f/actuator/philips/HJC42XB/bulb","http://www.w3.org/ns/sosa#actsOnProperty": [{"@id": "file:///.%2f/philips/46N7743619/light"}],"http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "Philips E27 Bulb - HJC42XB - Turn On/Off","@language": "en"}],"@type": ["http://www.w3.org/ns/sosa#Actuator"],"http://www.w3.org/ns/sosa#usedProcedure": [{"@id": "file:///.%2f/philips/46N7743619/switchAPI"}]},{"@id": "file:///.%2f/philips/46N7743619","http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "Philips Hue Bridge 46N7743619","@language": "en"}],"http://www.w3.org/ns/sosa#hosts": [{"@id": "file:///.%2f/actuator/philips/HJC42XB/bulb"},{"@id": "file:///.%2f/sensor/philips/HJC42XB/bulb"}],"@type": ["http://www.w3.org/ns/sosa#Platform"],"http://www.w3.org/2000/01/rdf-schema#comment": [{"@value": "Philips Hue Bridge - installed in living room","@language": "en"}]}]
--- end: JSON-LD ---
```


3. Download a file over http (**currently https is not working and needs debugging**), parse and serialize it.

Download and put the modified [foaf.n3](https://raw.githubusercontent.com/ksingh25/Files/main/foaf.n3) file in some folder on your PC. Then run a simple HTTP Server to make it accessible on web. Original foaf file has some special characters which are causing problems for parsing.

On your PC `cd` to the folder containing foaf.n3 file and start the server:

`sudo python -m SimpleHTTPServer 80`

Now to the ESP32 (using picocom)

Please put the ip address of the local pc (hosting modified foaf.n3) in the file example_parse_foaf.py and upload it to ESP32.

`ampy --port /dev/ttyUSB0 --baud 115200 put example_parse_foaf.py`

Then please add WiFi SSID and password to wlan.py and upload it to ESP32.

`ampy --port /dev/ttyUSB0 --baud 115200 put wlan.py`

Connect to ESP32 terminal:

`picocom -b 115200 /dev/ttyUSB0`

Connect ESP32 to WiFi and launch example_parse_foaf.py
```
>>> execfile('wlan.py')
network config: ('192.168.0.20', '255.255.255.0', '192.168.0.254', '8.8.8.8')
>>> execfile('example_parse_foaf.py')
...
```
This downloads the whole foaf.n3, parses it and prints the triples on the terminal.

