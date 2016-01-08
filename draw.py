"""
Script to draw drafting order. 

Each of four players is dealt cards 1 to Q, with each player having exactly
three cards of each suit. The deal is uniform over player, value, and suit. 
"""


import numpy as np


def draw():
	"""
	"""
	cards = np.ones((4, 12))*np.nan  # decks: (player, card)