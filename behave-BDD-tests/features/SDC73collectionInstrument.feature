Feature: Collection Instrument (CI) Status
  In order to request CI data the CI micro service
  must be running and responding to status requests.


# Not currently working. Is '/status' an endpoint now?
#  Scenario: CI Status Running
#    Given The CI status is active
#     When A request for status is given
#     Then The CI micro service returns status information about itself




  
# ----------------------------------------------------------------------------------------------------------------------
# Collection Instrument ID Tests
# ----------------------------------------------------------------------------------------------------------------------  
  
# GET (/collectioninstrument/id/{id}) Tests all possible API values for this endpoint. Tests are written in the style of:
# 1) Sunny day
# 2) invalid values
# 3) boundary case
# 4) exercising options/logic if any
# 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API

# 1) GET (/collectioninstrument/id/{id} using a valid ID
  Scenario: Obtain Collection Instrument data by ID
    Given a valid collection instrument ID
    When a request is made for the collection instrument data by ID
    Then check the returned data by collection instrument ID is correct


# 2.1) GET (/collectioninstrument/id/{id} using an ID with the wrong path e.g. ONS.GOV.US
  Scenario: Collection Instrument ID domain name is incorrect
    Given a collection instrument ID with an incorrect domain name
    When a request is made for the collection instrument using the ID with the incorrect domain name
    Then information is returned saying the ID with the incorrect domain name is invalid


# 2.2) GET (/collectioninstrument/id/{id} using an ID with the wrong number value e.g. ONS.GOV.UK.CI.00000000.0
  # TODO: Unsure what this 'number' portion of the ID is called? This should be changed to something more meaningful in here and in steps.py
  Scenario: Collection Instrument ID number value is incorrect
    Given a collection instrument ID with an incorrect number
    When a request is made for the collection instrument using the ID with the incorrect number
    Then information is returned saying the ID with the incorrect number is invalid


# 2.3) GET (/collectioninstrument/id/{id} using an ID with the wrong TYPE value e.g. ONS.GOV.UK.XX.000.000.00000
  Scenario: Collection Instrument ID type is incorrect
    Given a collection instrument ID with an incorrect type name
    When a request is made for the collection instrument using the ID with the incorrect type name
    Then information is returned saying the ID with the incorrect type name is invalid


# 3.1) GET (/collectioninstrument/id/{id} using an ID with a valid boundary case value e.g. ONS.GOV.UK.CI.000.000.00000 which is OK
  Scenario: Collection Instrument ID with the lowest boundary is not found
    Given a collection instrument ID with the lowest boundary that does not exist
    When a request is made for the collection instrument using the ID with the lowest boundary
    Then information is returned saying the ID with the lowest boundary is not found


# 3.2) GET (/collectioninstrument/id/{id} using an ID with a valid boundary case value e.g. ONS.GOV.UK.XX.999.999.99999 which is OK
  Scenario: Collection Instrument ID with the highest boundary is not found
    Given a collection instrument ID with the highest boundary that does not exist
    When a request is made for the collection instrument using the ID with the highest boundary
    Then information is returned saying the ID with the highest boundary is not found

@wip
#  Currently, this test fails due to length validation. Should it fail for negative numbers?
# 3.3) GET (/collectioninstrument/id/{id} using an ID with a boundary case value that is too small e.g. ONS.GOV.UK.XX.-100.-100.-10000 which is too small
  Scenario: Collection Instrument ID number value too low
    Given a collection instrument ID with a number value too low
    When a request is made for the collection instrument using the ID with the number value too low
    Then information is returned saying the ID with the number value too low is invalid


# 3.4) GET (/collectioninstrument/id/{id} using an ID with a boundary case value that is too high e.g. ONS.GOV.UK.XX.9999.9999.999999 which is too big
    Scenario: Collection Instrument ID number value too high
    Given a collection instrument ID with a number value too high
    When a request is made for the collection instrument using the ID with the number value too high
    Then information is returned saying the ID with the number value too high is invalid


# 4.1) GET (/collectioninstrument/id/{id} using an ID but set content type as excel and fetch the excel file

# 4.2) GET (/collectioninstrument/id/{id} using an ID but set content type as doc and fetch the doc file


# 5.1) GET (/collectioninstrument/id/{id} using an ID that is not in the DB
#  Scenario: Collection Instrument ID is not found
#    Given a collection instrument ID that does not exist
#    When a request is made for the collection instrument data using its ID which does not exist
#    Then information is returned saying the collection instrument is not found (ID)

# 5.2) GET (/collectioninstrument/id/{id} populate a new value in the DB and ensure it can be fetched via the API.


# 5.3) GET (/collectioninstrument/id/{id} remove ID from db and ensure it cannot be found via the API.









# ----------------------------------------------------------------------------------------------------------------------
# Survey ID Tests
# ----------------------------------------------------------------------------------------------------------------------
# GET (/collectioninstrument/surveyid/{surveyid}) Tests all possible API values for this endpoint. Tests are written in the style of:
# 1) Sunny day
# 2) invalid values
# 3) boundary case
# 4) exercising options/logic if any
# 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API


# 1) GET (/collectioninstrument/surveyid/{surveyid} using a valid survey ID
  Scenario: Obtain Collection Instrument data by survey ID
    Given a valid collection instrument survey ID
    When a request is made for the collection instrument data by survey ID
    Then check the returned data by collection instrument survey ID is correct


# 2.1) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID with the wrong path e.g. ONS.GOV.US
  Scenario: Collection Instrument survey ID domain name is incorrect
    Given a collection instrument survey ID with an incorrect domain name
    When a request is made for the collection instrument using the survey ID with the incorrect domain name
    Then information is returned saying the survey ID with the incorrect domain name is invalid


# 2.2) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID with the wrong number value e.g. ONS.GOV.UK.CI.00000000.0
  # TODO: Unsure what this 'number' portion of the survey ID is called? This should be changed to something more meaningful in here and in steps.py
  Scenario: Collection Instrument survey ID number value is incorrect
    Given a collection instrument survey ID with an incorrect number
    When a request is made for the collection instrument using the survey ID with the incorrect number
    Then information is returned saying the survey ID with the incorrect number is invalid


# 2.3) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID with the wrong TYPE value e.g. ONS.GOV.UK.XX.000.000.00000
  Scenario: Collection Instrument survey ID type is incorrect
    Given a collection instrument survey ID with an incorrect type name
    When a request is made for the collection instrument using the survey ID with the incorrect type name
    Then information is returned saying the survey ID with the incorrect type name is invalid


# 3.1) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID with a valid boundary case value e.g. ONS.GOV.UK.CI.000.000.00000 which is OK
  Scenario: Collection Instrument survey ID with the lowest boundary is not found
    Given a collection instrument survey ID with the lowest boundary that does not exist
    When a request is made for the collection instrument using the survey ID with the lowest boundary
    Then information is returned saying the survey ID with the lowest boundary is not found


# 3.2) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID with a valid boundary case value e.g. ONS.GOV.UK.XX.999.999.99999 which is OK
  Scenario: Collection Instrument survey ID with the highest boundary is not found
    Given a collection instrument survey ID with the highest boundary that does not exist
    When a request is made for the collection instrument using the survey ID with the highest boundary
    Then information is returned saying the survey ID with the highest boundary is not found

@wip
#  Currently, this test fails due to length validation. Should it fail for negative numbers?
# 3.3) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID with a boundary case value that is too small e.g. ONS.GOV.UK.XX.-100.-100.-10000 which is too small
  Scenario: Collection Instrument survey ID number value too low
    Given a collection instrument survey ID with a number value too low
    When a request is made for the collection instrument using the survey ID with the number value too low
    Then information is returned saying the survey ID with the number value too low is invalid


# 3.4) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID with a boundary case value that is too high e.g. ONS.GOV.UK.XX.9999.9999.999999 which is too big
    Scenario: Collection Instrument survey ID number value too high
    Given a collection instrument survey ID with a number value too high
    When a request is made for the collection instrument using the survey ID with the number value too high
    Then information is returned saying the survey ID with the number value too high is invalid


# 4.1) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID but set content type as excel and fetch the excel file

# 4.2) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID but set content type as doc and fetch the doc file


# 5.1) GET (/collectioninstrument/surveyid/{surveyid} using a survey ID that is not in the DB
#  Scenario: Collection Instrument survey ID is not found
#    Given a collection instrument survey ID that does not exist
#    When a request is made for the collection instrument data using its survey ID which does not exist
#    Then information is returned saying the collection instrument is not found (survey ID)

# 5.2) GET (/collectioninstrument/surveyid/{surveyid} populate a new value in the DB and ensure it can be fetched via the API.


# 5.3) GET (/collectioninstrument/surveyid/{surveyid} remove survey ID from db and ensure it cannot be found via the API.








































# POST (/collectioninstrument/) Tests all possible API values for this endpoint. Tests are written in the style of:
# 1) Sunny day
# 2) invalid values
# 3) boundary case
# 4) exercising options/logic if any
# 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API
#

# POST (/collectioninstument
#  Scenario: Create a new collection instrument
#    Given a new collection instrument
#    When a request is made to create the collection instrument
#    Then the collection instrument is created successfully
