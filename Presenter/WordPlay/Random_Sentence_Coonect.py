#
#   Exercise 2.1
#   A simple sentence generator
#
#   One possible solution
#
##


import random

def noun():
    """Return a random noun"""
    n = ['dog', 'cat', 'poodle', 'manx']
    return random.choice(n)

def det():
    """Return a random determiner"""
    return random.choice(['a', 'the'])

def adj():
    """Return a random adjective"""
    return random.choice(['sad', 'happy', 'silly'])

def verb():
    """Return a transitive verb"""
    return random.choice(['likes', 'saw'])

def np():
    """Returns a random noun phrase"""
    return det() + ' ' + adj() + ' ' + noun()

def vp():
    """Returns a random verb phrase"""
    return verb() +  ' ' + np()

def s():
    """Return a simple sentence"""
    return np().capitalize() + ' ' + vp() + '.'

