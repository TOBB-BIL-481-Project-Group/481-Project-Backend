import random
from consts import alphabetChars


def is_special_char(chr):
    if chr >= "0" and chr <= "9":
        return False
    elif chr >= "a" and chr <= "z":
        return False
    elif chr >= "A" and chr >= "Z":
        return False
    return True


def searchInTheList(arr, value):
    for element in arr:
        if element == value:
            return True
    return False


def create_char(
    allowed_chars=None,
    is_lowercase_allowed=None,
    is_uppercase_allowed=None,
    is_digits_allowed=None,
    should_non_zero=False,
    value=None,
):
    if value != None:
        allowed_chars = value["allowedChars"]
        is_lowercase_allowed = searchInTheList(value["selectedFeatures"], "Lowercase")
        is_uppercase_allowed = searchInTheList(value["selectedFeatures"], "Uppercase")
        is_digits_allowed = searchInTheList(value["selectedFeatures"], "Digits")

    alphabet = []

    is_all_alphabet = (
        not is_lowercase_allowed
        and not is_digits_allowed
        and not is_uppercase_allowed
        and len(allowed_chars) == 0
    )

    if is_lowercase_allowed or is_all_alphabet:
        for i in range(ord("a"), ord("z") + 1):
            alphabet.append(chr(i))
    if is_uppercase_allowed or is_all_alphabet:
        for i in range(ord("A"), ord("Z") + 1):
            alphabet.append(chr(i))
    if is_digits_allowed or is_all_alphabet:
        for i in range(ord("1") if should_non_zero else ord("0"), ord("9") + 1):
            alphabet.append(chr(i))

    for element in allowed_chars:
        if should_non_zero and element == "0":
            continue
        alphabet.append(element)

    alphabet = list(set(alphabet))  # to make it unique.

    if len(alphabet) == 0:
        raise Exception("No choice is possible!: char_creation")

    random_chr = random.choice(alphabet)
    return random_chr
