from __future__ import print_function, division
from os.path import join, dirname
from sys import argv
from math import sqrt, sin, cos, radians
from collections import deque
import pygame
import WalabotAPI
from random import randint
import time
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    range = xrange
except NameError:
    pass
import config


R_MIN, R_MAX, R_RES = 10, 120, 10  # SetArenaR values
THETA_MIN, THETA_MAX, THETA_RES = -20,20, 10  # SetArenaTheta values
PHI_MIN, PHI_MAX, PHI_RES = -45, 45, 10  # SetArenaPhi values
TSHLD = 1  # SetThreshold value
VELOCITY_THRESHOLD = 3  # captured vel bigger than that counts as key-press

IMG_PATH = join(dirname(argv[0]), 'img')  # path to images
SOUND_PATH = join(dirname(argv[0]), 'sabresounds')  # path to sound files
APP_X, APP_Y = 150, 50  # (x, y) of left corner of the window (in pixels)

def getVelocity(data):
    """ Calculate velocity of a given set of values using linear regression.
        Arguments:
            data            An iterable of numbers.
        Returns:
            velocity        The estimates slope.
    """
    sumY = sumXY = 0
    for x, y in enumerate(data):
        sumY, sumXY = sumY + y, sumXY + x*y
    if sumXY == 0:  # no values / one values only / all values are 0
        return 0
    sumX = x * (x+1) / 2  # Gauss's formula - sum of first x natural numbers
    sumXX = x * (x+1) * (2*x+1) / 6  # sum of sequence of squares
    return abs((sumXY - sumX*sumY/(x+1)) / (sumXX - sumX**2/(x+1)))
    #return (sumXY - sumX*sumY/(x+1)) / (sumXX - sumX**2/(x+1))

class MainGUI(tk.Label):

    def __init__(self, master):
        """ Loads the app assets (images, sound files), init the Walabot,
            sets variables and start the main loop.
        """
        self.img = tk.PhotoImage(file=join(IMG_PATH, 'lightsaber-closed.gif'))
        tk.Label.__init__(self, master, image=self.img)
        self.highlightImage, self.hitImages, self.hbHighlightImage = self.initImages()
        self.wlbt = Walabot()  # init the Walabot SDK
        self.SabreSounds = SabreSounds()  # used to play piano sound
        self.playedLastTime = False
        self.lastTargets = deque([None] * 5)
        self.after(750, self.startWlbt)  # necessary delay to open the window
        self.sabrereset = True
        self.sabretoggle = False
        self.sabreimagetoggle = False
        
    def initImages(self):
        """ Loads the piano images from IMG_PATH and returns them.
            Returns:
                HBhighlightImages     The Sabre Half Bright image when target is not in range
                highlightImages     The Sabre Hightlight image when target is in range
                pressedImages       A list of images of the hit light sabre
        """
        hbHighlightImage = tk.PhotoImage(file=join(IMG_PATH, 'lightsaber-openHB.gif'))        
        highlightImage = tk.PhotoImage(file=join(IMG_PATH, 'lightsaber-open.gif'))
        hitImages = [
            tk.PhotoImage(file=join(IMG_PATH, 'lightsaberhit-'+str(k+1)+'.gif'))
            for k in range(7)]
        return highlightImage, hitImages, hbHighlightImage 

    def startWlbt(self):
        """ Makes sure a Walabot is connected, sets it's parameters and start
            detecting targets and play sounds.
        """
        if self.alertIfWalabotIsNotConnected():
            self.wlbt.setParametersAndStart()
            self.detectTargetAndReply()

    def alertIfWalabotIsNotConnected(self):
        """ Alerts the user to connect a Walabot as long device is not found.
        """
        if not self.wlbt.isConnected():
            self.img = tk.PhotoImage(file=join(IMG_PATH, 'connect-device.gif'))
            self.configure(image=self.img)
            self.after_idle(self.startWlbt)
            return False
        self.img = tk.PhotoImage(file=join(IMG_PATH, 'lightsaber-closed.gif'))
        self.configure(image=self.img)
        return True

    def detectTargetAndReply(self):
        """ 

            will do nothing until the sabre has been opened by Alexa
        """
        if True:
            if config.sabreopen == 1 and not self.sabretoggle:

                if not self.sabreimagetoggle:    
                    self.img = tk.PhotoImage(file=join(IMG_PATH, 'lightsaber-openHB.gif'))
                    self.configure(image=self.img)
                    self.sabreimagetoggle = True
                time.sleep(5)                
                self.SabreSounds.playSabreOpen()
                self.sabretoggle = True
 

            elif config.sabreopen == 0 and self.sabretoggle:
                self.SabreSounds.playSabreClosed()
                self.img = tk.PhotoImage(file=join(IMG_PATH, 'lightsaber-closed.gif'))
                self.configure(image=self.img)
                self.sabretoggle = False
                self.sabreimagetoggle = False                

            self.after_idle(self.detectTargetAndReply)
            target = self.wlbt.getClosestTarget()
            self.lastTargets.popleft()
            self.lastTargets.append(target)
            if not target:
                self.configure(image=self.img)
                self.playedLastTime = False
                return

            vel = getVelocity(t.xPosCm for t in self.lastTargets if t is not None)

                   
            
            if target.zPosCm < R_MAX and config.sabreopen == 1:
                #if target.xPosCm >= 0 and vel > VELOCITY_THRESHOLD:  # 'press' area
                if vel > VELOCITY_THRESHOLD:  # 'press' area            
                    if not self.playedLastTime:  # plays only if in the last
                        hit = randint(0,6)
                        self.configure(image=self.hitImages[hit])
                        print("Sabre Sequence! the key is "+str(hit)) 
                        self.SabreSounds.play(hit)  # iteration no sound was played
                        self.playedLastTime = True
                        config.hit_counter+=1
                        print(str(vel)+'  Its a Hit! '+str(config.hit_counter))
                       
                else:  # hand is at 'highlight' area
                    self.configure(image=self.highlightImage)
                    self.playedLastTime = False
            else:  # hand is too far from the Walabot
                if config.sabreopen == 1:
                    self.configure(image=self.hbHighlightImage)
                    self.playedLastTime = False

class SabreSounds:
    """ This class is designed to play sound files of light sabre FX.
    """

    def __init__(self):
        """ Initialize the PyGame module and loads the sound files according
            to the order of notes.
        """
        self.pygame = pygame
        self.pygame.init()
        self.openFX = pygame.mixer.Sound(join(SOUND_PATH,'fx4.wav'))
        self.closedFX = pygame.mixer.Sound(join(SOUND_PATH,'fx5.wav'))        
        self.hum = pygame.mixer.Sound(join(SOUND_PATH,'hum4.wav'))        
        
        self.notes = {1: '2 Clash', 2: '2clash2', 3: '2clash3', 4: '2clash4', 5: '2clash5', 6: '3 clash 1', 7: '3 Clash Ck' }
        self.sounds = [
            self.pygame.mixer.Sound(
                join(SOUND_PATH,self.notes[key+1]+'.wav')
            )
            for key in range(7)]

    def play(self, key):
        """ Plays a sound of a given key (between 1 and 7).
        """
        self.sounds[key].play()

    def playSabreOpen(self):
        """ play the open sabre sounds and add the hum noise on infinite loop
        """
        self.openFX.play()
        time.sleep(2)
        self.hum.play(loops = -1)

    def playSabreClosed(self):
        """ play the open sabre sounds and add the hum noise on infinite loop
        """
        self.closedFX.play()
        self.hum.stop()       


        

        


class Walabot:
    """ This class is designed to control Walabot device using the Walabot SDK.
    """

    def __init__(self):
        """ Initialize the Walabot SDK, importing the Walabot module,
            set the settings folder path and declare the 'distance' lambda
            function which calculates the distance of a 3D point from the
            origin of axes.
        """
        self.wlbt = WalabotAPI
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()
        self.distance = lambda t: sqrt(t.xPosCm**2 + t.yPosCm**2 + t.zPosCm**2)

    def isConnected(self):
        """ Connect the Walabot, return True/False according to the result.
            Returns:
                isConnected     'True' if connected, 'False' if not
        """
        try:
            self.wlbt.ConnectAny()
        except self.wlbt.WalabotError as err:
            if err.code == 19:  # 'WALABOT_INSTRUMENT_NOT_FOUND'
                return False
        return True

    def setParametersAndStart(self):
        """ Set the Walabot's profile, arena parameters, and filter type. Then
            start the walabot using Start() function.
        """
        self.wlbt.SetProfile(self.wlbt.PROF_TRACKER)
        self.wlbt.SetArenaR(R_MIN, R_MAX, R_RES)
        self.wlbt.SetArenaTheta(THETA_MIN, THETA_MAX, THETA_RES)
        self.wlbt.SetArenaPhi(PHI_MIN, PHI_MAX, PHI_RES)
        self.wlbt.SetThreshold(TSHLD)
        self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_MTI)
        self.wlbt.Start()

    def getClosestTarget(self):
        """ Trigger the Walabot and retrieve the recieved targets using
            GetSensorTargets(). Then calculate the closest target (to the
            walabot) and returns it.
            Returns:
                target      Of SensorTarget type. The closest one. May be
                            'None' if no targets where found.
        """
        self.wlbt.Trigger()
        targets = self.wlbt.GetTrackerTargets()
        try:
            return max(targets, key=self.distance)
        except ValueError:  # 'targets' is empty; no targets were found
            return None


def configureWindow(root):
    """ Set configurations for the GUI window, such as icon, title, etc.
    """
    root.title('Alexa Light Sabre Trainer')
    iconPath = join(IMG_PATH, 'icon.gif')
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=iconPath))
    root.geometry('+{}+{}'.format(APP_X, APP_Y))
    root.resizable(width=False, height=False)


def startApp():
    """ Main function. Create and init the MainGUI class, which runs the app.
    """
    root = tk.Tk()
    configureWindow(root)
    MainGUI(root).pack()
    root.mainloop()

