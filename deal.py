"""
Script to deal cards for drafting order. 

Each of four players is dealt cards 1 to Q, with each player having exactly
three cards of each suit. The deal is uniform over player, value, and suit. 
"""


import numpy as np


class PlayoffDeck(object):
	"""
	This object represents the 4 decks of cards dealt, one to each player.
	"""
	def __init__(self):
		"""
		Initialize set of four empty decks.
		"""
		self.num_players = 4
		self.num_each_suit = 3 # cards of each suit given to each player
		self.num_suits = 4
		self.num_in_deck = num_each_suit*num_suits # cards in each player deck
		self.players = np.arange(num_players)
		self.suits = ['H', 'S', 'D', 'C'] 
		self.cards = np.empty((num_players, num_in_deck), dtype=str)
		self.cards[:, :] = 'X' # X indicates card not yet drawn
		self.nominal = [[s for s in suits] for player in players]
			# see update_nomial

	def update_nominal(self):
		"""
		Determine the nominally available suits for each slot of each deck.

		The result is 'nominal' as it will check only the suits in the
		corresponding slots in other players' decks, not considering the 
		constraints imposed by the suits in the current player's other slots.
		"""



