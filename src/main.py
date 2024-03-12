from flask import Flask, request, send_file
from flask_cors import CORS
import os
import sys
import uuid
import shutil
import time
import random
import subprocess

sys.path.append("./creations")
from creations import (
    integer_creation,
    double_creation,
    string_creation,
    pair_creation,
    array_creation,
    char_creation,
    graph_creation,
)
from utils import adjustVariableBoundaries

app = Flask(__name__)
CORS(app, methods=["POST", "GET", "DELETE", "PUT"])
app.config["CORS_HEADERS"] = "*"
app.secret_key = os.urandom(24).hex()


@app.route("/downloadFile/<fileName>", methods=["GET"])
def downloaddFile(fileName):
    complete_file_path = "createdZips/" + fileName + "/Test_Data.zip"
    abs_path = os.path.abspath(complete_file_path)

    if not os.path.isfile(abs_path):
        return "File not found", 404
    try:
        return send_file(abs_path, as_attachment=True, mimetype="application/zip")
    except Exception as e:
        return str(e), 500


@app.route("/deleteFile/<fileName>", methods=["DELETE"])
def deleteFile(fileName):
    complete_file_path = "createdZips/" + fileName
    abs_path = os.path.abspath(complete_file_path)
    if os.path.exists(abs_path):
        shutil.rmtree(abs_path)
        return "Successfully deleted", 200
    else:
        return "File not found", 404
    
@app.route("/uploadCode/<userId>", methods=["POST"])
def upload_code(userId):
    if 'codeFile' in request.files:
        code_file = request.files["codeFile"]
        folder_name = "./createdFolders/" + userId
        code_file.save("./createdFolders/"+str(userId)+"/"+code_file.filename)
        files=os.listdir(folder_name)
        compile_string='g++ ' +folder_name+"/"+code_file.filename+' -o ' + 'result'
        os.system(compile_string)
        for file_name in files:
            file_name_without_extension, file_extension = os.path.splitext(os.path.basename(os.path.abspath(file_name)))
            if(file_extension==".out"):
                continue
            if(file_extension==".cpp"):
                continue
            new_name = file_name_without_extension + ".out"
            new_path="input.txt"
            #print(userId+" Path: "+new_path)
            shutil.copy(folder_name+"/"+file_name,new_path)
            #burada kodu derle ve calistir outa yazilan seyi de yeni isme kaydet. sonra dosyalari zipe at sonra sil!...
            run_string='./result'
            os.system(run_string)
            shutil.copy("output.txt",folder_name+"/"+new_name)
            
        #print(code_file.filename + " user id: " + userId)
        for file_name in files:
            file_name_without_extension, file_extension = os.path.splitext(os.path.basename(os.path.abspath(file_name)))
            if(file_extension==".cpp"):
                os.remove(folder_name+"/"+file_name)
                break
        os.remove("input.txt");
        os.remove("output.txt");
        os.remove("result");
        zip_filename = "Test_Data"
        zip_folder_name = "createdZips/" + userId
        if not os.path.exists(zip_folder_name):
            os.makedirs(zip_folder_name)

        full_zip_path = zip_folder_name + "/" + zip_filename
        shutil.make_archive(full_zip_path, "zip", "createdFolders/" + userId)

        if os.path.exists("createdFolders/" + userId):
            shutil.rmtree("createdFolders/" + userId)
        return userId, 200
    
    return "Code is not uploaded", 400


@app.route("/createFile", methods=["POST"])
def create_file():
    client_start_time = time.time()
    client_max_time = 10  # 10 secs

    complete_packet = request.json
    file_part = complete_packet["filePart"]
    testcase_part = complete_packet["testcasePart"]
    content = testcase_part["content"]
    content_len = len(content)
    all_variables = testcase_part["allVariables"]
    constrained_variables = testcase_part["constrainedVariables"]
    file_amount = int(file_part["amount"])
    file_name = file_part["name"]
    file_extension = file_part["extension"]
    file_numbering = file_part["numbering"]

    result_string = ""

    variables = []
    is_line_finished = True

    user_specific_id = str(uuid.uuid4())
    folder_name = "createdFolders/" + user_specific_id
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    try:
        for file_index in range(file_amount):
            testcase_amount = random.randint(
                int(testcase_part["testcaseAmount"][0]),
                int(testcase_part["testcaseAmount"][1]),
            )
            result_string = str(testcase_amount) + "\n"
            is_line_finished = True

            variable_usage_dict = {}
            for element in constrained_variables:
                variable_usage_dict[element["symbol"]] = 0

            for index in range(testcase_amount):
                if time.time() - client_start_time > client_max_time:
                    clear_folders(folder_name)
                    return "Your allowed time limit is finished", 404

                variables = []
                for element in all_variables:
                    integer_creation.create_integer(element, True, variables)
                content_index = 0
                for element in content:
                    content_index += 1
                    if element["type"] == "int" or element["type"] == "variable":
                        max_variable_constraint = None
                        if (
                            element["type"] == "variable"
                            and total_value_of_constraint(
                                constrained_variables, element["symbol"]
                            )
                            != -1
                        ):
                            total_available_sum = total_value_of_constraint(
                                constrained_variables, element["symbol"]
                            )
                            min_variable_value = int(element["lowerBound"])
                            remaining_testcase_count = testcase_amount - index - 1
                            max_variable_constraint = (
                                total_available_sum
                                - variable_usage_dict[element["symbol"]]
                                - remaining_testcase_count * min_variable_value
                            )

                        value, possible_options = integer_creation.create_integer(
                            element, False, variables, max_variable_constraint
                        )
                        if element["type"] == "variable":
                            adjustVariableBoundaries.make_variable_value_to_single_value(
                                variables, element["symbol"], value
                            )
                            if (
                                total_value_of_constraint(
                                    constrained_variables, element["symbol"]
                                )
                                != -1
                            ):
                                variable_usage_dict[element["symbol"]] += value

                        if not is_line_finished:
                            result_string += " "
                        result_string += str(value)
                        is_line_finished = False

                    elif element["type"] == "double":
                        value = double_creation.create_double(element, variables)
                        if not is_line_finished:
                            result_string += " "
                        result_string += str(value)
                        is_line_finished = False

                    elif element["type"] == "string":
                        value = string_creation.create_string(element, variables)
                        if not is_line_finished:
                            result_string += " "
                        result_string += str(value)
                        is_line_finished = False

                    elif element["type"] == "pair":
                        value = pair_creation.create_pair(element, variables)
                        if not is_line_finished:
                            result_string += " "
                        result_string += str(value)
                        is_line_finished = False
                    elif element["type"] == "char":
                        value = char_creation.create_char(value=element)
                        if not is_line_finished:
                            result_string += " "
                        result_string += str(value)
                        is_line_finished = False

                    elif element["type"] == "array":
                        value = array_creation.create_array(element, variables)
                        if not is_line_finished:
                            result_string += "\n"
                        result_string += str(value)
                        if content_index != content_len:
                            result_string += "\n"
                        is_line_finished = True

                    elif element["type"] == "graph" or element["type"] == "tree":
                        value = graph_creation.create_graph(element, variables)
                        if not is_line_finished:
                            result_string += "\n"
                        result_string += str(value)
                        if content_index != content_len:
                            result_string += "\n"
                        is_line_finished = True

                    elif element["type"] == "newLine":
                        result_string += "\n"
                        is_line_finished = True

                if index < testcase_amount - 1:
                    result_string += "\n"
                    is_line_finished = True

            created_file_name = get_filename(
                file_name, file_numbering, file_extension, file_index
            )
            file_path = os.path.join(folder_name, created_file_name)
            with open(file_path, "w+") as file:
                file.write(result_string)

    except Exception as e:
        print("Error: ", e)
        clear_folders(folder_name)
        return "Input creation or file creation error:  " + str(e), 404

    #try:
        #zip_filename = "Inputs"
        #zip_folder_name = "createdZips/" + user_specific_id
        #if not os.path.exists(zip_folder_name):
        #    os.makedirs(zip_folder_name)

        #full_zip_path = zip_folder_name + "/" + zip_filename
        #shutil.make_archive(full_zip_path, "zip", "createdFolders/" + user_specific_id)

        #if os.path.exists("createdFolders/" + user_specific_id):
        #    shutil.rmtree("createdFolders/" + user_specific_id)

    #except Exception as e:
    #    print("File zipping error: ", e)
    #    if os.path.exists("createdFolders/" + user_specific_id):
    #        shutil.rmtree("createdFolders/" + user_specific_id)
    #    return "File zipping error: " + str(e), 404

    return user_specific_id, 200


def total_value_of_constraint(constraints_list, symbol):
    for element in constraints_list:
        if element["symbol"] == symbol:
            return element["sumValue"]

    return -1


def clear_folders(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)


def get_filename(file_name, file_numbering, file_extension, file_index):
    number_code = ""
    if file_numbering == "0":
        number_code = str(file_index)
    elif file_numbering == "1":
        number_code = str(file_index + 1)
    elif file_numbering == "00":
        if file_index <= 9:
            number_code = "0" + str(file_index)
        else:
            number_code = str(file_index)
    elif file_numbering == "01":
        if file_index + 1 <= 9:
            number_code = "0" + str(file_index + 1)
        else:
            number_code = str(file_index + 1)

    return file_name + number_code + "." + file_extension


if __name__ == "__main__":
    app.run(debug=True)
