Feature: Pokemon API Testing
  As a Pokemon API user
  I want to retrieve Pokemon information
  So that I can access Pokemon data reliably

  Background:
    Given the Pokemon API is available

  @smoke
  Scenario Outline: Get Pokemon by valid ID
    When I request Pokemon with ID "<pokemon_id>"
    Then the response status should be 200
    And the response time should be less than 5 seconds
    And the response should contain valid Pokemon data
    And the Pokemon ID should be <pokemon_id>

    Examples:
      | pokemon_id |
      | 1          |
      | 25         |
      | 150        |

  @smoke
  Scenario Outline: Get Pokemon by valid name
    When I request Pokemon with name "<pokemon_name>"
    Then the response status should be 200
    And the response time should be less than 5 seconds
    And the response should contain valid Pokemon data
    And the Pokemon name should be "<pokemon_name>"

    Examples:
      | pokemon_name |
      | pikachu      |
      | charizard    |
      | mewtwo       |

  @negative
  Scenario Outline: Get Pokemon with invalid ID
    When I request Pokemon with ID "<invalid_id>"
    Then the response status should be 404

    Examples:
      | invalid_id |
      | 0          |
      | -1         |
      | 99999      |

  @negative
  Scenario Outline: Get Pokemon with invalid name
    When I request Pokemon with name "<invalid_name>"
    Then the response status should be 404

    Examples:
      | invalid_name   |
      | invalidpokemon |
      | 123abc         |

  @validation
  Scenario: Validate Pokemon response structure
    When I request Pokemon with name "pikachu"
    Then the response status should be 200
    And the response should contain required fields:
      | field     |
      | id        |
      | name      |
      | height    |
      | weight    |
      | abilities |
      | types     |
    And the Pokemon should have at least one ability
    And the Pokemon should have at least one type

  @integration
  Scenario: Pokemon evolution chain integration
    When I request Pokemon with name "pikachu"
    Then the response status should be 200
    When I get the species information for the Pokemon
    Then the response status should be 200
    When I get the evolution chain for the species
    Then the response status should be 200
    And the evolution chain should contain species information