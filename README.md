# RobbieAssistant
Desktop Phone Notification Assistant Featuring (R.O.B.) Robotic Operating Buddy

![Final Construction](https://raw.githubusercontent.com/khinds10/XXX.jpg "Final Construction")

#### Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
> 
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
> 
> $ `umount /dev/sdb1`
> 
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
> 
> *if=location of RASPBIAN JESSIE LITE image file*
> *of=location of your microSD card*
> 
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
> pass: **raspberry**

Change your account password for security
>`sudo passwd pi`

Enable RaspberriPi Advanced Options
>`sudo raspi-config`

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "RobbieAssistant"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Reboot PI for Keyboard layout changes / file system resizing to take effect**
>$ `sudo shutdown -r now`

**Auto-Connect to your WiFi**

>`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines to have your raspberrypi automatically connect to your home WiFi
*(if your wireless network is named "linksys" for example, in the following example)*

	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}

**Reboot PI to connect to WiFi network**

>$ `sudo shutdown -r now`
>
>Now that your PI is finally on the local network, you can login remotely to it via SSH.
>But first you need to get the IP address it currently has.
>
>$ `ifconfig`
>*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

**Go to another machine and login to your raspberrypi via ssh**

> $ `ssh pi@192.168.XXX.XXX`

**Start Installing required packages**

>$ `sudo apt-get update`
>
>$ `sudo apt-get upgrade`
>
>$ `sudo apt-get install build-essential tk-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libncurses5-dev libncursesw5-dev libreadline6-dev python3-pip python3-requests python3-setuptools python3-urllib python3-urllib3 python3-requests vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip libi2c-dev vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip python-gpiozero python-psutil xz-utils`
>
>$ `sudo pip install requests`

**Update local timezone settings

>$ `sudo dpkg-reconfigure tzdata`

`select your timezone using the interface`

**Setup the simple directory `l` command [optional]**

>`vi ~/.bashrc`
>
>*add the following line:*
>
>`alias l='ls -lh'`
>
>`source ~/.bashrc`

**Fix VIM default syntax highlighting [optional]**

>`sudo vi  /etc/vim/vimrc`
>
>uncomment the following line:
>
>_syntax on_

# make the logs folder for the application to run

`mkdir /home/pi/RobbieAssistant/logs`
`chmod 777 /home/pi/RobbieAssistant/logs`

## Configure Application to run correctly in settings.py config file

Find the file `settings-shadow.py` in the `/includes/` folder of the project and copy it to `settings.py` and adjust to your current settings

> \# forecast.io API key for local weather information
>
> weatherAPIURL = 'https://api.forecast.io/forecast/'
>
> weatherAPIKey = 'YOUR API KEY FOR FORECAST.IO'
> 
> \# optional for running the remote temp/humidity logger
>
> dashboardServer = 'mydevicelogger.com'
>
> \# search google to get the Latitude/Longitude for your home location
>
> latitude = 41.4552578
>
> longitude = -72.1665444
>

# Supplies Needed

**RaspberriPi Zero**

![Pi Zero](https://github.com/khinds10/RobbieAssistant/master/images/pizero.jpg "Pi Zero")

**DHT11 Humidistat**

![DHT11 Humidistat](https://github.com/khinds10/RobbieAssistant/master/images/dht11.jpg "DHT11 Humidistat")

LED Lights (x4) Green / Yellow / Blue / Red

![LED Lights](https://github.com/khinds10/RobbieAssistant/master/images/led.jpg "LED Lights")

**2.6" Digole Display**

![Digole Display](https://github.com/khinds10/RobbieAssistant/master/images/display.png "Digole Display")

## Build and wire the device

**1) Prepare the Digole Display for i2C**

On the back of the Digole Display, solder the jumper to assign the display to use the i2c protocol
![i2c Jumper Digole](https://github.com/khinds10/RobbieAssistant/master/images/display-back.png "i2c Jumper Digole")

## Using a 3d printer, print the cover, box and back panels

Using the following X STL files in the `3DPrint` folder, R.O.B. Robot, LED Harness and Display Mount
>
> buttonContainer-base.stl
>
> buttonContainer-lid.stl
>
> displaymount-final.stl
>
> led-harness-final.stl
>
> MiniNintendoROB.zip

Robot Print by: Mini Nintendo R.O.B. - by RabbitEngineering

https://www.thingiverse.com/thing:1494964

![Wiring Diagram](https://github.com/khinds10/RobbieAssistant/master/images/wiringdiagram.png "Wiring Diagram")

**Digole Display**
>
> GND -> GND
>
> DATA -> SDA
>
> CLK -> SCL
>
> VCC -> 3V
    
**DHT11 Humidistat**
>
> VCC -> 5V
>
> GND -> GND
>
> DATA -> GPIO 25
>

**BLUE Resistor**
>
> VCC -> GPIO 17 (with 270ohm resistor)
>
> GND -> GND
>

**YELLOW Resistor**
>
> VCC -> GPIO 13 (with 270ohm resistor)
>
> GND -> GND
>

**GREEN Resistor**
>
> VCC -> GPIO 6 (with 270ohm resistor)
>
> GND -> GND
>

**RED Resistor**
>
> VCC -> GPIO 12 (with 270ohm resistor)
>
> GND -> GND
>

**RED Momentary Pushbutton**
>
> VCC -> GPIO 16 (with 270ohm resistor)
>
> GND -> GND
>

**BLUE Momentary Pushbutton**
>
> VCC -> GPIO 26 (with 270ohm resistor)
>
> GND -> GND
>

## Check I2C Configuration

Start up your RaspberryPi and make sure the I2C bus recognizes all your connected 7/14 segment displays. 
*[each display is given a unique address described above by how you solder each display's jumpers in different combinations]*

If you have the display with jumper soldered correctly, you should have the following output for the `i2cdetect` command:

`sudo i2cdetect -y 1`
     
>     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
>
>00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
>
>10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
>
>20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- -- 
>
>30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
>
>40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
>
>50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
>
>60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
>
>70: -- -- -- -- -- -- -- --
>

**DHT11 Install**

>$ `cd ~`
>
>$ `git clone https://github.com/adafruit/Adafruit_Python_DHT.git`
>
>$ `cd Adafruit_Python_DHT/`
>
>$ `sudo python setup.py install`
>
>$ `sudo python ez_setup.py`
>
>$ `cd examples/`
>
>$ `vi simpletest.py`
>

Change the following line:
> sensor = Adafruit_DHT.DHT11

Comment the line out
> pin = 'P8_11'

Uncomment the line and change the pin number to 16
> pin = 25

Run the test

`python simpletest.py`

> You should see a metric reading of Temp and Humidity displayed on the command line.

**Clone RobbieAssistant repository**

>$ `cd ~`
>
>$ `git clone https://github.com/khinds10/RobbieAssistant.git`

**PushBullet/**

*Using the pushbullet app for your phone, signup to recieve an API key to have a simple python script be able to capture and push data hub notifications and indicator flags*

Install Python 3.5 for asyncio functionality

	sudo apt-get update
	sudo apt-get install build-essential tk-dev
	sudo apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev
	sudo apt-get install libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
	sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

If one of the packages cannot be found, try a newer version number (e.g. libdb5.4-dev instead of libdb5.3-dev).

	wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
	tar zxvf Python-3.5.2.tgz
	cd Python-3.5.2
	./configure --prefix=/usr/local/opt/python-3.5.2
	make
	sudo make install
	sudo ln -s /usr/local/opt/python-3.5.2/bin/pydoc3.5 /usr/bin/pydoc3.5
	sudo ln -s /usr/local/opt/python-3.5.2/bin/python3.5 /usr/bin/python3.5
	sudo ln -s /usr/local/opt/python-3.5.2/bin/python3.5m /usr/bin/python3.5m
	sudo ln -s /usr/local/opt/python-3.5.2/bin/pyvenv-3.5 /usr/bin/pyvenv-3.5
	sudo ln -s /usr/local/opt/python-3.5.2/bin/pip3.5 /usr/bin/pip3.5
	cd ~
	echo 'alias python35="/usr/local/opt/python-3.5.2/bin/python3.5"' >> .bashrc
	echo 'alias idle35="/usr/local/opt/python-3.5.2/bin/python3.5"' >> .bashrc

Install the python3 dependancies

	sudo apt-get install python3-setuptools
	sudo apt-get install python3-pip
	sudo pip3 install asyncpushbullet
    sudo pip3 install requests
    
*Optional way* Download the python repository directly to obtain the python dependancies without the use of pip installing it

    git clone https://github.com/rharder/asyncpushbullet
    cd asyncpushbullet && sudo /usr/local/opt/python-3.5.2/bin/python3.5 setup.py install

Visit the pushbullet settings page in your account to generate an API key to use
https://www.pushbullet.com/#settings

Configure your `pushbullet-listener.py` script to have the correct API and dashboard central host

	# your API Key from PushBullet.com
	API_KEY = "o.XXXYYYZZZ111222333444555666"

	# dashboard central server host
	dashboardServer = 'MY-SERVER-HERE.com'

Add the script to start at dashboard boot and restart your dashboard pi

$ `crontab -e`

`@reboot nohup /usr/local/opt/python-3.5.2/bin/python3.5 /home/pi/PushBullet/pushbullet-listener.py >/dev/null 2>&1`
`@reboot nohup /usr/local/opt/python-3.5.3/bin/python3.5 /home/pi/RobbieAssistant/PushBullet/pushbullet-listener.py > /dev/null 2>&1`
`@reboot nohup python /home/pi/RobbieAssistant/Robbie.py > /dev/null 2>&1`
`@reboot nohup python /home/pi/RobbieAssistant/Temp.py > /dev/null 2>&1`
`@reboot nohup python /home/pi/RobbieAssistant/Weather.py > /dev/null 2>&1`

## OPTIONAL: Creating your own Nintendo images to render on the display

Upload your own 128x128 file to the following URL:

http://www.digole.com/tools/PicturetoC_Hex_converter.php 

Choose your image file to upload, add what size you want it to be on the screen (Width/Height)

Select "256 Color for Color OLED/LCD(1 byte/pixel)" in the "Used for" dropdown

Obtain the hex output.

Add the hex output to a display/build/ header (.h) file, use the other ones as guides for syntax.

Include the new file in the digole.c file 
`#include "myimage.h`

Include a new command line hook to your image file in the.
_Note: the command below is saying draw your image at position 10 pixels over 10  pixels down. You can change it to different X,Y coordinates, you can also change the values 128,128 to whatever size your new image actually is._

`} else if (strcmp(digoleCommand, "myimage") == 0) {`
    `drawBitmap256(10, 10, 128, 128, &myimageVariableHere,0);  // myimageVariableHere is defined in your (.h) file`
`}`

Now rebuild (ignore the errors) below to have your new image render with the following command.
>$ `./digole myimage`

**Re-Building [Included] Digole Display Driver for your optional changes**

>$ `cd display/build`

>$ `gcc digole.c`

>$ `mv a.out ../../digole`

>$ `chmod +x ../../digole`
