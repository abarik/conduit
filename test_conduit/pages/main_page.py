from selenium.webdriver.common.by import By
from test_conduit.pages.base_page import BasePage


class MainPage(BasePage):
    class NavBar:
        """Navbar"""
        LOGO_LINK = (By.XPATH, '//div[@id="app"]/nav/div/a[@href="#/" and contains(text(), "conduit")]')
        HOME_BUTTON = (By.XPATH, '//a[@href="#/" and contains(text(), "Home")]')
        SIGNIN_BUTTON = (By.XPATH, '//a[@href="#/login"]')
        SIGNUP_BUTTON = (By.XPATH, '//a[@href="#/register"]')
        # LOGOUT_BUTTON = (By.XPATH, '//i[@class="ion-android-exit"]/..')
        LOGOUT_BUTTON = (By.XPATH, '//a[contains(text(), "Log out")]')
        NEW_ARTICLE_BUTTON = (By.XPATH, '//a[@href="#/editor"]')
        SETTINGS_BUTTON = (By.XPATH, '//a[@href="#/settings"]')

    class Home:
        """Cookie - Accept/Decline"""
        ACCEPT_LINK = (By.XPATH, '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')

        """Popular tags"""
        POPULAR_TAGS = (By.XPATH, '//p[contains(text(), "Popular Tags")]//following-sibling::div[@class="tag-list"]//a')
        PAGES = (By.XPATH, '//ul[@class="pagination"]/li/a[contains(@class, "page-link")]')
        ARTICLES_TITLES = (
            By.XPATH, '//div[@class="article-preview"]//a[@class="preview-link" and contains(@href, "articles")]/h1')
        ARTICLES_LINKS = (
            By.XPATH, '//div[@class="article-preview"]//a[@class="preview-link" and contains(@href, "articles")]')

        ONE_LINK = (By.XPATH, '//a[contains(@href, "l=intezet")]')

    class RegistrationForm:
        """ SIGNUP FORM"""
        SIGNUP_USERNAME_FIELD = (By.XPATH, '//input[@type="text" and @placeholder="Username"]')
        SIGNUP_EMAIL_FIELD = (By.XPATH, '//input[@type="text" and @placeholder="Email"]')
        SIGNUP_PASSWORD_FIELD = (By.XPATH, '//input[@type="password" and @placeholder="Password"]')
        SIGNUP_FORM_BUTTON = (
            By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right" and contains(text(), "Sign up")]')
        SIGNUP_SUCCESS_OK_BUTTON = (By.XPATH, '//button[@class="swal-button swal-button--confirm"]')

    class LoginForm:
        """ LOGIN FORM"""
        LOGIN_EMAIL_FIELD = (By.XPATH, '//input[@type="text" and @placeholder="Email"]')
        LOGIN_PASSWORD_FIELD = (By.XPATH, '//input[@type="password" and @placeholder="Password"]')
        LOGIN_FORM_BUTTON = (
            By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right" and contains(text(), "Sign in")]')

    class NewArticleForm:
        """ NEW ARTICLE FORM"""
        ARTICLE_TITLE_FIELD = (By.XPATH, '//input[@type="text" and @placeholder="Article Title"]')
        ARTICLE_ABOUT_FIELD = (By.XPATH, '//input[@type="text" and @placeholder="What\'s this article about?"]')
        ARTICLE_TEXTAREA = (By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')
        ARTICLE_TAG_FIELD = (By.XPATH, '//input[@type="text" and @placeholder="Enter tags"]')
        ARTICLE_PUBLISH_BUTTON = (By.XPATH, '//button[@type="submit" and contains(text(), "Publish Article")]')

    class SettingsForm:
        """ SETTINGS FORM"""
        SHORTBIO_TEXTAREA = (By.XPATH, '//textarea[@placeholder="Short bio about you"]')
        UPDATE_SETTINGS_BUTTON = (
            By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right" and contains(text(), "Update Settings")]')
        UPDATE_SUCCESS_OK_BUTTON = (
            By.XPATH, '//button[@class="swal-button swal-button--confirm" and contains(text(), "OK")]')

    class EditArticle:
        DELETE_BUTTON = (By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')
        COMMENT_TEXTAREA = (By.XPATH, '//textarea[@placeholder="Write a comment..."]')
        POST_BUTTON = (By.XPATH, '//button[@class="btn btn-sm btn-primary" and text()="Post Comment"]')

    """class variables to reach controls"""
    NAV_BAR = NavBar()
    HOME = Home()
    REG_FORM = RegistrationForm()
    LOG_FORM = LoginForm()
    NEW_ART_FORM = NewArticleForm()
    SETTINGS_FORM = SettingsForm()
    EDT_ART_FORM = EditArticle()
