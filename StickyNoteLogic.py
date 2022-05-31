# Backend development - the functions in this file will be tested in 'StickyNoteTester.py'

# Given a string s, capitalizes all letters in said string
def capitalize_all_characters(s):
    new_string = "" # the string to be returned
    difference = 32 # difference between lower and capital 'A' for conversion
    for c in s:
        # Lower case, switch to capital
        if c >= 'a' and c <= 'z':
            # Appending with '+='
            # https://stackoverflow.com/questions/12169839/which-is-the-preferred-way-to-concatenate-a-string-in-python
            new_string += chr(ord(c) - difference)
        else: # All other characters, simply append as normal
            new_string += c

    # Return the new string
    return new_string

# Given a string s, lower-case all letters in said string
def lowercase_all_characters(s):
    new_string = "" # the string to be returned
    difference = 32 # difference between lower and capital 'A' for conversion
    for c in s:
        # Upper case, switch to lower case
        if c >= 'A' and c <= 'Z':
            # Appending with '+='
            # https://stackoverflow.com/questions/12169839/which-is-the-preferred-way-to-concatenate-a-string-in-python
            new_string += chr(ord(c) + difference)
        else: # All other characters, simply append as normal
            new_string += c

    # Return the new string
    return new_string