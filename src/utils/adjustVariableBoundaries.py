def set_variable(variables, symbol, lower, upper, is_variable_print=False):
    variables.append([symbol, lower, upper, is_variable_print])


def make_variable_value_to_single_value(variables, symbol, value):
    for index in range(len(variables)):
        element = variables[index]
        if element[0] == symbol and element[1] != element[2]:
            variables[index][1] = variables[index][2] = value
            break


def get_variable_boundaries(variables, symbol):
    for element in variables:
        if element[0] == symbol:
            return [element[1], element[2]]

    raise Exception("No such variable!")
