# Search For Environment Variables

import csv
import grin
import subprocess
import sys

# Gives us the ability to print out some colors to the screen.
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


environment_vars = 'environment_variables.csv'
warningFile = 'usersWarnings.csv'
errorFile = 'usersErrors.csv'
successFile = 'usersSuccess.csv'

# Read a file line by line pulling columns out of the spread sheet and yielding ot the calling function.
'''
    We are expecting a file format of:
    name,                           occurrence ,                    file_names,                 date
    RM_CASE_SERVICE_PORT
    RM_CASE_GET
    PASSWORD_MIN_LENGTH
    
'''
def readfileLineByLine(theFileToRead):
    with open(environment_vars, 'r') as ev:
        reader = csv.reader(ev)
        for row in reader:
            dataElement = []
            dataElement.append(row[0])      # this is the name of the environment variable
            #dataElement.append(row[1])      # this is the occurrences we found from last time
            #dataElement.append(row[2])      # this is a list of the file names that we may have found from last test
            #dataElement.append((row[3]))    # date we found last time we ran the test.
            yield dataElement  # this could be a massive file so lets use 'yield' to save the computer memory


if __name__ == "__main__":

    row_number = 0
    warning_counter = 0
    error_counter = 0
    success_counter = 0
    fileHeader = ['name', 'occurrence', 'file_name', 'date']
    warningData = []
    warningData.append(fileHeader)
    errorData = []
    errorData.append(fileHeader)
    successData = []
    successData.append(fileHeader)

    environment_variables=[]

    print "************************************************************"
    print "****************** Program starting ************************"
    print "************************************************************"
    print "\n\n"

    search_path = sys.argv[1:]

    for num_elements, lineData in enumerate(readfileLineByLine(environment_vars)):

        if num_elements % 100 == 0:
            print "Working...... " + str(num_elements) + " lines processed."

        if num_elements >= 1:
            environment_variables.append(lineData[0])
            print "*** Reading environment Variables: {} ".format(lineData[0])

    #print("Environment variables are: {}".format(environment_variables))

    for env_variable in environment_variables:
        print "{}Searching folders for: {} ....{}".format(bcolors.BOLD, env_variable, bcolors.ENDC)
        if search_path:
            print "{}Trying search path {}: {}".format(bcolors.OKGREEN, search_path[0], bcolors.ENDC)
            subprocess.call(["grin", '-i', env_variable, search_path[0]])
        else:
            print "{}Searching current path{}".format(bcolors.OKBLUE, bcolors.ENDC)
            subprocess.call(["grin", '-i', env_variable])


# Lets write our data to the files now and close up.
# Open our 3 file handlers to record what works and what does not.
with open(errorFile, 'w') as ef:
    errorWriter = csv.writer(ef)
    errorWriter.writerows(errorData)

with open(warningFile, 'w') as wf:
    warningWriter = csv.writer(wf)
    warningWriter.writerows(warningData)

with open(successFile, 'w') as sf:
    successWriter = csv.writer(sf)
    successWriter.writerows(successData)

