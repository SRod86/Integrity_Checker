import hashlib
import json
import os
import fnmatch
import sys
from codecs import open


def check_mhash():
    d_contents = os.listdir("recorded")
    text_mhash = "checkMaster.txt"
    flush_file = open(text_mhash, "w")
    flush_file.write("")
    flush_file.close()
    write_file = open(text_mhash, "a")
    for f in d_contents:
        if f == "mHash.json":
            continue
        json_obj = read_the_json(f)
        md5 = json_obj['Contents']['md5']
        write_file.write(md5)

    write_file.close()
    content = read_the_file(text_mhash)
    comp_hash = create_hash(content)
    json_mhash = text_mhash.replace(".txt", ".json")
    json_obj = read_the_json("mHash.json")
    if json_obj['Contents']['md5'] == comp_hash:
        print("Master Hash verified")
        integrity = create_hash("success")
        json_obj["integrity"] = integrity
        write_to_json(json_mhash, json_obj)
    else:
        print("Master Hash could not be verified.")


def master_hash():
    d_contents = os.listdir("recorded")
    text_mhash = "mHash.txt"
    flush_file = open(text_mhash, "w")
    flush_file.write("")
    flush_file.close()
    write_file = open(text_mhash, "a")
    for f in d_contents:
        if f == "mHash.json":
            continue
        json_obj = read_the_json(f)
        md5 = json_obj['Contents']['md5']
        write_file.write(md5)

    write_file.close()
    content = read_the_file(text_mhash)
    comp_hash = create_hash(content)
    json_obj = {"Directory": "recorded", "Contents": {"filename": text_mhash,
                                                      "original string": str(content), "md5": str(comp_hash)}}
    write_to_json(text_mhash, json_obj)


#opens the file, reads/encodes it, and returns the contents (c)
def read_the_file(f_location):
    with open(f_location, 'r', encoding="utf-8") as f:
        c = f.read()

    f.close()
    return c


def scan_hash_json(directory_content, arg):
    for f in directory_content:
        location = arg + "/" + f
        content = read_the_file(location)
        comp_hash = create_hash(content)
        json_obj = {"Directory": arg, "Contents": {"filename": str(f),
                                                   "original string": str(content), "md5": str(comp_hash)}}
        location = location.replace(arg, "")
        write_to_json(location, json_obj)


#scans the file, creates the hash, and writes it to a json file
def read_the_json(f):
    if "recorded" not in f:
        f_location = "recorded" + "/" + f
        read_json = open(f_location, "r")
    else:
        read_json = open(f, "r")

    json_obj = json.load(read_json)
    read_json.close()
    return json_obj


def display_record_integrity(comp_hash, json_obj, file, opt):
    #if the hashes match...
    if json_obj['Contents']['md5'] == comp_hash:
        print(file + ": File has not been modified.")
        integrity = create_hash("success")
        json_obj["integrity"] = integrity
        write_to_json(file, json_obj)
    else:
        print(file + ": File was modified.")
        if opt == "-u":
            content = read_the_file(file)
            comp_hash = create_hash(content)
            integrity = create_hash("userModified")
            json_obj = {"Directory": "Default", "Contents": {
                "filename": str(file), "original string": str(content), "md5": str(comp_hash)},
                "integrity": integrity}
            write_to_json(file, json_obj)
            print("Json file has been updated.")
        elif opt == "-t":
            integrity = create_hash("failure")
            json_obj["integrity"] = integrity
            write_to_json(file, json_obj)
        elif opt == "-s":
            user_change = input("Did you modify the file? (y/n) ")
            if user_change.lower() == "n":
                sys.exit("MD5s did not match.")
            elif user_change.lower() == "y":
                text = file.replace(".json", ".txt")
                content = read_the_file(text)
                comp_hash = create_hash(content)
                integrity = create_hash("userModified")
                json_obj = {"Directory": "Default", "Contents": {
                    "filename": str(file), "original string": str(content), "md5": str(comp_hash)},
                    "integrity": integrity}
                print(argument)
                write_to_json(file, json_obj)
                print("Json file has been updated.")
            else:
                print("Invalid option. No action taken.")


#check integrity of the file
def check_integrity(d_content, opt, arg):
    if opt == "-u":
        f_content = read_the_file(arg)
        to_json = arg.replace(".txt", ".json")
        result = find(to_json, os.getcwd())
        json_obj = read_the_json(result)
        comp_hash = create_hash(f_content)
        display_record_integrity(comp_hash, json_obj, arg, opt)

    elif opt == "-t" or opt == "-s":
        #d_content = directory content
        for f in d_content:
            if f == "mHash.json":
                continue
            json_obj = read_the_json(f)
            text = f.replace(".json", ".txt")
            result = find(text, os.getcwd())
            content = read_the_file(result)
            comp_hash = create_hash(content)
            display_record_integrity(comp_hash, json_obj, f, opt)
        check_mhash()


#find the file being searched for
def find(pattern, path):
    result = ""
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result = os.path.join(root, name)
                #if the result is a .json file, start the loop over
                if '.txt' in pattern and 'recorded' in result or '.json' in pattern and '.txt' in result:
                    continue

    return result


#create a hash for the file contents being passed in
def create_hash(content):
    h = hashlib.md5()
    key_before = "reallyBad".encode('utf-8')
    key_after = "hashKeyAlgorithm".encode('utf-8')
    content = content.encode('utf-8')
    h.update(key_before)
    h.update(content)
    h.update(key_after)
    return h.hexdigest()


#write the MD5 hash to the json file within "recorded" directory
def write_to_json(arg, json_obj):
    if ".txt" in arg:
        arg = arg.replace(".txt", ".json")
    if "recorded" not in arg:
        storage_location = "recorded/" + str(arg)
    else:
        storage_location = str(arg)
    write_file = open(storage_location, "w")
    json.dump(json_obj, write_file, indent=4, sort_keys=True)
    write_file.close()


#variable to hold status of user (whether they are done or not)
working = 1
#while the user is not done, continue running the program
while working == 1:
    print("Please input a command. For help type 'help'. To exit type 'exit'")

    #grab input from user, divide it into words, and grab the command/option/argument
    request = input()
    request = request.split()

    if len(request) == 1:
        command = request[0]
        option = ""
        argument = ""
    elif len(request) == 2:
        command = request[0]
        option = request[1]
        argument = ""
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
                scan_hash_json(dirContents, argument)
                master_hash()

            except OSError:
                print("Directory not found. Make sure the directory name is correct or try a different directory.")

        elif option == '-f':
            if argument == "":
                print("For option -f, please input a file name.")
                continue

            try:
                contents = read_the_file(argument)
                computedHash = create_hash(contents)
                jsonObj = {"Directory": "Default", "Contents": {
                    "filename": str(argument), "original string": str(contents), "md5": str(computedHash)}}
                write_to_json(argument, jsonObj)
                master_hash()
            except OSError:
                print("File not found. Make sure the file name is correct or try a different file.")

        elif option == '-t':
            dirContents = os.listdir("recorded")
            check_integrity(dirContents, option, "none")

        elif option == '-u':
            if argument == "":
                print("For option -u, please input a file name.")
                continue
            if ".txt" not in argument:
                print("Please make sure you input the correct file name and/or full file path.")
                continue

            check_integrity("none", option, argument)

            try:
                contents = read_the_file(argument)
                computedHash = create_hash(contents)
                jsonObj = {"Directory": "Default", "Contents": {
                    "filename": str(argument), "original string": str(contents), "md5": str(computedHash)}}
                write_to_json(argument, jsonObj)
                master_hash()
            except OSError:
                print("File not found. Make sure the file name is correct or try a different file.")

        elif option == '-s':
            dirContents = os.listdir("recorded")
            check_integrity(dirContents, option, "none")

        elif option == '-r':
            if argument == "":
                print("For option -r, please input a file name.")
                continue

            try:
                if ".json" in argument:
                    if "recorded" not in argument:
                        argument = "recorded/" + argument
                    os.remove(argument)
                    master_hash()
                else:
                    print("Invalid file type. Can not remove MD5 record.")
            except OSError:
                print("File not found. Make sure the file name is correct or try a different file.")

    #if user inputs command 'help'...
    elif command == 'help':
        #display help screen
        print("Integrity Checker has a few options you can use. Each option "
              "must begin with the command 'icheck'. The options are as follows:")
        print("\t-l <directory>: Reads the list of files in the directory and computes the MD5 for each one")
        print("\t-f <file>: Reads a specific file and computes its MD5")
        print("\t-t: Tests integrity of the files with recorded MD5s")
        print("\t-u <file>: Update a file that you have modified after its integrity has been checked")
        print("\t-s: Scan all files with recorded MD5s. If a difference is found, "
              "user is asked if they made the change")
        print("\t-r <file>: Removes the .json file from the recorded MD5s\n")

    #if user inputs command 'exit'
    elif command == 'exit':
        #set working to zero and exit program loop
        working = 0

    #if anything other than 'icheck', 'help', and 'exit' are input...
    else:
        #display error message and start over
        print("I'm sorry that is not a valid command.\n")