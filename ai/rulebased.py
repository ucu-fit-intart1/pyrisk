from ai import AI
import random
import collections

RULE_ANTECEDENT_SIZE = 6

class RuleBasedAI(AI):
    """
    RuleBasedAI: Plays a by following a given set of rules.
    """
    def __init__(self, player, game, world, **kwargs):
        AI.__init__(self, player, game, world, **kwargs)
        rules = kwargs.get('rules')
        if not rules:
            rules = self.random_rules(world.territories)
        self.rules = rules

    def random_rules(self, territories, levelCount=10, ruleCount=20):
        return [
            [self.random_rule(territories) for i in range(ruleCount)]
            for i in range(levelCount)
        ]

    def random_rule(self, territories):
        territories = list(territories.keys())
        random.shuffle(territories)
        antecedent = {
            k: (random.randint(0,5), min(random.randint(1,30), random.randint(0,30)))  
            for k in territories[:RULE_ANTECEDENT_SIZE]
        }
        consequent = territories[RULE_ANTECEDENT_SIZE]
        return (antecedent, consequent)
            
    def check_rules(self, rules):
        matches = []
        for level in rules:
            matches = list(filter(lambda v: v is not None, [self.check_rule(rule) for rule in level]))
            if matches:
                break
        return matches

    def get_player_turn(self, player):
        for (p, i) in zip(self.game.turn_order, range(6)):
            if p == player:
                return i
        return -1

    def check_rule(self, rule):
        antecedent, consequent = rule
        for (t, (p, c)) in antecedent.items():
            t = self.world.territories[t]
            if self.get_player_turn(t.owner) < p and t.forces < c:
                return None
        return consequent

    ################################################################################################

    def initial_placement(self, empty, remaining):
        """
        """
        matches = set(self.check_rules(self.rules))
        if empty:
            emptyMatches = list(matches.intersection(empty))
            return random.choice(emptyMatches or empty)
        else:
            playerMatches = list(matches.intersection(self.player.territories))
            return random.choice(playerMatches or list(self.player.territories))

    def attack(self):
        """TODO
        """
        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
                    if t.forces > a.forces:
                        yield (t, a, None, None)

    def reinforce(self, available):
        """TODO
        """
        matches = set(self.check_rules(self.rules))
        result = collections.defaultdict(int)
        
        border = [t for t in self.player.territories if t.border]
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result
