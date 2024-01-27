from creations import (
    integer_creation,
    char_creation,
    double_creation,
    string_creation,
    pair_creation,
)


def selectInTheList(arr, value):
    for element in arr:
        if element == value:
            return True
    return False


def create_instance(type_name, content, variables):
    if type_name == "int":
        created_int, possible_options = integer_creation.create_integer(
            content, False, variables
        )
        return str(created_int)
    elif type_name == "double":
        return str(double_creation.create_double(content, variables))
    elif type_name == "char":
        return str(
            char_creation.create_char(
                content["allowedChars"],
                selectInTheList(content["selectedFeatures"], "Lowercase"),
                selectInTheList(content["selectedFeatures"], "Uppercase"),
                selectInTheList(content["selectedFeatures"], "Digits"),
            ),
        )
    elif type_name == "string":
        return string_creation.create_string(content, variables)

    elif type_name == "pair":
        return pair_creation.create_pair(content, variables)
