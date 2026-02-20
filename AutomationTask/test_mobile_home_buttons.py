"""
I decided to automate one window flow. Specifically the mobile/modular home window.
TC-006 and TC-007 showcase the steps that i automated.

"""

from playwright.sync_api import Page, expect


BASE_URL = "https://hb-test.stage.sirenltd.dev/"
ZIP_CODE = "10001"



def navigate_to_mobile_home_warning(page: Page) -> None:
    page.goto(BASE_URL)
    page.locator("#zipCode").fill(ZIP_CODE)
    page.locator("[data-submit-btn]").click()

    page.wait_for_selector("text=Which elements of the kitchen would you like to update?",
                           timeout=10_000)
    page.get_by_text("Kitchen cabinets", exact=True).click()
    page.get_by_role("button", name="Next").click()

    page.wait_for_selector("text=What would you like to do with your kitchen cabinets?",
                           timeout=8_000)
    page.get_by_text("Replace all or most cabinets", exact=True).click()
    page.get_by_role("button", name="Next").click()

    page.wait_for_selector("text=What type of property is this?", timeout=8_000)
    page.get_by_text("Multi-family home", exact=True).click()
    page.get_by_role("button", name="Next").click()

    page.wait_for_selector("text=Is it a mobile, modular or manufactured home?",
                           timeout=8_000)
    page.locator("[data-autotest-radio-internalmobilehome-yes] + label").click()

    expect(page.get_by_text(
        "Unfortunately, our contractors do not work with mobile, modular or manufactured homes.",
        exact=False,
    )).to_be_visible(timeout=3_000)


class TestMobileHomeButtons:
    def test_no_button_shows_exit_screen(self, page: Page) -> None:
        navigate_to_mobile_home_warning(page)

        page.locator("[data-autotest-button-submit-no]").click()

        exit_message = page.get_by_text("Sorry to see you go", exact=False)
        expect(exit_message).to_be_visible(timeout=5_000), (
            "Clicking 'No' didn't show the exit screen."
        )

    def test_yes_button_advances_to_next_step(self, page: Page) -> None:
        navigate_to_mobile_home_warning(page)

        page.locator("[data-autotest-button-submit-yes]").click()

        expect(page.get_by_text(
            "Are you the homeowner or authorized to make property changes?",
            exact=False,
        )).to_be_visible(timeout=5_000)
