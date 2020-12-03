import os
import json

def get_file_list(dirName):
    listOfFiles = []
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    return listOfFiles

def constructOutputFilenames(main_path, filenames):
    output_file_list = []
    for filename in filenames:
        output_file_list.append(os.path.join(main_path, filename))
    return output_file_list

def saveToJson(dictionary, filepath):
    with open(filepath, 'w') as f:
        json.dump(dictionary, f)

def multipleSaveToJson(l_dictionary, l_filepath):
    files_and_data = zip(l_dictionary, l_filepath)
    for file, data in files_and_data:
        with open(file, 'w') as f:
            json.dump(data, f)
