import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

import config


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    if config.welcome_toggle == 0:
        welcome_msg = render_template('welcome')
        config.welcome_toggle = 1
    else:
        welcome_msg = render_template('welcome2')

    return question(welcome_msg)


@ask.intent("YesIntent")

def open_sabre():
    open_msg = render_template('open')
    config.sabreopen = 1
    return statement(open_msg)

@ask.intent("CloseIntent")

def close_sabre():
    close_msg = render_template('close')
    config.sabreopen = 0
    config.welcome_toggle = 0
    config.hit_counter = 0    
    return statement(close_msg)

@ask.intent("HitIntent")

def hit_count():
    numbers = config.hit_counter
    hit_msg = render_template('hit', numbers=numbers)

    return question(hit_msg)

@ask.intent("YesResetIntent")

def reset_count():
    config.hit_counter = 0
    reset_hit_msg = render_template('resethit')

    return statement(reset_hit_msg)

@ask.intent("NoResetIntent")

def no_reset_count():

    no_reset_hit_msg = render_template('noresethit')

    return statement(no_reset_hit_msg)
