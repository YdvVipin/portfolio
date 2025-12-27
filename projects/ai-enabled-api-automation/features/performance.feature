Feature: API Performance Testing
  As a Pokemon API user
  I want the API to respond quickly
  So that I have a good user experience

  Background:
    Given the Pokemon API is available

  @performance
  Scenario: Single Pokemon request performance
    When I request Pokemon with name "pikachu"
    Then the response status should be 200
    And the response time should be less than 2 seconds

  @performance
  Scenario Outline: Multiple endpoint performance
    When I request "<endpoint>" with identifier "<identifier>"
    Then the response status should be 200
    And the response time should be less than 3 seconds

    Examples:
      | endpoint | identifier |
      | pokemon  | 1          |
      | ability  | 1          |
      | item     | 1          |

  @performance
  Scenario: Pokemon list pagination performance
    When I request Pokemon list with limit 100 and offset 0
    Then the response status should be 200
    And the response time should be less than 5 seconds
    And the response should contain 100 Pokemon entries