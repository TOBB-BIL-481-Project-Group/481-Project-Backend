from utils import create_small_types


def selectInTheList(arr, value):
    for element in arr:
        if element == value:
            return True
    return False


def create_pair(value, variables=None):
    first_content = value["firstContent"]
    second_content = value["secondContent"]
    features = value["features"]
    try:
        first_instance = create_small_types.create_instance(
            first_content["type"], first_content, variables
        )
        second_instance = create_small_types.create_instance(
            second_content["type"], second_content, variables
        )
        if selectInTheList(features, "1st=2nd"):
            return first_instance + " " + first_instance
        elif selectInTheList(features, "1st<2nd"):
            if first_instance < second_instance:
                return first_instance + " " + second_instance
            else:
                return second_instance + " " + first_instance
        elif selectInTheList(features, "1st>2nd"):
            if first_instance < second_instance:
                return second_instance + " " + first_instance
            else:
                return first_instance + " " + second_instance
        else:
            return first_instance + " " + second_instance

    except Exception as e:
        raise e
