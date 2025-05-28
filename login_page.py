# locators/login_page.py

class LoginPageLocators:
    # Existing locators
    LOGIN_LINK = 'a.nav-link[title="Click here to access the Vault Verify portal."]'
    LOGIN_PAGE_HEADER = 'xpath=//h1[translate(normalize-space(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="login"]'
    COMMERCIAL_VERIFIER_HEADING = 'xpath=//h2[normalize-space()="Commercial Verifier"]'
    GOVERNMENT_VERIFIER_HEADING = 'xpath=//h2[normalize-space()="Government Verifier"]'
    EMPLOYER_HEADING = 'xpath=//h2[normalize-space()="Employer"]'
    EMPLOYEE_HEADING = 'xpath=//h2[normalize-space()="Employee"]'
    EMPLOYEE_REGISTER_NOW_LINK = (
        'xpath=//a[@id="ctl00_ContentPlaceHolder1_lnkRegister_EP"]'
        '//span[normalize-space()="Register Now"]'
    )
    ##EMPLOYEE_REGISTRATION_HEADER = 'xpath=//h1[normalize-space()="Employee Registration"]'
    EMPLOYEE_REGISTRATION_HEADER = 'xpath=//h1[translate(normalize-space(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="employee registration"]'

