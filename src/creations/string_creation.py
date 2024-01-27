from utils import adjustVariableBoundaries
from creations import char_creation
import random


def isSymbol(str):
    return (
        type(str) == type("str") and len(str) == 1 and str[0] >= "a" and str[0] <= "z"
    )


def searchInTheList(arr, value):
    for element in arr:
        if element == value:
            return True

    return False


def create_string(value, variables=None, max_length=None):
    lower_bound = value["lowerBound"]
    upper_bound = value["upperBound"]
    char_features = value["charFeatures"]
    allowed_chars = value["allowedChars"]
    string_features = value["stringFeatures"]
    try:
        lower_bound = (
            int(lower_bound)
            if not isSymbol(lower_bound)
            else adjustVariableBoundaries.get_variable_boundaries(
                variables, lower_bound
            )[0]
        )
        upper_bound = (
            int(upper_bound)
            if not isSymbol(upper_bound)
            else adjustVariableBoundaries.get_variable_boundaries(
                variables, upper_bound
            )[1]
        )
    except Exception as e:
        raise e

    if max_length != None:
        upper_bound = min(upper_bound, max_length)
        if upper_bound < lower_bound:  # BUNU DUSUNMEK LAZIM SONRADAN!
            lower_bound = 1

    if upper_bound < lower_bound:
        raise Exception("Lower bound larger than upper bound")
    if lower_bound <= 0:
        raise Exception("String length must > 0")
    if upper_bound > 1e6:
        raise Exception("String length must be <= 1e6")

    is_digit = searchInTheList(char_features, "Digits")
    is_lowercase = searchInTheList(char_features, "Lowercase")
    is_uppercase = searchInTheList(char_features, "Uppercase")
    is_leading0_allowed = searchInTheList(string_features, "Leading 0")
    is_palindrome = searchInTheList(string_features, "Palindrome")

    random_str_length = random.randint(lower_bound, upper_bound)
    produced_str = ""
    half_length = random_str_length // 2
    if is_palindrome:
        random_str_length = (random_str_length + 1) // 2
    try:
        for i in range(random_str_length):
            created_chr = char_creation.create_char(
                allowed_chars,
                is_lowercase,
                is_uppercase,
                is_digit,
                i == 0 and not is_leading0_allowed,
            )
            produced_str += created_chr

        if is_palindrome:
            half_str = produced_str[0:half_length]
            produced_str += half_str[::-1]

    except Exception as e:
        raise e

    return produced_str
