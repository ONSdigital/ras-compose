Feature: Collection Instrument (CI) Status
  In order to request CI data the CI micro service
  must be running and responding to status requests.


# Not currently working. Is '/status' an endpoint now?
#  Scenario: CI Status Running
#    Given The CI status is active
#     When A request for status is given
#     Then The CI micro service returns status information about itself


# POST (/collectioninstrument/) Tests all possible API values for this endpoint. Tests are written in the style of:
# 1) Sunny day
# 2) invalid values
# 3) boundary case
# 4) exercising options/logic if any
# 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API


# 1) GET (/collectioninstrument/id/{id} using a valid ID
  Scenario: Obtain Collection Instrument data
    Given a valid collection instrument ID
    When a request is made for the collection instrument data
    Then check the returned data is correct

# 2.1) GET (/collectioninstrument/id/{id} using an ID with the wrong path e.g. ONS.GOV.US
  Scenario: Collection Instrument ID is invalid
    Given an incorrect collection instrument ID
    When a request is made for the collection instrument data using this ID
    Then information is returned saying the ID is invalid

# 2.2) GET (/collectioninstrument/id/{id} using an ID with the wrong number value e.g. ONS.GOV.UK.CI.00000000.0

# 2.3) GET (/collectioninstrument/id/{id} using an ID with the wrong TYPE value e.g. ONS.GOV.UK.XX.00000000.0


# 3.1) GET (/collectioninstrument/id/{id} using an ID with a boundary case value e.g. ONS.GOV.UK.XX.0000.000.000.000 which is OK

# 3.2) GET (/collectioninstrument/id/{id} using an ID with a boundary case value e.g. ONS.GOV.UK.XX.9999.999.999.999 which is OK

# 3.3) GET (/collectioninstrument/id/{id} using an ID with a boundary case value e.g. ONS.GOV.UK.XX.-1.000.000.000 which is to small

# 3.4) GET (/collectioninstrument/id/{id} using an ID with a boundary case value e.g. ONS.GOV.UK.XX.99999.000.000.000 which is to big


# 4.1) GET (/collectioninstrument/id/{id} using an ID but set content type as excel and fetch the excel file

# 4.2) GET (/collectioninstrument/id/{id} using an ID but set content type as doc and fetch the doc file




# 5.1) GET (/collectioninstrument/id/{id} using an ID that is not in the DB
  Scenario: Collection Instrument is not found
    Given a collection instrument that does not exist
    When a request is made for the collection instrument data using its ID
    Then information is returned saying the collection instrument is not found

# 5.2) GET (/collectioninstrument/id/{id} populate a new value in the DB and ensure it can be fetched via the API.






# POST (/collectioninstrument/) Tests all possible API values for this endpoint. Tests are written in the style of:
# 1) Sunny day
# 2) invalid values
# 3) boundary case
# 4) exercising options/logic if any
# 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API


# POST (/collectioninstument
  Scenario: Create a new collection instrument
    Given a new collection instrument
    When a request is made to create the collection instrument
    Then the collection instrument is created successfully

