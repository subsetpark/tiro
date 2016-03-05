import re


rules = [
    (re.compile("(?P<pat>\\w+)#pref"), "(?<=\\\\b)\g<pat>", 3),
    (re.compile("(?P<pat>\\w+)#suf"), "\g<pat>(?=\\\\b)", 3),
    (re.compile("(?P<pat>\\w+)#init"), "(?<=\\\\b)\g<pat>", 0),
    (re.compile("(?P<pat>\\w+)#final"), "\g<pat>(?=\\\\b)", 0),
    (re.compile("(?P<pat>\\w+)#iso"), "(?<=\\\\b)\g<pat>(?=\\\\b)", 0),
    (re.compile("(?P<pat>\\w+)#word"), "(?<=\\\\b)\g<pat>", 1),
    (re.compile("(?P<pat>^\\w\\w\\w$)"), "\g<pat>", 3),
    (re.compile("(?P<pat>^\\w\\w$)"), "\g<pat>", 4),
    (re.compile("(?P<pat>^\\w$)"), "\g<pat>", -1),
    (re.compile("(?P<pat>\\w+)#vow"), "(?<=[aeiouy])\g<pat>", 2),
    (re.compile("(?P<pat>\\w+)#hard"), "\g<pat>", 0)
]

REGNET_CONTROL = "/"


class Regnet(object):

    def __init__(self, pattern):
        """
        Given a user-defined pattern, compile it into a regnet.
        A regnet has two parts: a compiled regexp, and its precedence level.

        So a finalized regnet takes this:
        "foo#init"

        And produces:
        a compiled regexp for "(?<=\\\\b)foo" and
        prec = 0

        """

        # find the rule that applies to this regnet, compile a regexp and assign
        for rule in rules:
            if re.match(rule[0], pattern):
                self.pattern = re.compile(re.sub(rule[0], rule[1], pattern), re.IGNORECASE)
                self.prec = rule[2]
                break
        else:
            self.prec = -1
            self.pattern = re.compile(pattern, re.IGNORECASE)


class Parser(object):

    def __init__(self, ruleset, encoding):
        self.aliases = ruleset.get("aliases", {})
        self.abbreviations = ruleset.get("abbreviations", [])
        for abbreviation in self.abbreviations:
            value = abbreviation.get(encoding, "")
            if value:
                tokens = value.split(REGNET_CONTROL)
                interpolated = [self.interpolate_token(t) for t in tokens]
                abbreviation[encoding] = "".join(interpolated)

    def interpolate_token(self, value):
        """
        Read the .ini formatting looking for references to unicode characters.
        Recurse through the display value, replacing codepoint references as you
        go.
        """

        if value in self.aliases:
            return self.interpolate_token(self.aliases[value])
        try:
            # Interpolate bare codepoint references into unicode characters
            base_16 = int(value, 16)
            return chr(base_16)
        except ValueError:
            return value
