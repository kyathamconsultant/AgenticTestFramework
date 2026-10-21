Feature: Product Functionality for SauceDemo Application
  As a logged-in user
  I want to browse and interact with products
  So that I can select items to purchase

  Background:
    Given I navigate to the login page
    And I login with username "standard_user" and password "secret_sauce"
    And I am on the products page

  Scenario: View products on inventory page
    Then I should see at least 6 products
    And Products page should be displayed

  Scenario: Add single product to cart
    When I add product "Sauce Labs Backpack" to cart
    Then The cart badge should show "1"
    And Product should be added to cart successfully

  Scenario: Add multiple products to cart
    When I add product "Sauce Labs Backpack" to cart
    And I add product "Sauce Labs Bike Light" to cart
    And I add product "Sauce Labs Bolt T-Shirt" to cart
    Then The cart badge should show "3"

  Scenario: Add all products to cart
    When I add all products to cart
    Then The cart badge should show "6"

  Scenario: Remove product from cart
    When I add product "Sauce Labs Backpack" to cart
    And I remove product "Sauce Labs Backpack" from cart
    Then The cart badge should not be displayed

  Scenario: Sort products by name (A-Z)
    When I sort products by "Name (A to Z)"
    Then Products should be sorted alphabetically

  Scenario: Sort products by price (low to high)
    When I sort products by "Price (low to high)"
    Then Products should be sorted by price in ascending order

  Scenario: Sort products by price (high to low)
    When I sort products by "Price (high to low)"
    Then Products should be sorted by price in descending order

  Scenario: Sort products by relevance
    When I sort products by "Relevance"
    Then Products should be sorted by relevance

  Scenario: View product details
    When I click on product "Sauce Labs Backpack"
    Then I should see product details page
    And Product name should be "Sauce Labs Backpack"

  Scenario: Logout from products page
    When I click the menu button
    And I click logout
    Then I should be redirected to the login page
