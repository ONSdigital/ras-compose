Feature: Collection Instrument (CI) Status
  In order to request CI data the CI micro service
  must be running and responding to status requests.

  Scenario: CI Status Running
    Given The CI status is active
     When A request for status is given
     Then The CI micro service returns status information about itself

