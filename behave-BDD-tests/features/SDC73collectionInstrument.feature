Feature: Collection Instrument (CI) Status
  In order to request CI data the CI micro service
  must be running and responding to status requests.


# Not currently working. Is '/status' an endpoint now?
#  Scenario: CI Status Running
#    Given The CI status is active
#     When A request for status is given
#     Then The CI micro service returns status information about itself


# GET (/collectioninstrument/id/{id}
  Scenario: Obtain Collection Instrument data
    Given a valid collection instrument ID
    When a request is made for the collection instrument data
    Then check the returned data is correct


  Scenario: Collection Instrument ID is invalid
    Given an incorrect collection instrument ID
    When a request is made for the collection instrument data using this ID
    Then information is returned saying the ID is invalid


  Scenario: Collection Instrument is not found
    Given a collection instrument that does not exist
    When a request is made for the collection instrument data using its ID
    Then information is returned saying the collection instrument is not found


# POST (/collectioninstument
  Scenario: Create a new collection instrument
    Given a new collection instrument
    When a request is made to create the collection instrument
    Then the collection instrument is created successfully

