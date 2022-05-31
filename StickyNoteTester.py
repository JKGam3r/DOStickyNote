import unittest
from StickyNoteLogic import *

# Test all cases in the StickyNoteLogic python file
class MyTestCase(unittest.TestCase):
    # Test the capitalize_all_characters() function
    def test_capitalize_all_characters(self):
        '''
        TEST 0, 1, MANY - refers to length of input
        '''
        # Length 0
        self.assertEqual(capitalize_all_characters(""), "")
        # Length 1
        self.assertEqual(capitalize_all_characters("a"), "A") # capitalize
        self.assertEqual(capitalize_all_characters("G"), "G") # already capped
        self.assertEqual(capitalize_all_characters("%"), "%") # not a letter
        # Length MANY
        self.assertEqual(capitalize_all_characters("my name is python"), "MY NAME IS PYTHON") # all lowercase
        self.assertEqual(capitalize_all_characters("GREAT SCOTT"), "GREAT SCOTT") # all uppercase already
        self.assertEqual(capitalize_all_characters("r@Nd0M a55OrTm3nt"), "R@ND0M A55ORTM3NT") # a mix
        self.assertEqual(capitalize_all_characters("     "), "     ") # only spaces
        self.assertEqual(capitalize_all_characters("  j  "), "  J  ") # spaces with a character
        self.assertEqual(capitalize_all_characters("\tab"), "\tAB") # use of escape sequences
        self.assertEqual(capitalize_all_characters("NEW\nline"), "NEW\nLINE") # another escape sequence test

        '''
        TEST FIRST, MIDDLE, LAST - refers to capitalizing different parts of input
        '''
        # FIRST
        self.assertEqual(capitalize_all_characters("a STRING IS PRESENT"), "A STRING IS PRESENT")
        # LAST
        self.assertEqual(capitalize_all_characters("A STRING IS PRESENt"), "A STRING IS PRESENT")
        # MIDDLE
        self.assertEqual(capitalize_all_characters("A sTRING IS PRESENT"), "A STRING IS PRESENT")
        self.assertEqual(capitalize_all_characters("A STRiNG IS PRESENT"), "A STRING IS PRESENT")
        self.assertEqual(capitalize_all_characters("A STRINg IS PRESENT"), "A STRING IS PRESENT")
        self.assertEqual(capitalize_all_characters("A STRING iS PRESENT"), "A STRING IS PRESENT")
        self.assertEqual(capitalize_all_characters("A STRING iS pRESENT"), "A STRING IS PRESENT")
        self.assertEqual(capitalize_all_characters("A sTRiNg is PrEsEnT"), "A STRING IS PRESENT")
        self.assertEqual(capitalize_all_characters("a sTRiNg is PrEsEnt"), "A STRING IS PRESENT")

    # Test the lowercase_all_characters() function
    def test_lowercase_all_characters(self):
        '''
        TEST 0, 1, MANY - refers to length of input
        '''
        # Length 0
        self.assertEqual(lowercase_all_characters(""), "")
        # Length 1
        self.assertEqual(lowercase_all_characters("A"), "a") # lower case
        self.assertEqual(lowercase_all_characters("g"), "g") # already lower case
        self.assertEqual(lowercase_all_characters("%"), "%") # not a letter
        # Length MANY
        self.assertEqual(lowercase_all_characters("MY NAME IS PYTHON"), "my name is python") # all upper case
        self.assertEqual(lowercase_all_characters("great scott"), "great scott") # all lower case already
        self.assertEqual(lowercase_all_characters("r@Nd0M a55OrTm3nt"), "r@nd0m a55ortm3nt") # a mix
        self.assertEqual(lowercase_all_characters("     "), "     ") # only spaces
        self.assertEqual(lowercase_all_characters("  J  "), "  j  ") # spaces with a character
        self.assertEqual(lowercase_all_characters("\tAB"), "\tab") # use of escape sequences
        self.assertEqual(lowercase_all_characters("NEW\nline"), "new\nline") # another escape sequence test

        '''
        TEST FIRST, MIDDLE, LAST - refers to lower-casing different parts of input
        '''
        # FIRST
        self.assertEqual(lowercase_all_characters("A string is present"), "a string is present")
        # LAST
        self.assertEqual(lowercase_all_characters("a string is presenT"), "a string is present")
        # MIDDLE
        self.assertEqual(lowercase_all_characters("a String is present"), "a string is present")
        self.assertEqual(lowercase_all_characters("a strIng is present"), "a string is present")
        self.assertEqual(lowercase_all_characters("a string Is present"), "a string is present")
        self.assertEqual(lowercase_all_characters("a string is presEnt"), "a string is present")
        self.assertEqual(lowercase_all_characters("a StrInG iS PresEnt"), "a string is present")
        self.assertEqual(lowercase_all_characters("A StrInG iS PresEnT"), "a string is present")

if __name__ == '__main__':
    unittest.main()
