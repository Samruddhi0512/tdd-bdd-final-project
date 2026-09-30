from behave import when, then

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button"""
    button_id = button.lower() + "-btn"

    context.driver.find_element(
        By.ID,
        button_id
    ).click()


@then('I should see "{name}" in the results')
def step_impl(context, name):
    """Verify that a name is present in the results"""

    found = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_results"),
            name
        )
    )

    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Verify that a name is not present"""

    element = context.driver.find_element(
        By.ID,
        "search_results"
    )

    assert name not in element.text


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify that a message is displayed"""

    found = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"),
            message
        )
    )

    assert found
