import random

# here is the class that simulates Schnapsen game with some strategy
class SchnapsenStrategy:
    def __init__(self):
        # add card's value, based on Schanpsen rules
        self.card_values = {'A': 11, '10': 10, 'K': 4, 'Q': 3, 'J': 2}
        self.marriage_scores = {'non-trump': 20, 'trump': 40}
        # create the deck
        self.suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        # create the deck, every card have value and suit
        self.deck = [(value, suit) for value in self.card_values for suit in self.suits]

    def deal_cards(self):
        # shuffle and deal the cards to the players
        # player1 - first 5. player 2- second 5 and other left to the deck
        random.shuffle(self.deck)
        return self.deck[:5], self.deck[5:10], self.deck[10:]

    def draw_cards(self, player1_hand, player2_hand, deck, winner):
        # the player who won the level draw the first card if the deck is not empty
        if deck:
            if winner == 1:
                player1_hand.append(deck.pop(0))
                if deck:
                    player2_hand.append(deck.pop(0))
            else:
                player2_hand.append(deck.pop(0))
                if deck:
                    player1_hand.append(deck.pop(0))

    def declare_marriage(self, hand, trump_suit):
        marriage_score = 0
        # collect the unique suits in the hand
        suits_in_hand = {card[1] for card in hand}
        # check if there is king and queen of the same suit
        for suit in suits_in_hand:
            if ('K', suit) in hand and ('Q', suit) in hand:
                marriage_score += self.marriage_scores['trump' if suit == trump_suit else 'non-trump']
        return marriage_score

    def play_round(self, leader, player1_hand, player2_hand, trump_suit, declared_marriages, deck):
        must_follow_suit = len(deck) == 0

        if leader == 1:
            leader_hand = player1_hand
            follower_hand = player2_hand
        else:
            leader_hand = player2_hand
            follower_hand = player1_hand

        # Marriage declaration by leader
        possible_marriages = {
            suit for suit in self.suits
            if ('K', suit) in leader_hand and ('Q', suit) in leader_hand and suit not in declared_marriages[leader]
        }

        leader_card = None
        marriage_suit = None
        for suit in possible_marriages:
            if ('Q', suit) in leader_hand:
                leader_card = ('Q', suit)
                marriage_suit = suit
                break
            elif ('K', suit) in leader_hand:
                leader_card = ('K', suit)
                marriage_suit = suit
                break

        if not leader_card:
            # No marriage to declare — choose smart lead
            non_trump_cards = [card for card in leader_hand if card[1] != trump_suit]
            trump_cards = [card for card in leader_hand if card[1] == trump_suit]

            # Prefer to lead with a low non-trump card
            if non_trump_cards:
                leader_card = min(non_trump_cards, key=lambda c: self.card_values[c[0]])
            elif trump_cards:
                # If only trumps, lead with lowest trump
                leader_card = min(trump_cards, key=lambda c: self.card_values[c[0]])
            else:
                # Fallback: just play the lowest card
                leader_card = min(leader_hand, key=lambda c: self.card_values[c[0]])

        leader_hand.remove(leader_card)

        # Follower strategy logic
        follow_suit_cards = [card for card in follower_hand if card[1] == leader_card[1]]
        higher_follow_cards = [c for c in follow_suit_cards if
                               self.card_values[c[0]] > self.card_values[leader_card[0]]]
        trump_cards = [card for card in follower_hand if card[1] == trump_suit]
        non_trump_cards = [card for card in follower_hand if card[1] != trump_suit]

        if must_follow_suit:
            if follow_suit_cards:
                if higher_follow_cards:
                    follower_card = min(higher_follow_cards, key=lambda c: self.card_values[c[0]])
                else:
                    follower_card = min(follow_suit_cards, key=lambda c: self.card_values[c[0]])
            elif trump_cards:
                follower_card = min(trump_cards, key=lambda c: self.card_values[c[0]])
            else:
                follower_card = min(follower_hand, key=lambda c: self.card_values[c[0]])
        else:
            # Flexible strategy
            if higher_follow_cards:
                follower_card = min(higher_follow_cards, key=lambda c: self.card_values[c[0]])
            elif leader_card[0] in ['A', '10'] and trump_cards:
                follower_card = min(trump_cards, key=lambda c: self.card_values[c[0]])
            elif non_trump_cards:
                follower_card = min(non_trump_cards, key=lambda c: self.card_values[c[0]])
            elif follow_suit_cards:
                # Only now use follow suit (even if it's lower), as last resort
                follower_card = min(follow_suit_cards, key=lambda c: self.card_values[c[0]])
            else:
                follower_card = min(follower_hand, key=lambda c: self.card_values[c[0]])

        follower_hand.remove(follower_card)

        # Assign played cards back to players
        if leader == 1:
            p1_card, p2_card = leader_card, follower_card
        else:
            p1_card, p2_card = follower_card, leader_card

        # Determine round winner
        if p1_card[1] == p2_card[1]:
            winner = 1 if self.card_values[p1_card[0]] > self.card_values[p2_card[0]] else 2
        elif p1_card[1] == trump_suit:
            winner = 1
        elif p2_card[1] == trump_suit:
            winner = 2
        else:
            winner = leader

        points = self.card_values[p1_card[0]] + self.card_values[p2_card[0]]
        return winner, points, marriage_suit

    def simulate_game(self):
        player1_hand, player2_hand, deck = self.deal_cards()
        trump_card = deck.pop(0)
        trump_suit = trump_card[1]
        player1_score, player2_score = 0, 0
        declared_marriages = {1: set(), 2: set()}
        leader = 1

        while player1_hand and player2_hand:
            winner, score, marriage_suit = self.play_round(
                leader, player1_hand, player2_hand, trump_suit, declared_marriages, deck
            )

            if marriage_suit:
                declared_marriages[leader].add(marriage_suit)
                score += self.marriage_scores['trump' if marriage_suit == trump_suit else 'non-trump']

            if winner == 1:
                player1_score += score
            else:
                player2_score += score

            self.draw_cards(player1_hand, player2_hand, deck, winner)
            leader = winner

            if player1_score >= 66 or player2_score >= 66:
                break

        if player1_score >= 66:
            return 1
        elif player2_score >= 66:
            return 2
        else:
            return 1 if player1_score > player2_score else 2 if player2_score > player1_score else 0

    def simulate_games(self, num_games):
        wins = {1: 0, 2: 0, 'draw': 0}
        for _ in range(num_games):
            winner = self.simulate_game()
            if winner:
                wins[winner] += 1
            else:
                wins['draw'] += 1  # Count draws where both have the same score and less than 66
        return wins

