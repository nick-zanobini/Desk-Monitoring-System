#Creating a Desk Monitoring System.

Components:
  * Raspberry Pi 3
  * 8GB MicroSD Card
  * 5V 2.1A Switching Power Supply
  * Raspberry Pi Camera
  * QLight ST-USB Series Signal Tower
  * Raspberry Pi and PiCamera Case

- Flash latest version of Raspian Jesse on to SD Card
- Connect PiCamera to Raspberry Pi (Silver connectors facing the HDMI port)
- Install your case on both your Raspberry Pi and PiCamera
- Plug both USB ports from the QLight into the Raspberry Pi
- Plug in your Raspberry Pi and connect it to the internet

You can work on your Raspberry Pi as a computer (with a mouse, keyboard and monitor connected) or as I prefer SSH into your RPi from your computer. I use X11 forwarding so I can see the video stream of the PiCamera. To SSH with X11 forwarding the following and replace 192.168.0.XX with the IP address of your Raspberry Pi.:
  * `ssh -X pi@192.168.0.XX`

Once connected to your Raspberry Pi you need to start installing the necessary libraries.


