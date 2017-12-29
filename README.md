# Alexa-Lightsabre-Trainer


**For the full tutorial look here https://www.hackster.io/daveclarke/alexa-walabot-lightsabre-trainer-c16c17**

## Abstract
Do you want to be able to bring one of your toy lightsabre's to life using nothing but your voice? Then this is the project for you! Using an Echo dot, any computer that can run Python and a Walabot, we're going to add special FX and voice control.

## First Steps
Firstly you will need a Walabot, and Amazon Echo / Dot, a computer capable of running Python and a toy lightsabre. Got that lot? good...

## Initial setup
To run this program properly you will need to make sure you install some frameworks to help us communicate with Alexa
Firstly, from the command line type
pip install flask 
this will install the flask framework modules for Python to use
next
pip intall flask_ask
Flask ask is very nifty and runs a server locally that will interface with the amazon cloud. The only issue is.. how do we get the amazon cloud to see it if it's only available locally? ngrok to the rescue! 
go to ngrok sign up (for free) and download it for your OS. follow the excellent instructions on the website to get it configured and then from the location of the downloaded ngrok exectutable type
ngrok http 5000
This will start a service that will open a tunnel from port 5000 (this is what flask_ask will be using) to the cloud via a randomly assigned url. you will need the https url it gives you, take a note of it. we will need this when setting up the alexa skill.

## Walabot
What is a Walabot?
Want to see through walls? Sense objects in 3D space? Sense if you are breathing from across the room?
Well, you're in luck

The Walabot is whole new way for sensing the space around you using low power radar.
 
Head on over to api.walabot.com and download the latest walabot drivers for your OS. make sure you follow the python installation instructions. you'll need to python walabot wrapper for this to work 
For this project i used the Beta version of the SDK, i was eager to try out the new GetTrackerTargets functionality. This makes target acquisition and tracking way more accurate. you can download the installer for windows and RPi here
https://walabot.com/getting-started-beta 
This installs everything you need to interface with the Walabot. 
 
# The Code
The best thing to do is to either download or fork my github repo for this project
This can be found here
https://github.com/daveyclk/Alexa-Lightsabre-Trainer  
In here you will see a few seperate sheets of code. This keeps things nice and neat. it is very easily stitched together
the sheets are

*main.py - This is the program you will run. This sets up threads for the various servers and programs running.
*config.py - this contains the variables that are shared between the sheets
*lightsabre.py - This controls the UI, walabot tracking ans special FX sounds
*lightsabreAlexa.py - This is the flask ask app that will communitcate with the alexa service
*templates.yaml - This holds all the phrases Alexa will say. These are rendered within lightsabreAlexa.py

looks scary, it isn't! provided you have followed the initial setup steps, all you need to do is type this into your command line (this is a windows machine)
'python main.py'
you will see the startup screen pop up
![Lightsabre closed](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/img/lightsaber-closed.gif)
The startup screen has the lightsabre turned off
you will also see the command prompt showing the flask_ask app server running on 127.0.0.1:5000 this is the reason we needed to point ngrok to port 5000.
Thats it for the app.. but until we add Alexa support, it will do nothing..

# Alexa Skill
Now wait a minute. if you think for a second this is going to be hard.. guess again. Amazon have made skill creation very VERY easy. This is the first skill i have created, and this method made it completely pain free
Firstly you'll need to sign up for an amazon developer account here 
Once you've been fully authorised (this can take a day or so as i found out) you're ready to go.
Next you'll want to begin to create your new skill go here to begin
https://developer.amazon.com/edw/home.html#/skill/create/ 
For this skill we only need to work about the first 5 tabs
This is the Skill information. This is where you fill out the basic details. you need to give it a name and also an invocation name (this is what you shout out to start it up)
In this case the name and invocation name are the same. Light Sabre Trainer
![Skill Information](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/Alexa Skill Screengrabs/Skill Information.JPG)

The next page is the interaction model. This is the part where you tell the Alexa service what is going to be said and what sort of responses she can expect
![Interaction Model](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/Alexa Skill Screengrabs/interaction model.JPG)

for the purposed of this tutorial, just copy and paste the code from my github
/alexa/lightsabre_intent.json shoud be copied into the intent schema
/alexa/sample_utterances.txt should be copied into the sample utterances

The next page is the configuration. This is the part that points the Alexa service to our project. Remember the ngrok url you created? you need that now
select https and in the default field, paste the ngrok url. Copy all the other radio buttons
![Configuration](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/Alexa Skill Screengrabs/configuration.JPG)

Second to last is the SSL certification page. as we're using ngrok, you need to select the second one in the list
![SSL Certificate](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/Alexa Skill Screengrabs/ssl certificate.JPG)

And lastly we're going to look at the test page. This is where you enable you skill for testing on your Dot/echo.. but you can also test it using their beta test service. It's all very handy!
![Test](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/Alexa Skill Screengrabs/test.JPG)

## Testing
Once you have completed all those things, you should be in a position to have a play! 
Set up the Walabot as shown in the video, you'll want to stand about 1.5 metres away to the side. 
To start the app, simply say "Alexa, start Light Sabre Trainer"
She will ask you if you'd like to open your light sabre,  you can say yes at this point.
If you're out of the set arenas range, the light sabre will look Half Bright. like this
![Lightsabre Open Half Bright](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/img/lightsaber-openHB.gif)

When you move closer it will look like this
![Lightsabre Open](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/img/lightsaber-open.gif)

Start working on your best light sabre moves! you will see various lightsabre hit images
![Lightsabre Hit](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/img/lightsaberhit-1.gif)
![Lightsabre Hit](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/img/lightsaberhit-2.gif)
![Lightsabre Hit](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/img/lightsaberhit-3.gif)
![Lightsabre Hit](https://raw.githubusercontent.com/daveyclk/Alexa-Lightsabre-Trainer/img/lightsaberhit-4.gif)

At anypoint you can say "Alexa, start Light Sabre Trainer" 
you have a few options, you can ask Alexa what your score is, or you could say finish or you're tired and alexa will respond with either a current hit score or she will close the light sabre and the FX will stop.

## Caveats
I am still working on refining the Alexa utterances and general feel of her personality,
The arena area of the walabot may need to be tweaked depending on your environment
you can do this my modifying the this code in lightsabre.py
R_MIN, R_MAX, R_RES = 10, 120, 10  # SetArenaR values 
THETA_MIN, THETA_MAX, THETA_RES = -20,20, 10  # SetArenaTheta values 
PHI_MIN, PHI_MAX, PHI_RES = -45, 45, 10  # SetArenaPhi values 
TSHLD = 1  # SetThreshold value  

## Important!
Please enjoy responsibly and let your children have a go 