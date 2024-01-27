import random
import sys

sys.path.append("../utils")
from utils import get_primes
from utils import adjustVariableBoundaries


def isSymbol(str):
    return (
        type(str) == type("str") and len(str) == 1 and str[0] >= "a" and str[0] <= "z"
    )


def searchInTheList(arr, value):
    for element in arr:
        if element == value:
            return True
    return False


def isFactorial(value):
    fac = 1
    step = 2
    while fac < value:
        fac *= step
        step += 1

    return value == fac


def isPowerOfTwo(value):
    while value > 1:
        if value % 2 != 0:
            return False
        value /= 2

    return True


def isSuitable(value, features_array):
    if searchInTheList(features_array, "Even") and value % 2 == 1:
        return False
    if searchInTheList(features_array, "Odd") and value % 2 == 0:
        return False
    is_prime = get_primes.is_prime(value)
    if searchInTheList(features_array, "Prime") and not is_prime:
        return False
    if searchInTheList(features_array, "Not Prime") and is_prime:
        return False
    if searchInTheList(features_array, "Factorial") and not isFactorial(value):
        return False
    if searchInTheList(features_array, "Power of 2") and not isPowerOfTwo(value):
        return False
    return True


def searchAmongFactorials(features_array, lower, upper):
    fac = 1
    step = 2
    possible_options = []
    while fac <= 1e18 + 5:
        if fac >= lower and fac <= upper and isSuitable(fac, features_array):
            possible_options.append(fac)
        fac *= step
        step += 1
    return possible_options


def searchAmongPowerOf2(features_array, lower, upper):
    nmber = 1
    possible_options = []
    while nmber <= 1e18 + 5:
        if nmber >= lower and nmber <= upper and isSuitable(nmber, features_array):
            possible_options.append(nmber)
        nmber *= 2

    return possible_options


def searchAmongPrimes(features_array, lower, upper, primes):
    possible_options = []
    for element in primes:
        if element > upper:
            break
        if (
            element >= lower
            and element <= upper
            and isSuitable(element, features_array)
        ):
            possible_options.append(element)
    return possible_options


def searchAmongNonPrimes(features_array, lower, upper, non_primes):
    possible_options = []
    for element in non_primes:
        if element > upper:
            break
        if (
            element >= lower
            and element <= upper
            and isSuitable(element, features_array)
        ):
            possible_options.append(element)
    return possible_options


def create_integer(
    value, isVariableRegistration, variables=None, max_variable_constraint=None
):
    features = value["selectedFeatures"]
    allowed_integers = value["allowedIntegers"]
    sign_properties = value["signProperties"]
    primes, non_primes = get_primes.calculate_primes()
    minnPossibleLowerBound = (int)(1e20)
    maxxPossibleLowerBound = (int)(-1e20)
    try:
        lower_bound = (
            int(value["lowerBound"])
            if not isSymbol(value["lowerBound"])
            else adjustVariableBoundaries.get_variable_boundaries(
                variables, value["lowerBound"]
            )[0]
        )
        upper_bound = (
            int(value["upperBound"])
            if not isSymbol(value["upperBound"])
            else adjustVariableBoundaries.get_variable_boundaries(
                variables, value["upperBound"]
            )[1]
        )
    except Exception as e:
        raise e

    if upper_bound < lower_bound:
        raise Exception("Lower bound larger than upper bound: integer_creation")

    if value["type"] == "variable" and not isVariableRegistration:
        boundary = adjustVariableBoundaries.get_variable_boundaries(
            variables, value["symbol"]
        )
        lower_bound = boundary[0]
        upper_bound = boundary[1]

    if max_variable_constraint != None:
        upper_bound = min(upper_bound, max_variable_constraint)

    if upper_bound < lower_bound:
        raise Exception("Lower bound larger than upper bound: integer_creation")

    is_positive = searchInTheList(sign_properties, "Positive")
    is_negative = searchInTheList(sign_properties, "Negative")
    if upper_bound > 1e6 and (
        searchInTheList(features, "Prime") or searchInTheList(features, "Not Prime")
    ):
        raise Exception(
            "Prime or Not Prime option is not suitable for upperbound>1000000: integer_creation"
        )

    possible_elements = []
    if len(allowed_integers) > 0:
        for element in allowed_integers:
            if element < lower_bound or element > upper_bound:
                continue
            if not isSuitable(element, features):
                continue
            possible_elements.append(element)

        if len(possible_elements) == 0 and not is_negative and not is_positive:
            raise Exception("No possible option!: integer_creation")
        elif not is_positive and not is_positive:
            if isVariableRegistration:
                minnPossibleLowerBound = min(possible_elements)
                maxxPossibleLowerBound = max(possible_elements)
                adjustVariableBoundaries.set_variable(
                    variables,
                    value["symbol"],
                    minnPossibleLowerBound,
                    maxxPossibleLowerBound,
                    not isVariableRegistration,
                )

            return random.choice(possible_elements), possible_elements

    if is_negative:
        upper_bound = min(-1, upper_bound)
    if is_positive:
        lower_bound = max(1, lower_bound)

    if upper_bound < lower_bound:
        raise Exception("Lower bound larger than upper bound: integer_creation")

    if searchInTheList(features, "Factorial"):
        possible_elements.extend(
            searchAmongFactorials(features, lower_bound, upper_bound)
        )
        possible_elements = list(set(possible_elements))  # make list unique
        if len(possible_elements) == 0:
            raise Exception("No possible option!: integer_creation")

        if isVariableRegistration:
            minnPossibleLowerBound = min(possible_elements)
            maxxPossibleLowerBound = max(possible_elements)
            adjustVariableBoundaries.set_variable(
                variables,
                value["symbol"],
                minnPossibleLowerBound,
                maxxPossibleLowerBound,
                not isVariableRegistration,
            )
        return random.choice(possible_elements), possible_elements

    elif searchInTheList(features, "Power of 2"):
        possible_elements.extend(
            searchAmongPowerOf2(features, lower_bound, upper_bound)
        )
        possible_elements = list(set(possible_elements))  # make list unique
        if len(possible_elements) == 0:
            raise Exception("No possible option!: integer_creation")

        if isVariableRegistration:
            minnPossibleLowerBound = min(possible_elements)
            maxxPossibleLowerBound = max(possible_elements)
            adjustVariableBoundaries.set_variable(
                variables,
                value["symbol"],
                minnPossibleLowerBound,
                maxxPossibleLowerBound,
                not isVariableRegistration,
            )
        return random.choice(possible_elements), possible_elements

    elif searchInTheList(features, "Prime"):
        possible_elements.extend(
            searchAmongPrimes(features, lower_bound, upper_bound, primes)
        )

        possible_elements = list(set(possible_elements))  # make list unique
        if len(possible_elements) == 0:
            raise Exception("No possible option!: integer_creation")

        if isVariableRegistration:
            minnPossibleLowerBound = min(possible_elements)
            maxxPossibleLowerBound = max(possible_elements)
            adjustVariableBoundaries.set_variable(
                variables,
                value["symbol"],
                minnPossibleLowerBound,
                maxxPossibleLowerBound,
                not isVariableRegistration,
            )

        return random.choice(possible_elements), possible_elements

    elif searchInTheList(features, "Not Prime"):
        possible_elements.extend(
            searchAmongNonPrimes(features, lower_bound, upper_bound, non_primes)
        )
        possible_elements = list(set(possible_elements))  # make list unique
        if len(possible_elements) == 0:
            raise Exception("No possible option!: integer_creation")

        if isVariableRegistration:
            minnPossibleLowerBound = min(possible_elements)
            maxxPossibleLowerBound = max(possible_elements)
            adjustVariableBoundaries.set_variable(
                variables,
                value["symbol"],
                minnPossibleLowerBound,
                maxxPossibleLowerBound,
                not isVariableRegistration,
            )

        return random.choice(possible_elements), possible_elements

    elif searchInTheList(features, "Odd"):
        total_range = upper_bound - lower_bound + 1
        odd_count = (
            total_range // 2 if abs(lower_bound) % 2 == 0 else total_range // 2 + 1
        )
        random_item_count = odd_count + len(possible_elements)
        if random_item_count == 0:
            raise Exception("No possible option!: integer_creation")

        if isVariableRegistration:
            maxxPossibleLowerBound = (
                upper_bound if abs(upper_bound) % 2 == 1 else upper_bound - 1
            )
            minnPossibleLowerBound = (
                lower_bound if abs(lower_bound) % 2 == 1 else lower_bound + 1
            )
            adjustVariableBoundaries.set_variable(
                variables,
                value["symbol"],
                minnPossibleLowerBound,
                maxxPossibleLowerBound,
                not isVariableRegistration,
            )

        random_number = random.randint(1, random_item_count)
        if random_number <= odd_count:
            starting_number = lower_bound if lower_bound % 2 == 1 else lower_bound + 1
            starting_number += (random_number - 1) * 2
            return starting_number, None
        else:
            random.choice(possible_elements), None

    elif searchInTheList(features, "Even"):
        total_range = upper_bound - lower_bound + 1
        even_count = (
            total_range // 2 if abs(lower_bound) % 2 == 1 else total_range // 2 + 1
        )
        random_item_count = even_count + len(possible_elements)
        if random_item_count == 0:
            raise Exception("No possible option!: integer_creation")

        if isVariableRegistration:
            maxxPossibleLowerBound = (
                upper_bound if abs(upper_bound) % 2 == 0 else upper_bound - 1
            )
            minnPossibleLowerBound = (
                lower_bound if abs(lower_bound) % 2 == 0 else lower_bound + 1
            )
            adjustVariableBoundaries.set_variable(
                variables,
                value["symbol"],
                minnPossibleLowerBound,
                maxxPossibleLowerBound,
                not isVariableRegistration,
            )

        if random_number <= even_count:
            starting_number = (
                lower_bound if abs(lower_bound) % 2 == 0 else lower_bound + 1
            )
            starting_number += (random_number - 1) * 2
            return starting_number, None
        else:
            random.choice(possible_elements), None
    else:
        if isVariableRegistration:
            maxxPossibleLowerBound = upper_bound
            minnPossibleLowerBound = lower_bound
            adjustVariableBoundaries.set_variable(
                variables,
                value["symbol"],
                minnPossibleLowerBound,
                maxxPossibleLowerBound,
                not isVariableRegistration,
            )
        return random.randint(lower_bound, upper_bound), None
