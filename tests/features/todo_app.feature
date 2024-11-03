Feature: Todo Application

  Scenario: Add a task
    Given I am on the homepage
    When I add "Acceptance Task" to the list
    Then I should see "Acceptance Task" in the list

  Scenario: Edit a task
    Given I am on the homepage
    When I add "Task to Edit" to the list
    And I go to edit the task "Task to Edit"
    And I update the task to "Edited Task"
    Then I should see "Edited Task" in the list
    And I should not see "Task to Edit" in the list

  Scenario: Delete a task
    Given I am on the homepage
    When I add "Task to Delete" to the list
    And I delete the task "Task to Delete"
    Then I should not see "Task to Delete" in the list

  Scenario: Move a task to done
    Given I am on the homepage
    When I add "Task to Move to Done" to the list
    And I mark "Task to Move to Done" as done
    Then I should not see "Task to Move to Done" in the list

  Scenario: Delete a completed task
    Given I am on the homepage
    When I add "Completed Task" to the list
    And I mark "Completed Task" as done
    And I delete the completed task "Completed Task"
    Then I should not see "Completed Task" in the list
