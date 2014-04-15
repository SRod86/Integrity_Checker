#variable to hold status of user (whether they are done or not)
working = 1

#while the user is not done, continue running the program
while working == 1:
    print("Please input a command. For help type 'help'. To exit type 'exit'")

    #grab input from user, divide it into words, and grab the command/option/argument
    request = input()
    command = request.split()
    option = request.split()
    argument = request.split()
    #command = request[0]
    #option = request[1]
    #argument = request[2]

    #if user inputs command 'icheck'...
    if command == ['icheck']:
        if option == ['-l']:
            pass
        elif option == ['-f']:
            readFile = open(argument, "r")
            contents = readFile.read()
            print(contents)
        elif option == ['-t']:
            pass
        elif option == ['u']:
            pass
        elif option == ['-r']:
            pass

    #if user inputs command 'help'...
    elif command == ['help']:
        #display help screen
        print("Integrity Checker has a few options you can use. Each option "
              "must begin with the command 'icheck'. The options are as follows:")
        print("\t-l <directory>: Reads the list of files in the directory and computes the md5 for each one")
        print("\t-f <file>: Reads a specific file and computes its md5")
        print("\t-t: Tests integrity of the files with recorded md5s")
        print("\t-u <file>: Update a file that you have modified after its integrity has been checked")
        print("\t-r <file>: Removes a file from the recorded md5s\n")

    #if user inputs command 'exit'
    elif command == ['exit']:
        #set working to zero and exit program loop
        working = 0

    #if anything other than 'icheck', 'help', and 'exit' are input...
    else:
        #display error message and start over
        print("I'm sorry that is not a valid command.\n")