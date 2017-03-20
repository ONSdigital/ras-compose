#Feature: Collection Instrument (CI) Status
#  In order to request CI data the CI micro service
#  must be running and responding to status requests.
#
## ----------------------------------------------------------------------------------------------------------------------
## GET - Collection Instrument Tests (one or more)
## ----------------------------------------------------------------------------------------------------------------------
## (/collectioninstrument) Tests all possible API values for this endpoint. Tests are written in the style of:
## 1) Sunny day
## 2) invalid values
## 3) boundary case
## 4) exercising options/logic if any
## 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API
## 1) GET (/collectioninstrument)
#  @connect_to_database
#  Scenario: Obtain data for one or more Collection Instruments
#    Given one or more collection instruments exist
#    When a request is made for data for one or more collection instruments
#    Then check the returned data for one or more collection instruments are correct
#
## 2.1) GET (Placeholder for any boundary tests)
#
#
## 3.1) GET (Placeholder for any boundary tests)
#
#
## 4.1) GET (Placeholder for any options/logic tests)
#
#
## 5.1) GET (Placeholder for any end-to-end black box tests)
#
#
#
## ----------------------------------------------------------------------------------------------------------------------
## GET - Collection Instrument query by 'classifier'
## ----------------------------------------------------------------------------------------------------------------------
## GET (/collectioninstrument/?classifier={"CLASSIFIER_1":"A","CLASSIFIER2":"B"}) Tests all possible API values for this endpoint. Tests are written in the style of:
## 1) Sunny day
## 2) invalid values
## 3) boundary case
## 4) exercising options/logic if any
## 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API
#
## 1) GET (/collectioninstrument/?classifier={"classifier"})
#  @connect_to_database
#  Scenario: Obtain Collection Instrument data by classifier
#    Given a valid collection instrument classifier
#    When a request is made for the collection instrument data by classifier
#    Then check the returned data by collection instrument classifier are correct
#
#
## 2.1) GET (/collectioninstrument/?classifier={"classifier"}) using an unknown classifier e.g. {'TEST_UNKNOWN_CLASSIFIER_NAME': 'ABC'}
#  Scenario: Collection Instrument classifier is unknown
#    Given an unknown collection instrument classifier name
#    When a request is made for the collection instrument using the unknown classifier name
#    Then information is returned saying the collection instrument is not found using the unknown classifier name
#
#
## 2.2) GET (/collectioninstrument/?classifier={"classifier"}) using a classifier without enclosed braces e.g. ?classifier="LEGAL_STATUS":"A"
#  Scenario: Collection Instrument classifier query without enclosing braces
#    Given a collection instrument classifier query without enclosing braces
#    When a request is made for the collection instrument using the classifier without enclosed braces
#    Then information is returned saying the classifier without enclosed braces is invalid
#
#
## 2.3) GET (/collectioninstrument/?classifier={"classifier"}) using a the wrong query type e.g. ?incorrect={"LEGAL_STATUS":"A"}
#  Scenario: Collection Instrument classifier query using an incorrect query type
#    Given a collection instrument query using an incorrect query type
#    When a request is made for the collection instrument classifier using the incorrect query type
#    Then information is returned saying the classifier using the incorrect query type is invalid
#
#
## 3.1) GET (Placeholder for any boundary tests)
#
#
## 4.1) GET (Placeholder for any options/logic tests)
#
#
## 5.1) GET (Placeholder for any end-to-end black box tests)
#
#
#
#
## ----------------------------------------------------------------------------------------------------------------------
## GET - Collection Instrument ID Tests
## ----------------------------------------------------------------------------------------------------------------------
## GET (/collectioninstrument/id/{id}) Tests all possible API values for this endpoint. Tests are written in the style of:
## 1) Sunny day
## 2) invalid values
## 3) boundary case
## 4) exercising options/logic if any
## 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API
#
## 1) GET (/collectioninstrument/id/{id}) using a valid ID
#  @connect_to_database
#  Scenario: Obtain Collection Instrument data by ID
#    Given a valid collection instrument ID
#    When a request is made for the collection instrument data by ID
#    Then check the returned data by collection instrument ID are correct
#
#
## 2.1) GET (/collectioninstrument/id/{id}) using an ID with the wrong path e.g. ONS.GOV.US
#  Scenario: Collection Instrument ID domain name is incorrect
#    Given a collection instrument ID with an incorrect domain name
#    When a request is made for the collection instrument using the ID with the incorrect domain name
#    Then information is returned saying the ID with the incorrect domain name is invalid
#
#
## 2.2) GET (/collectioninstrument/id/{id}) using an ID with the wrong number value e.g. ONS.GOV.UK.CI.00000000.0
#  # TODO: Unsure what this 'number' portion of the ID is called? This should be changed to something more meaningful in here and in steps.py
#  Scenario: Collection Instrument ID number value is incorrect
#    Given a collection instrument ID with an incorrect number
#    When a request is made for the collection instrument using the ID with the incorrect number
#    Then information is returned saying the ID with the incorrect number is invalid
#
#
## 2.3) GET (/collectioninstrument/id/{id}) using an ID with the wrong TYPE value e.g. ONS.GOV.UK.XX.000.000.00000
#  Scenario: Collection Instrument ID type is incorrect
#    Given a collection instrument ID with an incorrect type name
#    When a request is made for the collection instrument using the ID with the incorrect type name
#    Then information is returned saying the ID with the incorrect type name is invalid
#
#
## 3.1) GET (/collectioninstrument/id/{id}) using an ID with a valid boundary case value e.g. ONS.GOV.UK.CI.000.000.00000 which is OK
#  Scenario: Collection Instrument ID with the lowest boundary is not found
#    Given a collection instrument ID with the lowest boundary that does not exist
#    When a request is made for the collection instrument using the ID with the lowest boundary
#    Then information is returned saying the ID with the lowest boundary is not found
#
#
## 3.2) GET (/collectioninstrument/id/{id}) using an ID with a valid boundary case value e.g. ONS.GOV.UK.XX.999.999.99999 which is OK
#  Scenario: Collection Instrument ID with the highest boundary is not found
#    Given a collection instrument ID with the highest boundary that does not exist
#    When a request is made for the collection instrument using the ID with the highest boundary
#    Then information is returned saying the ID with the highest boundary is not found
#
#
##  This test fails due to length validation. Should it fail for negative numbers?
## 3.3) GET (/collectioninstrument/id/{id}) using an ID with a boundary case value that is too small e.g. ONS.GOV.UK.XX.-100.-100.-10000 which is too small
#  Scenario: Collection Instrument ID number value too low
#    Given a collection instrument ID with a number value too low
#    When a request is made for the collection instrument using the ID with the number value too low
#    Then information is returned saying the ID with the number value too low is invalid
#
#
## 3.4) GET (/collectioninstrument/id/{id}) using an ID with a boundary case value that is too high e.g. ONS.GOV.UK.XX.9999.9999.999999 which is too big
#  Scenario: Collection Instrument ID number value too high
#    Given a collection instrument ID with a number value too high
#    When a request is made for the collection instrument using the ID with the number value too high
#    Then information is returned saying the ID with the number value too high is invalid
#
#
## 4.1) GET (/collectioninstrument/id/{id}) using an ID but set content type as excel and fetch the excel file
## TODO - This needs testing
#
#
## 4.2) GET (/collectioninstrument/id/{id}) using an ID but set content type as doc and fetch the doc file
## TODO - This needs testing
#
#
## 5.1) GET (/collectioninstrument/id/{id}) using an ID that is not in the DB
#  @connect_to_database
#  Scenario: Collection Instrument ID is not found
#    Given a collection instrument ID that does not exist
#    When a request is made for the collection instrument data using its ID which does not exist
#    Then information is returned saying the collection instrument is not found (ID)
#
#
## 5.2) GET (/collectioninstrument/id/{id}) populate a new value in the DB and ensure it can be fetched via the API.
#  @connect_to_database
#  Scenario: Add new Collection Instrument for obtaining data by ID
#    Given a newly created collection instrument for obtaining data by ID
#    When a request is made for the newly created collection instrument data by ID
#    Then check the returned data by collection instrument ID are correct
#
#
## 5.3) GET (/collectioninstrument/id/{id}) remove ID from db and ensure it cannot be found via the API.
#  @connect_to_database
#  Scenario: Remove new Collection Instrument to ensure its data cannot be obtained
#    Given a newly created collection instrument for obtaining data by ID has been removed
#    When a request is made for the removed collection instrument data by ID
#    Then information is returned saying the removed collection instrument is not found (ID)
#
#
#
#
#
## ----------------------------------------------------------------------------------------------------------------------
## GET - Survey ID Tests
## ----------------------------------------------------------------------------------------------------------------------
## GET (/collectioninstrument/surveyid/{surveyid}) Tests all possible API values for this endpoint. Tests are written in the style of:
## 1) Sunny day
## 2) invalid values
## 3) boundary case
## 4) exercising options/logic if any
## 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API
#
#
## 1) GET (/collectioninstrument/surveyid/{surveyid}) using a valid survey ID
#  @connect_to_database
#  Scenario: Obtain Collection Instrument data by survey ID
#    Given a valid collection instrument survey ID
#    When a request is made for the collection instrument data by survey ID
#    Then check the returned data by collection instrument survey ID are correct
#
#
## 2.1) GET (/collectioninstrument/surveyid/{surveyid}) using a survey ID with the wrong path e.g. ONS.GOV.US
#  Scenario: Collection Instrument survey ID domain name is incorrect
#    Given a collection instrument survey ID with an incorrect domain name
#    When a request is made for the collection instrument using the survey ID with the incorrect domain name
#    Then information is returned saying the survey ID with the incorrect domain name is invalid
#
#
## 2.2) GET (/collectioninstrument/surveyid/{surveyid}) using a survey ID with the wrong number value e.g. ONS.GOV.UK.CI.00000000.0
#  # TODO: Unsure what this 'number' portion of the survey ID is called? This should be changed to something more meaningful in here and in steps.py
#  Scenario: Collection Instrument survey ID number value is incorrect
#    Given a collection instrument survey ID with an incorrect number
#    When a request is made for the collection instrument using the survey ID with the incorrect number
#    Then information is returned saying the survey ID with the incorrect number is invalid
#
#
## 2.3) GET (/collectioninstrument/surveyid/{surveyid}) using a survey ID with the wrong TYPE value e.g. ONS.GOV.UK.XX.000.000.00000
#  Scenario: Collection Instrument survey ID type is incorrect
#    Given a collection instrument survey ID with an incorrect type name
#    When a request is made for the collection instrument using the survey ID with the incorrect type name
#    Then information is returned saying the survey ID with the incorrect type name is invalid
#
#
## 3.1) GET (/collectioninstrument/surveyid/{surveyid}) using a survey ID with a valid boundary case value e.g. ONS.GOV.UK.CI.000.000.00000 which is OK
#  Scenario: Collection Instrument survey ID with the lowest boundary is not found
#    Given a collection instrument survey ID with the lowest boundary that does not exist
#    When a request is made for the collection instrument using the survey ID with the lowest boundary
#    Then information is returned saying the survey ID with the lowest boundary is not found
#
#
## 3.2) GET (/collectioninstrument/surveyid/{surveyid}) using a survey ID with a valid boundary case value e.g. ONS.GOV.UK.XX.999.999.99999 which is OK
#  Scenario: Collection Instrument survey ID with the highest boundary is not found
#    Given a collection instrument survey ID with the highest boundary that does not exist
#    When a request is made for the collection instrument using the survey ID with the highest boundary
#    Then information is returned saying the survey ID with the highest boundary is not found
#
#
##  This test fails due to length validation. Should it fail for negative numbers?
## 3.3) GET (/collectioninstrument/surveyid/{surveyid}) using a survey ID with a boundary case value that is too small e.g. ONS.GOV.UK.XX.-100.-100.-10000 which is too small
#  Scenario: Collection Instrument survey ID number value too low
#    Given a collection instrument survey ID with a number value too low
#    When a request is made for the collection instrument using the survey ID with the number value too low
#    Then information is returned saying the survey ID with the number value too low is invalid
#
#
## 3.4) GET (/collectioninstrument/surveyid/{surveyid}) using a survey ID with a boundary case value that is too high e.g. ONS.GOV.UK.XX.9999.9999.999999 which is too big
#  Scenario: Collection Instrument survey ID number value too high
#    Given a collection instrument survey ID with a number value too high
#    When a request is made for the collection instrument using the survey ID with the number value too high
#    Then information is returned saying the survey ID with the number value too high is invalid
#
#
## 4.1) GET (Placeholder for any options/logic tests)
#
#
## 5.1) GET (Placeholder for any end-to-end black box tests)
#
#
#
#
## ----------------------------------------------------------------------------------------------------------------------
## GET - Reference Tests
## ----------------------------------------------------------------------------------------------------------------------
## GET (/collectioninstrument/reference/{reference}) Tests all possible API values for this endpoint. Tests are written in the style of:
## 1) Sunny day
## 2) invalid values
## 3) boundary case
## 4) exercising options/logic if any
## 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API
#
#
## 1) GET (/collectioninstrument/reference/{reference}) using a valid reference
#  @connect_to_database
#  Scenario: Obtain Collection Instrument data by reference
#    Given a valid collection instrument reference
#    When a request is made for the collection instrument data by reference
#    Then check the returned data by collection instrument reference are correct
#
#
## 2.1) GET (/collectioninstrument/reference/{reference}) using a reference with name that does not exist e.g. rsi-fuel(BDDTEST)
#  Scenario: Collection Instrument reference name does not exist
#    Given a collection instrument reference that does not exist
#    When a request is made for the collection instrument using the reference that does not exist
#    Then information is returned saying the reference does not exist
#
#
## 2.3) GET (/collectioninstrument/reference/{reference}) using a reference with a non-ASCII character e.g.
#  Scenario: Collection Instrument reference has non-ASCII character
#    Given a collection instrument reference with a non-ASCII character
#    When a request is made for the collection instrument using the reference with the non-ASCII character
#    Then information is returned saying the reference with the non-ASCII character is invalid
#
#
## 3.1) GET (Placeholder for any boundary tests)
#
#
## 4.1) GET (Placeholder for any options/logic tests)
#
#
## 5.1) GET (Placeholder for any end-to-end black box tests)
#
#
#
#
## ----------------------------------------------------------------------------------------------------------------------
## POST - Create Collection Instrument
## ----------------------------------------------------------------------------------------------------------------------
## POST (/collectioninstrument/{collection_instrument}) Tests all possible API values for this endpoint. Tests are written in the style of:
## 1) Sunny day
## 2) invalid values
## 3) boundary case
## 4) exercising options/logic if any
## 5) end to end black box i.e. adding to DB, checking it exists via API. removing from DB checking it does not exist via API
#
## 1) POST (/collectioninstrument/{collection_instrument}) using a correctly formed collection instrument
#  Scenario: Create a new collection instrument
#    Given a new collection instrument
#    When a request is made to create the collection instrument
#    Then the collection instrument is created successfully
#
#
## 2.1) POST (Placeholder for any invalid value tests)
#
#
## 3.1) POST (Placeholder for any boundary tests)
#
#
## 4.1) POST (Placeholder for any options/logic tests)
#
#
## 5.1) POST (Placeholder for any end-to-end black box tests)
#