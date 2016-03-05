import collections
import re
import random


class Generator(object):

    def __init__(self, text):
        # Take some interesting unicode ranges and cat them into a list.
        self.symbol_pool = sum([list(range(x, y)) for x, y in
                                [(383, 447), (502, 687), (913, 1071), (1120, 1319)]], [])
        # shuffle the list. (must be in-place)
        random.shuffle(self.symbol_pool)
        # make an iterator out of the list.
        self.symbol_pool = iter(self.symbol_pool)
        self.text = text

    def token_counter(self, pattern, count):
        """
        Return the <count> most common instances of <pattern> in the text.
        """
        return collections.Counter(
            re.findall(pattern, self.text)
        ).most_common(count)

    def dict_builder(self, counter, name_prefix="", pattern_suffix=""):
        """
        Build a dictionary of regnet-style abbreviation definitions.
        """
        rules = {"abbreviations": []}
        for most_common, _ in counter:
            rules["abbreviations"].append({
                "name": name_prefix + most_common.upper(),
                "pattern": most_common + pattern_suffix,
                "unicode": chr(next(self.symbol_pool))
            })
        return rules

    def generate_rules(self):
        # Build rules dictionary with most common digraphs.
        patterns = self.dict_builder(self.token_counter("\\w\\w", 15), name_prefix='_')
        # Update rules with most common words.
        patterns.update(self.dict_builder(self.token_counter("\\w\\w+", 20),
                                          pattern_suffix="#word"))
        return patterns
