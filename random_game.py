import random

# here is the class that simulates random Schnapsen game
class SchnapsenRandom:
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


    def play_round(self, leader, player1_hand, player2_hand, trump_suit, declared_marriages):
        if leader == 1:
            leader_hand, follower_hand = player1_hand, player2_hand
        else:
            leader_hand, follower_hand = player2_hand, player1_hand

        # Find possible marriage suits not yet declared
        possible_marriages = {
            suit for suit in self.suits
            if ('K', suit) in leader_hand and ('Q', suit) in leader_hand and suit not in declared_marriages[leader]
        }

        # Leader plays: try to declare marriage if possible
        leader_card = None
        marriage_suit = None
        for suit in possible_marriages:
            for rank in ['K', 'Q']:
                if (rank, suit) in leader_hand:
                    leader_card = (rank, suit)
                    marriage_suit = suit
                    break
            if leader_card:
                break

        if not leader_card:
            leader_card = random.choice(leader_hand)

        leader_hand.remove(leader_card)

        # Follower follows suit if possible
        follow_options = [card for card in follower_hand if card[1] == leader_card[1]]
        if follow_options:
            follower_card = random.choice(follow_options)
        else:
            follower_card = random.choice(follower_hand)
        follower_hand.remove(follower_card)

        # Assign cards back to players
        if leader == 1:
            p1_card, p2_card = leader_card, follower_card
        else:
            p1_card, p2_card = follower_card, leader_card

        # Determine winner
        if p1_card[1] == p2_card[1]:
            winner = 1 if self.card_values[p1_card[0]] > self.card_values[p2_card[0]] else 2
        elif p1_card[1] == trump_suit:
            winner = 1
        elif p2_card[1] == trump_suit:
            winner = 2
        else:
            winner = leader

        round_points = self.card_values[p1_card[0]] + self.card_values[p2_card[0]]
        return winner, round_points, marriage_suit

    def simulate_game(self):
        player1_hand, player2_hand, deck = self.deal_cards()
        trump_card = deck.pop(0)
        trump_suit = trump_card[1]

        player1_score = 0  # ✅ add this
        player2_score = 0  # ✅ and this

        declared_marriages = {1: set(), 2: set()}
        leader = 1

        while player1_hand and player2_hand:
            winner, score, marriage_suit = self.play_round(
                leader, player1_hand, player2_hand, trump_suit, declared_marriages
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

