# Roli Tweet Printer
A Python application for interfacing Twitter (and Reddit) with a cheap POS printer. Get tweets or other information printed in real time. Why? Because I can.

## Images
*Thing in action:*
![Tweet printer in action](https://user-images.githubusercontent.com/2136711/52536917-e7c3f400-2d60-11e9-94f5-8779e0c31cf4.JPG)

*The resulting print:*
![Example of stuff printed](https://user-images.githubusercontent.com/2136711/52536939-235ebe00-2d61-11e9-9d23-8f842d1da57b.JPG)

*Simple configuration web interface:*
![Simple web interface for configuration](https://user-images.githubusercontent.com/2136711/52536712-7125f700-2d5e-11e9-890a-e8620df19104.png)
## Features and stuff:
This was a quick afternoon project that I created just for fun because I had a cheap Chinese POS printer laying around (I bought it just for fun) and I wanted to do something with it. And I actually had a need to follow a specific Twitter account so I wouldn't miss some important events. So this project was born. But as always I over-engineered it a bit, so it has way more features than what I initially planned.

**Features:**
 - Printing Tweets from your favourite accounts (including images and quotes)
 - Printing of messages in your Reddit inbox
 - Print custom text (for notes or similar)
 - Print custom QR codes
 - Easy to use web interface for configuration

## I want to make one
Awesome. You will need two things from the hardware point of view... a POS printer and a computer running linux (something like a Raspberry Pi is probably your best option).

I am using a Chinese ZJ-5890 thermal printer (it's a standard 58mm thermal receipt printer that you can get on Ebay for around 25$). But any thermal printer supported by  **[python-escpos](https://github.com/python-escpos/python-escpos)** should work just fine. Similar ones will of course give you the best results. 
As for a computer running linux... Anything should work really. I recommend Raspberry Pi Zero or similar. But I am running an ACME Systems Arietta G25 because I had one laying around and had no better use for it.

**Software needed:**
This was originally written back in 2017 so don't expect everything to be up to date. Though I did update all of the required libraries in February 2019 and everything still seems to work. Next to the libraries I have written which versions I am currently using to test this. New versions will probably work, but I can't make any promises. Also don't expect the code to be perfect. I am not a professional Python programmer.

This is written in Python, so installing dependencies should be pretty easy. Install python, install pip and then just `pip install` the required libraries. At least that's the theory.

 - Python 3 (3.4)
 - [python-escpos](https://github.com/python-escpos/python-escpos) (2.2.0) [POS printer interface]
 - [Praw](https://github.com/praw-dev/praw) (6.1.1) [Reddit client]
 - [python-twitter](https://github.com/bear/python-twitter) (3.5) [Twitter client]
 - [CherryPy](https://github.com/cherrypy/cherrypy) (17.4.1) [Embedded Web server]
 - [Requests](https://github.com/kennethreitz/requests) (2.16.5) [HTTP Client]

**Setup:**
After you are done installing the libraries, download this project, navigate to the `roliPrinter` directory and run:

    python3 roliPrinter.py

Wait a few seconds then ipen your web browser and navigate to:

    http://[machine-running-roliprinter]:8080

When asked for authentication enter :

    username: printer
    password: printer

After that you should enter your printers PID and VID values into the web interface and configuring your services. How to do this should be explained in the actual web interface itself. This should be it. I may have forgotten something in which case please let me know.

## Troubleshooting, configuring and contributing
If any of this didn't work please look at the errors that are returned and try doing some googling. If that fails please open a new issue here and I will try to help. 

All of the configuration for this project gets stored in the settings.json file. You normally only need to touch it if you need to change the default username and password to something else (that settings is currently not available in the web interface).

If you want to contribute... awesome... I have a lot of ideas for this project, but very little time. So any help will be greately appreciated. Open a pull request, or contact me. My biggest desire is to add integration for Youtube and gmail, but when this will happen is unknown.

The project is currently licensed under the MIT license. 
