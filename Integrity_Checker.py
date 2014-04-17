import hashlib
import json
import os
import ntpath


def read_the_file(f_location):
    read_file = open(f_location, "r")
    c = read_file.read().encode('utf-8')
    read_file.close()
    return c


def scan_and_hash(directory_content):
    for f in directory_content:
        location = argument + "/" + f
        content = read_the_file(location)
        comp_hash = create_hash(content)
        json_obj = {"Directory": argument, "Contents": {"filename": str(f),
                                                        "original string": str(content), "md5": str(comp_hash)}}
        location = location.replace(argument, "")
        location = location.replace(".txt", "")
        write_to_json(location, json_obj)


def create_hash(content):
    key_before = "reallyBad".encode('utf-8')
    key_after = "hashKeyAlgorithm".encode('utf-8')
    h.update(key_before)
    h.update(content)
    h.update(key_after)
    return h.hexdigest()


def write_to_json(arg, json_obj):
    arg = arg.replace(".txt", "")
    storage_location = "recorded/" + str(arg) + ".json"
    write_file = open(storage_location, "w")
    json.dump(json_obj, write_file, indent=4, sort_keys=True)
    write_file.close()

#variable to hold status of user (whether they are done or not)
working = 1
#while the user is not done, continue running the program
while working == 1:
    h = hashlib.md5()
    print("Please input a command. For help type 'help'. To exit type 'exit'")

    #grab input from user, divide it into words, and grab the command/option/argument
    request = input()
    request = request.split()

    if len(request) == 1:
        command = request[0]
    elif len(request) == 2:
        command = request[0]
        option = request[1]
    elif len(request) == 3:
        command = request[0]
        option = request[1]
        argument = request[2]
    else:
        print("I'm sorry that is not a valid request.\n")
        continue

    #if user inputs command 'icheck'...
    if command == 'icheck':
        if option == '-l':
            if argument == "":
                print("For option -l, please input a directory name.")
                continue

            try:
                dirContents = os.listdir(argument)
                scan_and_hash(dirContents)

            except OSError:
                print("Directory not found. Make sure the directory name is correct or try a different directory.")

        elif option == '-f':
            if argument == "":
                print("For option -f, please input a file name.")
                continue

            try:
                contents = read_the_file(argument)
                computedHash = create_hash(contents)
                jsonObj = {"filename": str(argument), "original string": str(contents), "md5": str(computedHash)}
                write_to_json(argument, jsonObj)
            except OSError:
                print("File not found. Make sure the file name is correct or try a different file.")

        elif option == '-t':
            try:
                dirContents = os.listdir("recorded")
                for file in dirContents:
                    fileLocation = "recorded" + "/" + file
                    readJson = open(fileLocation, "r")
                    jsonObj = json.load(readJson)
                    readJson.close()
                    file.replace(".json", ".txt")
                    fileLocation = "recorded" + "/" + file
                    readFile = open(fileLocation, "r")
                    contents = readFile.read().encode('utf-8')
                    readFile.close()
                    print(jsonObj)
                    print(contents)
                    #h.update(contents)
                    #computedHash = h.digest()
                    #print(computedHash)
                    #print(jsonObj['contents']['md5'])
            except OSError:
                print("File not found. Make sure the file name is correct or try a different file.")

        elif option == '-u':
            print("gonna update stuff")
        elif option == '-r':
            print("gonna remove stuff")

    #if user inputs command 'help'...
    elif command == 'help':
        #display help screen
        print("Integrity Checker has a few options you can use. Each option "
              "must begin with the command 'icheck'. The options are as follows:")
        print("\t-l <directory>: Reads the list of files in the directory and computes the md5 for each one")
        print("\t-f <file>: Reads a specific file and computes its md5")
        print("\t-t: Tests integrity of the files with recorded md5s")
        print("\t-u <file>: Update a file that you have modified after its integrity has been checked")
        print("\t-r <file>: Removes a file from the recorded md5s\n")

    #if user inputs command 'exit'
    elif command == 'exit':
        #set working to zero and exit program loop
        working = 0

    #if anything other than 'icheck', 'help', and 'exit' are input...
    else:
        #display error message and start over
        print("I'm sorry that is not a valid command.\n")