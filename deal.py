"""
Script to deal cards for drafting order. 

Each of four players is dealt cards 1 to Q, with each player having exactly
three cards of each suit. The deal is uniform over player, value, and suit. 
"""


import numpy as np


def deal():
	"""
	"""
	cards = np.empty((4, 12), dtype=str) # decks: (player, card)
	cards[:, :] = 'X' # X indicates card not yet drawn
	suits = ['H', 'S', 'D', 'C'] 
	num_players = 4
	num_to_deal = 3 # number of cards of each suit given to each player
	num_suits = 4
	num_in_deck = num_to_deal*num_suits # number of cards in each player's deck
	players = np.arange(num_players)
	suits = ['H', 'S', 'D', 'C'] 
	cards = np.empty((num_players, num_in_deck), dtype=str) # (player, card)
	cards[:, :] = 'X' # X indicates card not yet drawn
	for suit in suits[:2]:
		for player in players:
			own_filled = cards[player] != 'X'
				# slots in current player's deck already filled by any suit 
			other_filled = np.any(cards[:player, :] == suit, axis=0)	
				# slots in other players' decks filled by only current suit
			available = np.arange(num_in_deck)[~own_filled & ~other_filled]
			print suit
			print cards
			print available, available.size
			print
			to_fill = np.random.choice(available, num_to_deal, replace=False)
			cards[player, to_fill] = suit
	return cards


