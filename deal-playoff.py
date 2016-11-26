#!/usr/bin/env python
"""
Script to randomly determine drafting order for fantasy playoff.
"""


import datetime as dt 
import random 

import numpy as np
import click


def get_available(cards, suits, player, rank):
    """
    Determine the available suits for the passed rank for the passed player
    """
    num_players, num_in_deck = cards.shape
    num_each_suit = num_in_deck/num_players  # must have no remainder
    current = cards[player, rank]
    if current == 'X':  # slot empty - find available suits
        available = []
        nominal = [s for s in suits if s not in cards[:, rank]]
            # all suits not yet given to another player at this rank
        for nom in nominal:
            already = np.sum(cards[player, :] == nom)
            if already < num_each_suit:
                available.append(nom)
        return available
    else:  # slot full - no suits available
        return []


def construct_full_available(cards, suits):
    """
    Construct suit availability grid - a list of available suits for each
    rank slot in each player's deck. Returns grid and array giving the the
    total number of available suits for each slot. 
    """
    num_players, num_in_deck = cards.shape
    num_available = np.ones(cards.shape)*np.nan
        # will store the number of possible cards that can fill each deck slot
    available = []
        # will store the suits that can fill each deck slot
    for player in range(num_players):
        avail_for_player = []
            # holds sublists of available suits for this player for each rank
        for rank in np.arange(num_in_deck): # iterate over card ranks
            a = get_available(cards, suits, player, rank)
                # list suits availed to this player at this rank (can be empty)
            avail_for_player.append(a)
            num_available[player, rank] = len(a)
        available.append(avail_for_player)
    return num_available, available


def deal(num_players=4, num_each_suit=3):
    """ 
    Deals cards. Each player receives a deck containing cards of rank 0 to some
    N. For a given rank, each player will have a card of a different suit. 
    Additionally, within a player's deck there will be an equal number of
    cards of each suit.  Thus the number of suits must equal the number of
    players. The deck size is set by specifying the number of cards per suit
    in each deck. (Deck size is this number times the number of players.)

    Returns an array with the suit of the mth players nth rank card: out[m,n].
    If suit number is less than four, traditional S, H, D, C symbols are used,
    otherwise the suits will be specified by numbers. 

    Example: In the classic setup, four players get three of each suit. A 
    possible (but unlikely) output might be:

         player \ rank | 0   1   2   3   4   5   6   7   8   9  10  11
        ---------------------------------------------------------------
           0           | S   D   C   H   S   D   C   H   S   D   C   H
           1           | H   S   D   C   H   S   D   C   H   S   D   C
           2           | C   H   S   D   C   H   S   D   C   H   S   D
           3           | D   C   H   S   D   C   H   S   D   C   H   S
    """
    REGS_SUITS = ['S', 'H', 'D', 'C']   # suit symbols, used for < 4 players
    # initialize blank decks
    num_players = int(num_players)
    num_each_suit = int(num_each_suit) 
    num_suits = int(num_players)
    num_in_deck = num_each_suit*num_suits  # cards in each player's deck
    players = np.arange(num_players)
    if num_suits <= 4:
        suits = REGS_SUITS[:num_suits] 
    else:
        suits = [str(n + 1) for n in range(num_suits)]
    cards = np.empty((num_players, num_in_deck), dtype=str)
    cards[:, :] = 'X' # X indicates card not yet drawn
    # fill decks
    while np.any(cards == "X"):
        num_available, available = construct_full_available(cards, suits)
        constrained = (num_available == 1) 
        if np.any(constrained):  # first fill fully constrained slots
            for index in zip(*np.nonzero(constrained)):
                cards[index] = available[index[0]][index[1]][0]
        else:
            lowest_avail = np.min(num_available[num_available > 0])
            most_constrained = (num_available == lowest_avail)
                # fill starting with most constrained slots
                # this ensures the grid does not become impossible to finish
            possible_to_fill = np.nonzero(most_constrained)
            num_slot_choices = possible_to_fill[0].size
            target = np.random.randint(num_slot_choices)
                # from most constrained, choose slot to fill at random
            target_index = (possible_to_fill[0][target],
                            possible_to_fill[1][target])
            suits_to_choose = available[target_index[0]][target_index[1]]
            num_suit_choices = num_available[target_index]
            suit_num_chosen = np.random.randint(num_suit_choices)
                # randomly choose filling suit from available suits
            suit_chosen = suits_to_choose[suit_num_chosen]
            cards[target_index] = suit_chosen
    return cards


@click.command()
@click.option('--num_players', default=4,
              help='number of players (default 4)')
@click.option('--num_each_suit', default=3,
              help="number of cards of each suit to deal "
                   "to each player (default 3)")
def start_playoff(num_players, num_each_suit):
    """ """
    num_players = int(num_players)
    num_each_suit = int(num_each_suit) 
    cards = deal(num_players, num_each_suit) # player, rank
    suits = list(cards[:, 0])
    random.shuffle(suits) # determine draft order of suits
    # print results
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        # uses local machine time, it is not timezone-aware.
    print "NFL Fantasy Playoff\n{}".format(now)
    print 
    print "Draft Order: {}".format(", ".join(suits))
    print
    player_list = map(str, np.arange(num_players) + 1)
    print "  Player:  {}".format("  ".join(player_list))
    print "-------------" + '-'*3*(num_players - 1)
    for index in range(num_players*num_each_suit):
        row = cards[:, index]
        print "Round {:2d}:  {}".format(index + 1, "  ".join(row))


if __name__ == "__main__":
    start_playoff()

