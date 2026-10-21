Feature: Login Functionality for SauceDemo Application
  As a user
  I want to login to the SauceDemo application
  So that I can access the product catalog

  Background:
    Given I navigate to the login page

  Scenario: Successful login with valid credentials
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be redirected to the products page

  Scenario: Login failure with invalid password
    When I enter username "standard_user"
    And I enter password "wrong_password"
    And I click the login button
    Then I should see an error message
    And The error message should contain "Username and password do not match"

  Scenario: Login failure with locked user
    When I enter username "locked_out_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And The error message should contain "Sorry, this user has been locked out"

  Scenario: Login with empty username
    When I enter username ""
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And The error message should contain "Username is required"

  Scenario: Login with empty password
    When I enter username "standard_user"
    And I enter password ""
    And I click the login button
    Then I should see an error message
    And The error message should contain "Password is required"

  Scenario Outline: Login with multiple users
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should <result>

    Examples:
      | username      | password     | result                                |
      | standard_user | secret_sauce | be redirected to the products page   |
      | problem_user  | secret_sauce | be redirected to the products page   |
      | performance_glitch_user | secret_sauce | be redirected to the products page |
