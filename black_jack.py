import random # 

suits = ('Hearts','Diamonds','Spades','Clubs') #suits of the deck
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace') #ranks of the deck
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10, 'Jack':10,
         'Queen':10,'King':10,'Ace':11}
playing = True


# Class to return a string of the suit and rank i.e 'Two of Kings'
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
    	# start with an empty list
        self.deck = []  
        for i in suits:
            for j in ranks:
            	# build Card objects and add them to the list
                self.deck.append(Card(i,j))  
    def __str__(self):
    	# start with an empty string
        deck_co = '' 
        for k in self.deck:
        	# add each Card object print string
            deck_co += '\n '+k.__str__() 
        return 'The deck has:' + deck_co
    # function to shuffle the deck 
    def shuffle(self):
        random.shuffle(self.deck)
    # fucntion to deal cards
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# Class for dealing cards to players hands
class Hand:
    def __init__(self):
    	# start with an empty list
        self.cards = []
        # start with zero value
        self.value = 0  
        # an attribute to keep track of aces 
        self.aces = 0    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        # check for Aces
        if card.rank == 'Ace':
        	# add to self.aces
        	self.aces +=1
    # Adjust for Aces
    def adjust_for_ace(self):
		while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1 

# Class for the Chips
class Chips:
    def __init__(self):
    	# Can be set to default value or by a user input
        self.total = 100
        self.bet = 0
    # Increments total when win
    def win_bet(self):
        self.total += self.bet
    # Decreases total when lose
    def lose_bet(self):
        self.total -= self.bet
# Function for taking hits
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
# Fucntion to ask players to make 
def place_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()
def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()
def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()   
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()  
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")
while True:
    # Print an opening statement
    print('Welcome to BlackJack!\n')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    # Set up the Player's chips
    player_chips = Chips()  # remember the default value is 100    
    # Prompt the Player for their bet
    place_bet(player_chips)
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand) 
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)  
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
        # Show all cards
        show_all(player_hand,dealer_hand) 
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)   
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",player_chips.total)
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break