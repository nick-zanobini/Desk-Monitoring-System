#Creating a Desk Monitoring System.

Components:
  * Raspberry Pi 3
  * 8GB MicroSD Card
  * 5V 2.1A Switching Power Supply
  * Raspberry Pi Camera
  * QLight ST-USB Series Signal Tower
  * Raspberry Pi and PiCamera Case

Here's what you need to do to get started:
- Flash latest version of Raspian Jesse on to SD Card
- Connect PiCamera to Raspberry Pi (Silver connectors facing the HDMI port)
- Install your case on both your Raspberry Pi and PiCamera
- Plug both USB ports from the QLight into the Raspberry Pi
- Plug in your Raspberry Pi and connect it to the internet

You can work on your Raspberry Pi as a computer (with a mouse, keyboard and monitor connected) or as I prefer SSH into your RPi from your computer. I use X11 forwarding so I can see the video stream of the PiCamera. To SSH with X11 forwarding the following and replace 192.168.0.XX with the IP address of your Raspberry Pi.:
  * `ssh -X pi@192.168.0.XX`

Once connected to your Raspberry Pi you need to start installing the necessary libraries.

0. Always good practice to update everything before you install stuff:
  * `sudo apt-get update`
  * `sudo apt-get upgrade`
  * `sudo rpi-update`

1. Install libusb
  * `sudo apt-get install libusb-1.0-0-dev`

2. Install the QLight interface.
  * `git clone https://github.com/KennethWilke/qlight_userspace`
  * `cd qlight_userspace`
  * `make`

3. Test that the QLight works
  * Plug in both USB ports to the Raspberry Pi. Navigate to the QLight folder
    * `cd qlight_userspace`
  * Turn on and off the Red Light on the Q light
    * `sudo ./qlight -r on`
      * You should get the following output.
          ```
          Q-light detected
          Claimed interface
          Released interface
          ```
    * `sudo ./qlight -r off`
      * You should get the following output.
          ```
          Q-light detected
          Claimed interface
          Released interface
          ```

4. Install OpenCV 3
  a. We need to install some packages that allow OpenCV to process images:
    * `sudo apt-get install libtiff5-dev libjasper-dev libpng12-dev`
  If you get an error about libjpeg-dev try installing this first:
    * `sudo apt-get install libjpeg-dev`
  b. We need to install some packages that allow OpenCV to process videos:
    * `sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev`
  c. We need to install the GTK library for some GUI stuff like viewing images.
    * `sudo apt-get install libgtk2.0-dev`
  d. We need to install some other packages for various operations in OpenCV:
    * `sudo apt-get install libatlas-base-dev gfortran`
  e. We need to install pip if you haven't done so in the past:
    * `wget https://bootstrap.pypa.io/get-pip.py`
    * `sudo python get-pip.py`
  f. Now we can install NumPy - a python library for maths stuff - needed for maths stuff.
    * `sudo pip install numpy`
  g. Download and install the file from this repo called "latest-OpenCV.deb".
    * `wget "https://github.com/jabelone/OpenCV-for-Pi/raw/master/latest-OpenCV.deb"`
    * `sudo dpkg -i latest-OpenCV.deb`
  h. Test it installed correctly by doing the following: Open a python shell
    * `python`
    * Run the following commands, it should return the same version you installed.
      ```
      import cv2
      cv2.__version__
      ```
