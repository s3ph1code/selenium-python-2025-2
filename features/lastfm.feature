Feature: Search artist and validate latest release date on Last.fm

  Scenario: Validate latest release date for Bruno Mars
    Given I am on Lastfm home
    When I search for artist "Bruno Mars"
    And I open the first artist result
    Then I should see the latest release date displayed

