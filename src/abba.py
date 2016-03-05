#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import configparser
import collections
import regnet
import rules_generator
import render

"""
Abba: The Abbreviation engine

This application works in several stages:

1. It reads abbreviation definitions written in the regnet markup from a .ini file.
2. It compiles each abbreviation definition into a regnet object in order to
   obtain a regexp and a precedence ranking.
3. It builds an abbreviation dictionary by:
    a. creating a new abbreviation object using the regexp and putting it into
       the correct order indicated by the precedence ranking.
    b. adding that abbreviation's rendering information to a lookup table.
4. It runs through a provided text, replacing matching patterns with single
   unicode control codepoints that are linked to abbreviation objects.
5. It renders the text according to the user's preference, referencing the
   control codepoints to the desired render method.

"""

# Objects which represent abbreviation glyphs and can be regexped.
Abbreviation = collections.namedtuple("Abbreviation", "name, pattern, codepoint")


class AbbreviationRegister(object):

    """
    This object contains sequences of glyph transformations which it can run on
    text objects.
    """

    def __init__(self, config):
        self.abb_sequences = []
        self.lookup_table = {}
        # begin creating unicode characters at the beginning
        # of the private use space
        self.pool = range(57344, 63743)
        # Read through the config file, pulling out abbreviation schemae
        for i, section in zip(self.pool, config.sections()):
            # Analyze the regnet markup and move it into the abbreviation dict
            codepoint = chr(i)
            regnet_object = regnet.Regnet(config[section]['pattern'])
            self.add_to_sequences(section, regnet_object, codepoint)
            for option in config.options(section):
                # Go through each section's options. If it has _rep in it,
                # It's a representation method. Add it to the lookup.
                if option.endswith("_rep"):
                    value = regnet.parse_regnet(list(config[section][option]))
                    self.add_to_lookup(codepoint, section, option=option, value=value)
                    break
            else:
                self.add_to_lookup(codepoint, section)

    def add_to_lookup(self, codepoint, section, option=None, value=None):
        """
        Add a representation method to the reverse lookup table as we create
        the register.
        """
        self.lookup_table.setdefault(codepoint, {'name': section})
        if option and value:
            self.lookup_table[codepoint][option] = value

    def lookup(self, char, option='uni_rep'):
        """
        Generic accessor for the lookup table.
        """
        try:
            return self.lookup_table[char][option]
        except KeyError:
            return self.lookup_table[char]['name']

    def add_to_sequences(self, section, regnet_object, serial):
        """
        Given the makings of an abbreviation, create a new object
        and add it to the sequences list.
        """
        # build abb_sequences to the number of prec levels
        while len(self.abb_sequences) < regnet_object.prec + 1:
            self.abb_sequences.append([])
        # add a new abbreviation object to the correct prec sequence
        self.abb_sequences[regnet_object.prec].append(Abbreviation(
            section, regnet_object.pattern, serial))

    def abbreviate_text(self, text):
        """
        Runs each sequence of transforms in the order they were loaded into the
        controller.
        """
        for sequence in self.abb_sequences:
            for abbreviation in sequence:
                text = re.sub(abbreviation.pattern, abbreviation.codepoint, text)
        return text

    def generate_legend(self):
        """
        Generate a unicode legend to print before the text. Right now
        it's brittle because it assumes unicode renderer.
        """
        return "\n".join("{}: '{}'"
                         .format(self.lookup(key), self.lookup(key, 'name'))
                         for key in self.lookup_table.keys())


def load_rules(filename):
    """
    Build a config object from the provided file
    """
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(),
                                       allow_no_value=True)
    config.read_file(filename)
    return config


if __name__ == "__main__":

    import doctest
    doctest.testmod()

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate',
                        help="Analyze a text for frequency and generate abbreviations on the fly.",
                        action="store_true")
    parser.add_argument("--ruleset",
                        help="The ruleset to use. Uses The New Abbreviations if none is supplied.",
                        default="../tna.ini")
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'))
    parser.add_argument('-t', '--text', nargs="+", help="""	The text to operate on.""")
    parser.add_argument('-r', '--render', help="Render method. Accepts 'unicode' or 'base'.",
                        default='unicode')
    parser.add_argument('-l', '--legend', help="Print a legend at the top of the text.",
                        action="store_true")
    args = parser.parse_args()

    # Determine input method
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip("\r\n")
    elif args.infile:
        text = (args.infile).read()
    elif args.text:
        text = " ".join(args.text)
    else:
        exit("No input received. Run 'python3 abba.py -h' for more information.")

    # Get a ruleset and use it to generate an abbreviation register
    if args.generate:
        abb_config = rules_generator.Generator(text).generate_rules()
    else:
        with open(args.ruleset) as ruleset:
            abb_config = load_rules(ruleset)
    abba = AbbreviationRegister(abb_config)

    # Choose the rendering method
    if args.legend:
        legend = abba.generate_legend()
        print(legend)

    encoding = 'uni_rep' if args.render == 'unicode' else 'name'
    print(render.decode(abba.abbreviate_text(text), abba, encoding))
