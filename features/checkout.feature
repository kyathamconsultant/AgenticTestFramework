Feature: Checkout Functionality for SauceDemo Application
  As a logged-in user with items in cart
  I want to complete the checkout process
  So that I can place an order

  Background:
    Given I navigate to the login page
    And I login with username "standard_user" and password "secret_sauce"
    And I am on the products page
    And I add product "Sauce Labs Backpack" to cart
    And I add product "Sauce Labs Bike Light" to cart
    And I click on the cart link
    And I click checkout button

  Scenario: Checkout with valid information
    When I enter first name "John"
    And I enter last name "Doe"
    And I enter postal code "12345"
    And I click continue button
    Then I should be on the checkout summary page
    And Order summary should be displayed

  Scenario: Checkout with missing first name
    When I enter first name ""
    And I enter last name "Doe"
    And I enter postal code "12345"
    And I click continue button
    Then I should see a checkout error message
    And The checkout error message should contain "First Name is required"

  Scenario: Checkout with missing last name
    When I enter first name "John"
    And I enter last name ""
    And I enter postal code "12345"
    And I click continue button
    Then I should see a checkout error message
    And The checkout error message should contain "Last Name is required"

  Scenario: Checkout with missing postal code
    When I enter first name "John"
    And I enter last name "Doe"
    And I enter postal code ""
    And I click continue button
    Then I should see a checkout error message
    And The checkout error message should contain "Postal Code is required"

  Scenario: Complete order successfully
    When I enter first name "John"
    And I enter last name "Doe"
    And I enter postal code "12345"
    And I click continue button
    And I click finish button
    Then I should see order confirmation message
    And Order should be confirmed successfully

  Scenario Outline: Checkout with different users
    When I enter first name "<firstname>"
    And I enter last name "<lastname>"
    And I enter postal code "<postalcode>"
    And I click continue button
    Then I should <result>

    Examples:
      | firstname | lastname | postalcode | result |
      | John      | Doe      | 12345      | be on the checkout summary page |
      | Jane      | Smith    | 54321      | be on the checkout summary page |
      | Bob       | Johnson  | 99999      | be on the checkout summary page |

  Scenario: Verify totals on checkout summary
    When I enter first name "John"
    And I enter last name "Doe"
    And I enter postal code "12345"
    And I click continue button
    Then Item total should be displayed
    And Tax should be calculated
    And Final total should be displayed

  Scenario: Cancel checkout
    When I click cancel button
    Then I should be on the products page
