"""
Simulation of a game of blackjack
"""

# Imports and global variables
import random
import time
import sys

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


# Classes
class Card:
    """
    Create card objects based on suits, ranks and values
    """

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    """
    Create 52 cards (a deck)
    """

    def __init__(self):
        self.deck = list()
        # Add each combination of cards in the deck list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        cards = list()
        for card in self.deck:
            cards.append(str(card))
        return str(cards)

    def shuffle(self):
        """
        Shuffle the list of cards
        """
        random.shuffle(self.deck)

    def deal(self):
        """
        Deal a random card and removing it from the list
        :return: deleted/dealed card
        """
        return self.deck.pop()


class Hand:
    """
    Class to manage what cards the player took
    """
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        """
        Add the dealed card to the hand of the player
        :param card: card that was taken by the Deck.deal method
        """
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def __str__(self):
        cards = ""
        for card in self.cards:
            cards += str(card) + " "
        return cards

    def adjust_for_aces(self):
        """
        If the hand values more than 21 and there are aces on it,
         we pass to consider the aces as 1 instead of 11
        """
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    """
    Class to manage bets and the amount of money of the play
    """

    def __init__(self):
        self.total = 500
        self.bet = 0

    def take_bet(self, bet):
        """
        Take the vlaue of the bet from the player
        :param bet: value of the bet
        """
        self.bet = bet

    def win_bet(self):
        """
        Player wins the game and wins the bet
        """
        self.total += self.bet

    def lose_bet(self):
        """
        PLayer loses the game and loses the bet
        """
        self.total -= self.bet


# Functions
def take_bet(chips):
    """
    Take the bet of the player
    :param chips: Instance of Chips' class
    """
    while True:
        bet = float(input("Bet: $"))
        if bet <= chips.total:
            return bet
        print("Not enough cash!")


def hit(deck_of_cards, hand):
    """
    Add a card to the player or the dealer
    :param deck_of_cards: deck
    :param hand: hand of the player in turn
    """
    card = deck_of_cards.deal()
    hand.add_card(card)
    return card


def hit_or_stand(cards, cards_in_hand):
    """
    Ask the player if he wants to hit or to stand
    :param cards: deck
    :param cards_in_hand: hand
    """
    global playing
    while True:
        choose = str(input("\nHit or stand? ").lower())
        if choose in ('hit', 'stand'):
            break
        print("Make sure you are typing correctly")

    if choose == 'stand':
        playing = False
    else:
        playing = True
        hit(cards, cards_in_hand)


def show_some(player_cards, dealer_cards):
    """
    Show all the cards, except the dealer's hidden one
    :param player_cards: player's hand
    :param dealer_cards: dealer's hand
    """
    print(f"Player's hand: {player_cards.value}\n{player_cards}")
    print(f"Dealer's hand: {dealer_cards.cards[0]}")


def show_all(player_cards, dealer_cards):
    """
    Show all the cards
    :param player_cards: player's hand
    :param dealer_cards: dealer's hand
    """
    print(f"Player's hand: {player_cards.value}\n{player_cards}")
    print(f"Dealer's hand: {dealer_cards.value}\n{dealer_cards}\n")


def got_21(hand, chips, is_player):
    """
    Check if someone got 21
    :param hand: cards of one of the players
    :param chips: player's chips
    :param is_player: if it is the player or the dealer playing
    :return: true if somebody got 21
    """
    if hand.value == 21:
        if is_player:
            print("\n\nCONGRATULATIONS! YOU GOT 21!!!!!\n\n")
            chips.win_bet()
        else:
            print("\n\nDealer got 21! More luck to you next time!\n\n")
            chips.lose_bet()
        return True
    return False


def busted(hand, chips, is_player):
    """
    Check if someone got 21
    :param hand: cards of one of the players
    :param chips: player's chips
    :param is_player: if it is the player or the dealer playing
    :return: true if somebody busted
    """
    if hand.value > 21:
        if is_player:
            print("\n\nYOU BUSTED =/\n\n")
            chips.lose_bet()
        else:
            print("\n\nDEALER BUSTED! YOU WIN!\n\n")
        return True
    return False


def count_points(player, dealer):
    """
    If nobody busted or got 21, we gotta count the points of both player and see who won
    :param player: hands of the player
    :param dealer: hands of the dealer
    """
    if player.value > dealer.value:
        print("\n\nYOU WON!!!\n\n")
    elif dealer.value > player.value:
        print("\n\nDEALER WON!!!\n\n")
    else:
        print("\n\nIT'S A DRAW!!!\n\n")


def play_again():
    """
    Checking if the player wants to play again
    :return: true if the player wants to play again
    """
    while True:
        yes_or_no = str(input("\nDo you want to play again? [yes/no] ")).lower()
        if yes_or_no in ('yes', 'no'):
            break

    return yes_or_no == 'yes'


def start():
    """
    Start the program (main function)
    """
    # Greeting message
    print("Welcome to blackjack!")

    # Creating deck of cards
    deck = Deck()
    deck.shuffle()

    # Creating the two hands: dealer and player and giving two cards to each one
    player = Hand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer = Hand()
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    # Creating a bet
    bet = Chips()
    value = take_bet(bet)
    bet.take_bet(value)
    print(f"Your bet is ${bet.bet :.2f}\nHave a good luck!\n")

    # Showing cards
    show_some(player, dealer)

    # Run this block of code while the player choose to stand
    while True:
        # Checking wheter the player want a new card
        hit_or_stand(deck, player)
        if not playing:
            print("Ok, it's dealer's time now!")
            break

        # Adjusting for aces
        player.adjust_for_aces()

        # Showing the new hand
        print(f"You got a {player.cards[-1]}!\n")
        show_some(player, dealer)

        # Checking if the player got 210
        if got_21(player, bet, True):
            if play_again():
                start()
            sys.exit()

        # Checking if the player busted
        if busted(player, bet, True):
            if play_again():
                start()
            sys.exit()

    # It's dealer turn now. He turn his hidden card up
    print(f"\nDealer's hidden card was a {dealer.cards[-1]}")
    show_all(player, dealer)

    # Dealer will continue to hit until he surpasses the player's points
    while dealer.value <= player.value:
        # Adding card to the dealer's deck
        time.sleep(2)
        dealer.add_card(deck.deal())

        # Printing new hands
        print(f"Dealer got a {dealer.cards[-1]}\n")
        show_all(player, dealer)

        # Adjust aces
        dealer.adjust_for_aces()

        # Checking if the dealer busted
        if busted(dealer, bet, False):
            if play_again():
                start()
            sys.exit()

        # Checking if the dealer got 21
        if got_21(dealer, bet, False):
            if play_again():
                start()
            sys.exit()

    # Nobody got 21 or busted, so we now show the points
    count_points(player, dealer)

    # Checking if the player wants to play again
    if play_again():
        start()


# Run main
start()
