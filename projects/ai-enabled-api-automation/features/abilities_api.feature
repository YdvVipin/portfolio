Feature: Abilities API Testing
  As a Pokemon API user
  I want to retrieve ability information
  So that I can access ability data reliably

  Background:
    Given the Pokemon API is available

  @smoke
  Scenario Outline: Get ability by valid identifier
    When I request ability with identifier "<identifier>"
    Then the response status should be 200
    And the response time should be less than 5 seconds
    And the response should contain valid ability data

    Examples:
      | identifier  |
      | 1           |
      | stench      |
      | 2           |
      | drizzle     |

  @validation
  Scenario: Validate ability response structure
    When I request ability with identifier "stench"
    Then the response status should be 200
    And the ability response should contain required fields:
      | field          |
      | id             |
      | name           |
      | is_main_series |