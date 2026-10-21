Feature: Shopping Cart Functionality for SauceDemo Application
  As a logged-in user
  I want to manage items in my shopping cart
  So that I can prepare for checkout

  Background:
    Given I navigate to the login page
    And I login with username "standard_user" and password "secret_sauce"
    And I am on the products page

  Scenario: View empty cart
    When I click on the cart link
    Then I should be on the cart page
    And Cart should be empty

  Scenario: Add item to cart and view cart
    When I add product "Sauce Labs Backpack" to cart
    And I click on the cart link
    Then I should be on the cart page
    And Cart should contain "1" item
    And Item "Sauce Labs Backpack" should be in cart

  Scenario: Add multiple items to cart
    When I add product "Sauce Labs Backpack" to cart
    And I add product "Sauce Labs Bike Light" to cart
    And I add product "Sauce Labs Bolt T-Shirt" to cart
    And I click on the cart link
    Then I should be on the cart page
    And Cart should contain "3" items

  Scenario: Remove item from cart
    When I add product "Sauce Labs Backpack" to cart
    And I add product "Sauce Labs Bike Light" to cart
    And I click on the cart link
    And I remove item "Sauce Labs Backpack" from cart
    Then Cart should contain "1" item
    And Item "Sauce Labs Bike Light" should be in cart

  Scenario: Clear all items from cart
    When I add all products to cart
    And I click on the cart link
    And I remove all items from cart
    Then Cart should be empty

  Scenario: Continue shopping from cart
    When I add product "Sauce Labs Backpack" to cart
    And I click on the cart link
    And I click continue shopping button
    Then I should be on the products page

  Scenario: Calculate cart total
    When I add product "Sauce Labs Backpack" to cart
    And I add product "Sauce Labs Bike Light" to cart
    And I click on the cart link
    Then Cart total should be calculated correctly

  Scenario: Proceed to checkout from cart
    When I add product "Sauce Labs Backpack" to cart
    And I click on the cart link
    Then Checkout button should be visible
    When I click checkout button
    Then I should be on the checkout page
