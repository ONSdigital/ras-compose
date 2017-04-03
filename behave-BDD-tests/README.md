# BDD Test Cases

This guide describes what to install and how to run the test cases for ONS RAS.


# Installation

The test cases contained within this directory are written using the Python Behave library. You can find details on
this at [python behave here.]( http://pythonhosted.org/behave/)
To setup your system go to the route folder of the ras-compose repo. You should find see a file called requirements.txt.
This contains a list of all required packages used within python tool/programs in ras-compose. From this directory
and within your virtual environment do:

	/> pip install -r requirements.txt

This will install all packages required. You can check this by typing the command 'behave' at the command line. The
system should say 'No steps in directory'.

# Running Tests

To run all tests, go to the `behave-BDD-tests` directory and run the command:

	/> behave

The system should output something like:
    
    ...
    
    Feature: Handle retrieval of Collection Instrument data # features/get_collection_instrument.feature:1
    
      @connect_to_database
      Scenario: Get all available collection instrument data              # features/get_collection_instrument.feature:7
        Given one or more collection instruments exist                    # features/steps/steps.py:77 0.002s
        When a request is made for one or more collection instrument data # features/steps/steps.py:151 185.385s
        Then check the returned data are correct                          # features/steps/steps.py:226 0.169s
        And the response status code is 200                               # features/steps/steps.py:209 0.000s
    
    ...

You can optionally run individual features by running:

    /> behave <http_method_name>_collection_instrument.feature

# Creating Tests

TODO

# Updating Tests

TODO

# Linking Tests to Stories

Each 'scenario' is mapped to a story within confluence contained within:

	https://digitaleq.atlassian.net/wiki/display/RASB/Epics+and+User+Stories+for+Beta

A user story of SDC01 will map to the feature name with the same number code. e.g. SDC01recoverCredentials.feature




