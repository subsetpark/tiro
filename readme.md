# Abba: The Abbreviation engine

This application works in several stages:

1. It reads abbreviation definitions written in the regnet markup from a .ini file.
2. It compiles each abbreviation definition into a regnet object in order to obtain a regexp and a precedence ranking.
3. It builds an abbreviation dictionary by:
	a. creating a new abbreviation object using the regexp and putting it into the correct order indicated by the precedence ranking.
	b. adding that abbreviation's rendering information to a lookup table.
4. It runs through a provided text, replacing matching patterns with single unicode control codepoints that are linked to abbreviation objects.
5. It renders the text according to the user's preference, referencing the control codepoints to the desired render method.


abba requires python3.
