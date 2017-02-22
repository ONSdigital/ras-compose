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

To run tests go to the features directory which is one step below the current one where this file is contained.
Run the command:

	/> behave collectionInstrument.feature

The system should output something like:


		Feature: Collection Instrument (CI) Status # collectionInstrument.feature:1
		  In order to request CI data the CI micro service
		  must be running and responding to status requests.
		  Scenario: CI Status Running                                         # collectionInstrument.feature:5
		    Given The CI status is active                                     # steps/collectionInstrument.py:30
		    *** The URL to go to is:http://127.0.0.1:8070/status
		    Given The CI status is active                                     # steps/collectionInstrument.py:30 0.011s
		    When A request for status is given                                # steps/collectionInstrument.py:41
		    *** HTT Response code is: 200

		    When A request for status is given                                # steps/collectionInstrument.py:41 0.000s
		    Then The CI micro service returns status information about itself # steps/collectionInstrument.py:47
		    *** Response is:  Collection Instrument service is running
		    Then The CI micro service returns status information about itself # steps/collectionInstrument.py:47 0.000s



# Creating Tests

TODO

# Updating Tests

TODO

# Linking Tests to Stories

Each 'scenario' is mapped to a story within confluence contained within:

	https://digitaleq.atlassian.net/wiki/display/RASB/Epics+and+User+Stories+for+Beta

A user story of SDC01 will map to the feature name with the same number code. e.g. SDC01recoverCredentials.feature




