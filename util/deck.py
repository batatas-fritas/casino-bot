import random

class Suits:
    DIAMONDS = '♦️'
    CLUBS = '♣️'
    SPADES = '♠️'
    HEARTS = '♥️'

class Card():
    def __init__(self, suit: Suits, number) -> None:
        self.suit = suit
        self.number = number
    
    def toString(self) -> str:
        if self.number > 1 and self.number < 11:
            return str(self.number)
        if self.number == 1:
            return "A"
        if self.number == 11:
            return "J"
        if self.number == 12:
            return "Q"
        if self.number == 13:
            return "K"
    
    def getBlackjackValue(self) -> int:
        if self.number > 10: return 10
        if self.number == 1: return 11 # Ace
        else: return self.number
         

class Deck():
    def __init__(self) -> None:
        self.cards = []
        self.refresh()
        self.shuffle()
    
    def refresh(self):
        self.cards = []
        suit = None
        for i in range(4):
            if i == 0:
                suit = Suits.CLUBS
            if i == 1:
                suit = Suits.DIAMONDS
            if i == 2:
                suit = Suits.SPADES
            if i == 3:
                suit = Suits.HEARTS
            for j in range(1,14):
                self.cards.append(Card(suit, j))
    
    def shuffle(self):
        random.shuffle(self.cards)

    def takeCard(self) -> Card:
        return self.cards.pop()
    
    def print(self):
        for card in self.cards:
            print(f"{card.toString()} {card.suit}")
