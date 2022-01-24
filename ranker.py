class Ranker:

    def __init__(self, cards):

        self.cards = cards

        self.spades = [card for card in cards if card.suit == 'spades']
        self.hearts = [card for card in cards if card.suit == 'hearts']
        self.clubs = [card for card in cards if card.suit == 'clubs']
        self.diamonds = [card for card in cards if card.suit == 'diamonds']

    # flush function
    def is_flush(self):
        if len(self.spades) >= 5 or len(self.hearts) >= 5 or len(self.clubs) >= 5 or len(self.diamonds) >= 5:
            if len(self.spades) >= 5:
                return self.sorted_ranks(self.spades, wheel_ace=False)[0]
            elif len(self.hearts) >= 5:
                return self.sorted_ranks(self.hearts, wheel_ace=False)[0]
            elif len(self.clubs) >= 5:
                return self.sorted_ranks(self.clubs, wheel_ace=False)[0]
            elif len(self.diamonds) >= 5:
                return self.sorted_ranks(self.diamonds, wheel_ace=False)[0]
        return False

    # strait functions
    def ranks(self, cards, wheel_ace=True):
        ranks = []
        for rank in [card.rank for card in cards]:
            if rank == 'A':
                ranks.append(14)
                if wheel_ace:
                    ranks.append(1)
            elif rank == 'K':
                ranks.append(13)
            elif rank == 'Q':
                ranks.append(12)
            elif rank == 'J':
                ranks.append(11)
            else:
                ranks.append(int(rank))
        return ranks
        # return sorted(ranks, reverse=True)

    def sorted_ranks(self, cards, wheel_ace=True):
        return sorted(self.ranks(cards, wheel_ace=wheel_ace), reverse=True)

    def unique_sorted_ranks(self, cards):
        return list(dict.fromkeys(self.sorted_ranks(cards)))

    def has_strait(self, cards):
        count = 0
        unique_sorted_cards = self.unique_sorted_ranks(cards)
        for i in range(len(unique_sorted_cards) - 1):
            if unique_sorted_cards[i] == unique_sorted_cards[i + 1] + 1:
                count += 1
                if count == 4:
                    return unique_sorted_cards[i] - 1
            else:
                count = 0
        return False

    def is_strait(self):
        return self.has_strait(self.cards)

    # strait flush function
    def is_strait_flush(self):
        if self.is_strait() and self.is_flush():
            for cards in [self.spades, self.hearts, self.clubs, self.diamonds]:
                if self.has_strait(cards):
                    return self.has_strait(cards)
        return False

    # pair functions
    def has_pair(self, cards):
        count = 0
        sorted_cards = self.sorted_ranks(cards)
        for i in range(len(sorted_cards) - 1):
            if sorted_cards[i] == sorted_cards[i + 1]:
                return sorted_cards[i]
                # count += 1
                # if count == 1:
                #    return True
            else:
                count = 0
        return False

    def is_pair(self):
        return self.has_pair(self.cards)

    # trips functions
    def has_trips(self, cards):
        count = 0
        sorted_cards = self.sorted_ranks(cards)
        for i in range(len(sorted_cards) - 1):
            if sorted_cards[i] == sorted_cards[i + 1]:
                count += 1
                if count == 2:
                    return sorted_cards[i]
            else:
                count = 0
        return False

    def is_trips(self):
        return self.has_trips(self.cards)

    # quads function
    def is_quads(self):
        count = 0
        sorted_cards = self.sorted_ranks(self.cards)
        for i in range(len(sorted_cards) - 1):
            if sorted_cards[i] == sorted_cards[i + 1]:
                count += 1
                if count == 3:
                    return sorted_cards[i]
            else:
                count = 0
        return False

    # two pair functions
    def is_two_pair(self):
        pair_rank = self.is_pair()
        cards = []
        if pair_rank:
            for i in range(6):
                if self.ranks(self.cards, wheel_ace=False)[i] != pair_rank:
                    cards.append(self.cards[i])
            if self.has_pair(cards):
                return pair_rank, self.has_pair(cards)
        return False

    # full house functions
    def is_full_house(self):
        trips_rank = self.is_trips()
        cards = []
        if trips_rank:
            for i in range(7):
                if self.ranks(self.cards, wheel_ace=False)[i] != trips_rank:
                    cards.append(self.cards[i])
            if self.has_pair(cards):
                return 15 * trips_rank + self.has_pair(cards)
        return False

    # calculate rank
    def calculate_major_rank(self):
        if self.is_strait_flush():
            return 8  # 'Strait Flush'
        elif self.is_quads():
            return 7  # '4 of a Kind'
        elif self.is_full_house():
            return 6  # 'Full House'
        elif self.is_flush():
            return 5  # 'Flush'
        elif self.is_strait():
            return 4  # 'Strait'
        elif self.is_trips():
            return 3  # '3 of a Kind'
        elif self.is_two_pair():
            return 2  # 'Two Pair'
        elif self.is_pair():
            return 1  # 'Pair'
        else:
            return 0  # 'High Card'

    def calculate_minor_rank(self):
        major_rank = self.calculate_major_rank()
        if major_rank == 8:
            return self.is_strait_flush()
        if major_rank == 7:  # four of a kind
            minor_rank = self.is_quads()
            cards = []
            for i in range(7):
                if self.ranks(self.cards, wheel_ace=False)[i] != minor_rank:
                    cards.append(self.cards[i])
            kicker_ranks = self.sorted_ranks(cards, wheel_ace=False)
            return minor_rank * 15 + kicker_ranks[0]
        if major_rank == 6:
            return self.is_full_house()
        if major_rank == 5:
            return self.is_flush()
        if major_rank == 4:
            return self.is_strait()
        if major_rank == 3:  # three of a kind
            minor_rank = self.is_trips()
            cards = []
            for i in range(7):
                if self.ranks(self.cards, wheel_ace=False)[i] != minor_rank:
                    cards.append(self.cards[i])
            kicker_ranks = self.sorted_ranks(cards, wheel_ace=False)
            return minor_rank * 15 * 15 + kicker_ranks[0] * 15 + kicker_ranks[1]
        if major_rank == 2:  # two pair
            minor_rank_high, minor_rank_low = self.is_two_pair()
            cards = []
            for i in range(7):
                if self.ranks(self.cards, wheel_ace=False)[i] != minor_rank_high and \
                        self.ranks(self.cards, wheel_ace=False)[i] != minor_rank_low:
                    cards.append(self.cards[i])
            kicker_ranks = self.sorted_ranks(cards, wheel_ace=False)
            return minor_rank_high * 15 * 15 + minor_rank_low * 15 + kicker_ranks[0]
        if major_rank == 1:  # pair
            minor_rank = self.is_trips()
            cards = []
            for i in range(7):
                if self.ranks(self.cards, wheel_ace=False)[i] != minor_rank:
                    cards.append(self.cards[i])
            kicker_ranks = self.sorted_ranks(cards, wheel_ace=False)
            return minor_rank * 15 * 15 * 15 + kicker_ranks[0] * 15 * 15 + kicker_ranks[1] * 15 + kicker_ranks[2]
        if major_rank == 0:  # high card
            kicker_ranks = self.sorted_ranks(self.cards, wheel_ace=False)
            return kicker_ranks[0] * 15 * 15 * 15 * 15 + kicker_ranks[1] * 15 * 15 * 15 + kicker_ranks[2] * 15 * 15 + \
                   kicker_ranks[3] * 15 + kicker_ranks[4]

def determine_winner(hand_one, hand_two):
    ranker_one = Ranker(hand_one)
    ranker_two = Ranker(hand_two)

    if ranker_one.calculate_major_rank() > ranker_two.calculate_major_rank():
        return 1  # 'Hand one wins', ranker_one.calculate_major_rank(), ranker_two.calculate_major_rank()
    elif ranker_one.calculate_major_rank() < ranker_two.calculate_major_rank():
        return 2  # 'Hand two wins', ranker_one.calculate_major_rank(), ranker_two.calculate_major_rank()
    elif ranker_one.calculate_minor_rank() > ranker_two.calculate_minor_rank():
        return 1  # 'Hand one wins', ranker_one.calculate_major_rank(), ranker_two.calculate_major_rank()
    elif ranker_one.calculate_minor_rank() < ranker_two.calculate_minor_rank():
        return 2  # 'Hand two wins', ranker_one.calculate_major_rank(), ranker_two.calculate_major_rank()
    else:
        return 0  # 'draw'