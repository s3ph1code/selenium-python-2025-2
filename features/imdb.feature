Feature: Search movie and validate rating on IMDb

  Scenario: Validate title and rating for Inception
    Given I am on IMDb home
    When I search for movie "Inception"
    And I open the first movie result
    Then I should see the title contains "Inception"
    And I should see a numeric rating
