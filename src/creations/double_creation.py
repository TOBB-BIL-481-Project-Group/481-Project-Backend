import random
from utils import adjustVariableBoundaries


def isSymbol(str):
    return (
        type(str) == type("str") and len(str) == 1 and str[0] >= "a" and str[0] <= "z"
    )


def create_double(value, variables=None):
    left_limit = value["leftLimit"]
    right_limit = value["rightLimit"]
    is_fixed_precision = value["isPrecision"]
    precision_amount = int(value["precisionAmount"]) if is_fixed_precision else 0

    try:
        left_limit = (
            float(left_limit)
            if not isSymbol(left_limit)
            else adjustVariableBoundaries.get_variable_boundaries(
                variables, left_limit
            )[0]
        )
        right_limit = (
            float(right_limit)
            if not isSymbol(right_limit)
            else adjustVariableBoundaries.get_variable_boundaries(
                variables, right_limit
            )[1]
        )
    except Exception as e:
        raise e

    if right_limit < left_limit:
        raise Exception("Lower bound larger than upper bound: double_creation")

    random_double = random.uniform(left_limit, right_limit)
    if is_fixed_precision:
        random_double = round(random_double, precision_amount)
        random_double = "{:.{}f}".format(random_double, precision_amount)
        if precision_amount == 0:
            temp = int(random_double)
            random_double = temp

    return random_double
