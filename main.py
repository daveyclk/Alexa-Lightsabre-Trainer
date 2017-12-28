"""
Runs that functionality of the program, the flask app and the server that communicates with Walabot.
"""

from threading import Thread

from LightSabreAlexa import app

import LightSabre

import time

import config


def main():
    """
   First Job, Get the walabot beer counter working
   Then add the alexa thread
    """
    #config.init() #control the global variables with this
    try:
        LSAlexa_thread = Thread(target=app.run)
        LSAlexa_thread.start()
        

        time.sleep(1)
        lightsabre_thread = Thread(target=LightSabre.startApp())
        lightsabre_thread.start()


       #lightsabre_thread.join()
       # LSAlexa_thread.join()

    except Exception:
        print("Unknown exception occurred!")
        raise

if __name__ == '__main__':
    main()
