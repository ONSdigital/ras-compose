Feature: Handle retrieval of Collection Instrument data


# ----------------------------------------------------------------------------------------------------------------------
# Collection Instrument data by valid identifier
# ----------------------------------------------------------------------------------------------------------------------
  @connect_to_database
  Scenario Outline: Get collection instrument data by valid identifier
    Given a valid <identifier_type>
    When a request is made for the collection instrument data
    Then check the returned data are correct
    And the response status code is <status_code>
    And the response returns an e-tag

    Examples:
        | identifier_type           | status_code |
        | Collection Instrument ID  | 200         |
        | Survey ID                 | 200         |
        | Reference                 | 200         |
        | Classifier                | 200         |


# ----------------------------------------------------------------------------------------------------------------------
# Collection Instrument file by valid identifier
# ----------------------------------------------------------------------------------------------------------------------
  @connect_to_database
  Scenario Outline: Get collection instrument data by valid identifier
    Given a valid <identifier_type>
    When a request is made for the collection instrument data
    Then check the returned data are correct
    And the response status code is <status_code>
    And the response returns an e-tag

    Examples:
        | identifier_type           | status_code |
        | Collection Instrument ID  | 200         |



# ----------------------------------------------------------------------------------------------------------------------
# Collection Instrument data by incorrect identifier
# ----------------------------------------------------------------------------------------------------------------------
  @connect_to_database
  Scenario Outline: Get collection instrument data by incorrect identifier
    Given a <identifier_type> of "<identifier>"
    When a request is made for the collection instrument data
    Then information is returned saying "<error_text>"
    And the response status code is <status_code>

    Examples: Incorrect domain name
        | identifier_type           | identifier                                    | error_text                      | status_code |
        | Collection Instrument ID  | urn:ons.gov.us:id:ci:001.001.00001            | Invalid ID supplied             | 400         |
        | Survey ID                 | urn:ons.gov.us:id:survey:001.001.00001        | Invalid ID supplied             | 400         |

    Examples: Incorrect number length
        | identifier_type           | identifier                                    | error_text                      | status_code |
        | Collection Instrument ID  | urn:ons.gov.uk:id:ci:001.001.000000           | Invalid ID supplied             | 400         |
        | Survey ID                 | urn:ons.gov.us:id:survey:001.001.00001        | Invalid ID supplied             | 400         |

    Examples: Incorrect type
        | identifier_type           | identifier                                    | error_text                      | status_code |
        | Collection Instrument ID  | urn:ons.gov.uk:id:XX:001.001.00001            | Invalid ID supplied             | 400         |
        | Survey ID                 | urn:ons.gov.uk:id:XX:001.001.00001            | Invalid ID supplied             | 400         |
        | Classifier                | 'TEST_MALFORMED_CLASSIFIER':'ABC'             | Bad input parameter             | 400         |

    Examples: Incorrect boundary value
        | identifier_type           | identifier                                    | error_text                      | status_code |
        | Collection Instrument ID  | urn:ons.gov.uk:id:ci:-1000.-1000.-100000      | Invalid ID supplied             | 400         |
        | Collection Instrument ID  | urn:ons.gov.uk:id:ci:9999.9999.999999         | Invalid ID supplied             | 400         |
        | Survey ID                 | urn:ons.gov.uk:id:survey:-1000.-1000.-100000  | Invalid ID supplied             | 400         |
        | Survey ID                 | urn:ons.gov.uk:id:survey:9999.9999.999999     | Invalid ID supplied             | 400         |

    Examples: Collection instrument not found
        | identifier_type           | identifier                                    | error_text                      | status_code |
        | Collection Instrument ID  | urn:ons.gov.uk:id:ci:000.000.00000            | Collection instrument not found | 404         |
        | Collection Instrument ID  | urn:ons.gov.uk:id:ci:999.999.99999            | Collection instrument not found | 404         |
        | Survey ID                 | urn:ons.gov.uk:id:survey:000.000.00000        | Collection instrument not found | 404         |
        | Survey ID                 | urn:ons.gov.uk:id:survey:999.999.99999        | Collection instrument not found | 404         |
        | Reference                 | bdd-test-reference                            | Collection instrument not found | 404         |
        | Classifier                | {'TEST_UNKNOWN_CLASSIFIER_NAME':'ABC'}        | Collection instrument not found | 404         |


# ----------------------------------------------------------------------------------------------------------------------
# Collection Instrument by valid identifiers (end-to-end test)
# ----------------------------------------------------------------------------------------------------------------------
  @connect_to_database
  Scenario Outline: Get new collection instrument data
    Given a new collection instrument has been created
    And the <identifier_type> of the new collection instrument
    When a request is made for the collection instrument data
    Then check the returned data are correct
    And the response status code is <successful_status_code>
    And the response returns an e-tag
    When the new collection instrument has been removed
    And a request is made for the collection instrument data
    Then information is returned saying "<error_text>"
    And the response status code is <unsuccessful_status_code>

    Examples:
      | identifier_type           | successful_status_code  | unsuccessful_status_code  | error_text                      |
      | Collection Instrument ID  | 200                     | 404                       | Collection instrument not found |
      | Survey ID                 | 200                     | 404                       | Collection instrument not found |
      | Reference                 | 200                     | 404                       | Collection instrument not found |
      | Classifier                | 200                     | 404                       | Collection instrument not found |
