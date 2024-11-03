from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@given('I am on the homepage')
def step_given_on_homepage(context):
    context.driver = webdriver.Chrome()  # Ensure you have the correct driver installed
    context.driver.get('http://127.0.0.1:5000/')  # Change to your app URL

@when('I add "{task}" to the list')
def step_when_add_task(context, task):
    task_input = context.driver.find_element(By.NAME, 'task')
    task_input.send_keys(task)
    task_input.send_keys(Keys.RETURN)

@then('I should see "{task}" in the list')
def step_then_see_task(context, task):
    assert task in context.driver.page_source

@when('I go to edit the task "{task}"')
def step_when_edit_task(context, task):
    # Find the edit button associated with the specific task
    edit_button_xpath = f"//tr[td[contains(text(), '{task}')]]/td/div/a/button[contains(text(), 'Edit')]"
    edit_button = context.driver.find_element(By.XPATH, edit_button_xpath)
    edit_button.click()

@when('I update the task to "{new_task}"')
def step_when_update_task(context, new_task):
    task_input = context.driver.find_element(By.NAME, 'task')
    task_input.clear()  # Clear the input field
    task_input.send_keys(new_task)
    task_input.send_keys(Keys.RETURN)

@when('I delete the task "{task}"')
def step_when_delete_task(context, task):
    delete_button_xpath = f"//tr[td[contains(text(), '{task}')]]/td/div/form/button[contains(text(), 'Delete')]"
    delete_button = context.driver.find_element(By.XPATH, delete_button_xpath)
    delete_button.click()

@when('I mark "{task}" as done')
def step_when_mark_as_done(context, task):
    done_button_xpath = f"//tr[td[contains(text(), '{task}')]]/td/div/form/button[contains(text(), 'Done')]"
    done_button = context.driver.find_element(By.XPATH, done_button_xpath)
    done_button.click()

@when('I delete the completed task "{task}"')
def step_when_delete_completed_task(context, task):
    delete_done_button_xpath = f"//tr[td[contains(text(), '{task}')]]/td/div/form/button[contains(text(), 'Delete')]"
    delete_done_button = context.driver.find_element(By.XPATH, delete_done_button_xpath)
    delete_done_button.click()

@then('I should not see "{task}" in the list')
def step_then_not_see_task(context, task):
    assert task not in context.driver.page_source
    context.driver.quit()  # Close the browser after the test
