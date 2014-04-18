Integrity Checker is a school assignment. It is written in Python using Pycharm and\n
is a console based program. There are a few options you can use. Each option must \n
begin with the command 'icheck'. The options are as follows:\n
	\t-l <directory>: Reads the list of files in the directory and computes the MD5 for each one
        \t-f <file>: Reads a specific file and computes its MD5
        \t-t: Tests integrity of the files with recorded MD5s
        \t-u <file>: Update a file that you have modified after its integrity has been checked
        \t-s: Scan all files with recorded MD5s. If a difference is found,
              user is asked if they made the change
        \t-r <file>: Removes the .json file from the recorded MD5s
