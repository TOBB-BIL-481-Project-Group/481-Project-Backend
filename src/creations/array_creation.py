from utils import create_small_types
from creations import integer_creation, string_creation
import random
from utils import adjustVariableBoundaries
import copy


def isSymbol(str):
    return (
        type(str) == type("str") and len(str) == 1 and str[0] >= "a" and str[0] <= "z"
    )


def searchInTheList(arr, value):
    for element in arr:
        if element == value:
            return True

    return False


def create_array(value, variables):
    dimension = value["dimension"]
    size = copy.deepcopy(value["size"])
    content = value["contentFormat"]
    features = value["features"]
    max_array_size = 1000000
    size_array = []
    if len(size) == 1:
        if isSymbol(size[0]):
            boundary = adjustVariableBoundaries.get_variable_boundaries(
                variables, size[0]
            )
            if boundary[0] != boundary[1]:
                raise Exception(
                    "Array length variable should be prewritten: array_creation"
                )
            size[0] = int(boundary[0])
        else:
            size[0] = int(size[0])

        if int(size[0]) > max_array_size:
            raise Exception("Length is greater than 1e6: array_creation")
        if int(size[0]) <= 0:
            raise Exception("Length should be positive: array_creation")
        size_array = [int(size[0])]

        if searchInTheList(features, "Permutation"):
            temp_numbers = list(range(1, size[0] + 1))
            perm = random.sample(temp_numbers, size[0])
            result_string = ""
            for i in range(size[0]):
                result_string += str(perm[i])
                if i < size[0] - 1:
                    result_string += " "

            return result_string

    else:
        if isSymbol(size[0]):
            boundary = adjustVariableBoundaries.get_variable_boundaries(
                variables, size[0]
            )
            if boundary[0] != boundary[1]:
                raise Exception(
                    "Array length variable should be prewritten: array_creation"
                )
            else:
                size[0] = int(boundary[0])

        if isSymbol(size[1]):
            boundary = adjustVariableBoundaries.get_variable_boundaries(
                variables, size[1]
            )
            if boundary[0] != boundary[1]:
                raise Exception(
                    "Array length variable should be prewritten: array_creation"
                )
            else:
                size[1] = int(boundary[0])

        if int(size[0]) * int(size[1]) > max_array_size:
            raise Exception("Length is greater than 1e6: array_creation")
        if int(size[0]) <= 0 or int(size[1]) <= 0:
            raise Exception("Length should be positive: array_creation")

        size_array = [int(size[0]), int(size[1])]

    result_string = ""
    int_possible_elements = None
    string_length = 0
    is_single_element = searchInTheList(features, "Single Element")
    is_unique_element = searchInTheList(features, "Unique Elements")
    if dimension == "1-D":
        length = size_array[0]
        set_elements = set()
        whole_elements = list()
        try:
            for i in range(5000000):
                if not is_unique_element and i == length:
                    break
                if is_unique_element and len(set_elements) == length:
                    break
                if (
                    content["type"] != "int"
                    and content["type"] != "string"
                    and (not (is_single_element and i > 0))
                ):
                    instance = create_small_types.create_instance(
                        content["type"], content, variables
                    )
                elif content["type"] == "string" and (
                    not (is_single_element and i > 0)
                ):
                    remaining_string = length - (i + 1)
                    instance = string_creation.create_string(
                        content,
                        variables,
                        max_array_size - string_length - remaining_string,
                    )
                    string_length += len(instance)
                elif not (is_single_element and i > 0):
                    if int_possible_elements != None:
                        instance = random.choice(int_possible_elements)
                    else:
                        (
                            instance,
                            int_possible_elements,
                        ) = integer_creation.create_integer(content, False, variables)

                if is_unique_element:
                    set_elements.add(instance)
                    if len(set_elements) == length:
                        break

                whole_elements.append(instance)

            if is_unique_element and len(set_elements) != length:
                raise Exception(
                    "Iteration count is exceeded for unique value creation: array_creation"
                )

        except Exception as e:
            raise e

        result_string = ""
        if is_unique_element:
            whole_elements = list(set_elements)
        if searchInTheList(features, "Sorted (Ascending)"):
            whole_elements.sort()
        elif searchInTheList(features, "Sorted (Descending)"):
            whole_elements.sort(reverse=True)

        for i in range(length):
            result_string += str(whole_elements[i])
            if (
                i < length - 1
                and content["type"] != "pair"
                and content["type"] != "char"
            ):
                result_string += " "
            if i < length - 1 and content["type"] == "pair":
                result_string += "\n"

        return result_string

    else:
        row = size_array[0]
        col = size_array[1]
        length = row * col
        set_elements = set()
        max_try_count = 5000000

        try:
            for i in range(5000000 if is_unique_element else row):
                if is_unique_element and (
                    max_try_count < 0 or len(set_elements) == length
                ):
                    break
                for j in range(col):
                    if is_unique_element:
                        max_try_count -= 1
                        if max_try_count < 0:
                            break
                    if (
                        content["type"] != "int"
                        and content["type"] != "string"
                        and (not (is_single_element and i > 0))
                    ):
                        instance = create_small_types.create_instance(
                            content["type"], content, variables
                        )
                    elif content["type"] == "string" and (
                        not (is_single_element and i > 0)
                    ):
                        remaining_string = row * col - (col * i + j)
                        instance = string_creation.create_string(
                            content,
                            variables,
                            max_array_size - string_length - remaining_string,
                        )
                        string_length += len(instance)
                    elif not (is_single_element and i > 0):
                        if int_possible_elements != None:
                            instance = random.choice(int_possible_elements)
                        else:
                            (
                                instance,
                                int_possible_elements,
                            ) = integer_creation.create_integer(
                                content, False, variables
                            )

                    result_string += str(instance)
                    if j < col - 1 and content["type"] != "char":
                        result_string += " "

                    if is_unique_element:
                        set_elements.add(str(instance))
                        if len(set_elements) == length:
                            break

                if i < row - 1:
                    result_string += "\n"

            if is_unique_element and len(set_elements) < length:
                raise Exception(
                    "Iteration count is exceeded for unique value creation: array_creation"
                )

        except Exception as e:
            raise e

        if is_unique_element:
            result_string = ""
            set_list = list(set_elements)
            col_index = 0
            for i in range(length):
                result_string += set_list[i]
                if col_index < col - 1 and content["type"] != "char":
                    result_string += " "
                col_index = (col_index + 1) % col
                if i < length - 1 and col_index == 0:
                    result_string += "\n"

        return result_string
