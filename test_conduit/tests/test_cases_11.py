import csv
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

from test_conduit.config.browser import Browser
from test_conduit.pages.main_page import MainPage
from test_conduit.pages.base_page import Mode
from test_conduit.config.data_for_test import DataForTest


class TestConduit:
    def setup(self):
        try:
            self.data_for_test = DataForTest()
            self.browser = Browser().get_browser()
            self.mp = MainPage(self.browser, self.data_for_test.BASE_URL, mode=Mode.TIMESLEEP)

        except BaseException:
            self.mp.log_error('Webdriver error.')
            assert False
        else:
            assert True

        self.__register(self.data_for_test.GEN_USER)  # register a new general user

    def teardown(self):
        self.mp.close_test()

    def __register(self, user):
        self.mp.go()
        try:
            self.mp.do_click(MainPage.NAV_BAR.SIGNUP_BUTTON, wtime=2)
            self.mp.get_url('register', wtime=2)  # waiting for url change
            self.mp.do_send_keys(MainPage.REG_FORM.SIGNUP_USERNAME_FIELD, user.user_name, wtime=0.1)
            self.mp.do_send_keys(MainPage.REG_FORM.SIGNUP_EMAIL_FIELD, user.user_email, wtime=0.1)
            self.mp.do_send_keys(MainPage.REG_FORM.SIGNUP_PASSWORD_FIELD, user.password, wtime=0.1)
            self.mp.do_click(MainPage.REG_FORM.SIGNUP_FORM_BUTTON, wtime=0.1)
            self.mp.do_click(MainPage.REG_FORM.SIGNUP_SUCCESS_OK_BUTTON, wtime=3)
            self.__logout()
        except BaseException:
            self.mp.log_error('General user registration failed.')
            assert False
        else:
            assert True
        return None

    def __login(self, user):
        self.mp.go()
        try:
            self.mp.do_click(MainPage.NAV_BAR.SIGNIN_BUTTON, wtime=2)
            self.mp.get_url('login', wtime=2)  # waiting for url change
        except BaseException:
            self.mp.log_error('Login page cannot be reached.')
            assert False
        else:
            assert True

        try:
            self.mp.do_send_keys(MainPage.LOG_FORM.LOGIN_EMAIL_FIELD, user.user_email, wtime=0.1)
            self.mp.do_send_keys(MainPage.LOG_FORM.LOGIN_PASSWORD_FIELD, user.password, wtime=0.1)
            self.mp.do_click(MainPage.LOG_FORM.LOGIN_FORM_BUTTON, wtime=0.1)
        except BaseException:
            self.mp.log_error('Login failed.')
            assert False
        else:
            assert True
        return None

    def __logout(self):
        try:
            self.mp.do_click(MainPage.NAV_BAR.LOGOUT_BUTTON, wtime=1)
        except:
            pass
        return None

    def __new_article(self, title, about, body, *tags):
        try:
            self.mp.do_click(MainPage.NAV_BAR.NEW_ARTICLE_BUTTON, wtime=1)
            self.mp.get_url('editor', wtime=1)
            self.mp.do_send_keys(MainPage.NEW_ART_FORM.ARTICLE_TITLE_FIELD, title, wtime=0.1)
            self.mp.do_send_keys(MainPage.NEW_ART_FORM.ARTICLE_ABOUT_FIELD, about, wtime=0.1)
            self.mp.do_send_keys(MainPage.NEW_ART_FORM.ARTICLE_TEXTAREA, body, wtime=0.1)
            self.mp.do_send_keys(MainPage.NEW_ART_FORM.ARTICLE_TAG_FIELD, ';'.join(tags), wtime=0.1)
            self.mp.do_click(MainPage.NEW_ART_FORM.ARTICLE_PUBLISH_BUTTON, wtime=0.1)
            self.mp.get_url('articles', wtime=1)
        except BaseException:
            self.mp.log_error('Inserting new article failed.')
            assert False
        else:
            assert True
        return None

    def __in_pop_tags(self, text):
        try:
            self.mp.do_click(MainPage.NAV_BAR.HOME_BUTTON, wtime=1)
        except:
            assert False

        pop_tags = self.mp.get_elements(MainPage.HOME.POPULAR_TAGS, wtime=0.3)
        in_tags = False
        for tag in pop_tags:
            if MainPage.get_element_text_on_webelement(tag) == text:
                in_tags = True
                break
        return in_tags

    def __delete_article_by_title(self, title):
        self.mp.do_click(MainPage.NAV_BAR.HOME_BUTTON, wtime=1)
        in_article = False
        pages = self.mp.get_elements(MainPage.HOME.PAGES, wtime=0.5)
        article_found = None
        for page in pages:
            MainPage.do_click_on_webelement(page)
            article_titles = self.mp.get_elements(MainPage.HOME.ARTICLES_TITLES, wtime=0.2)
            for art in article_titles:
                if MainPage.get_element_text_on_webelement(art) == title:
                    in_article = True
                    article_found = art
                    break
            if in_article:
                break
        MainPage.do_click_on_webelement(article_found)
        self.mp.do_click(MainPage.EDT_ART_FORM.DELETE_BUTTON, wtime=1)
        return in_article

    def test_tc_01(self):
        """Regisztráció"""
        self.__register(self.data_for_test.REG_USER)  # register a new  user, asserts inserted
        assert not self.mp.get_element(MainPage.NAV_BAR.LOGOUT_BUTTON, wtime=3)  # there is no 'Log out' button
        self.__login(self.data_for_test.REG_USER)  # login with the new, asserts inserted
        assert self.mp.get_element(MainPage.NAV_BAR.LOGOUT_BUTTON, wtime=3)  # there is 'Log out' button
        self.__logout()
        return None

    def test_tc_02(self):
        """Bejelentkezés"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        assert self.mp.get_element(MainPage.NAV_BAR.LOGOUT_BUTTON, wtime=3)  # there is 'Log out' button
        self.__logout()
        return None

    def test_tc_03(self):
        """Adatkezelési nyilatkozat használata"""
        self.mp.go()
        assert self.mp.get_element(MainPage.HOME.ACCEPT_LINK, wtime=1)  # accept link reachable
        self.mp.do_click(MainPage.HOME.ACCEPT_LINK, wtime=1)
        assert not self.mp.get_element(MainPage.HOME.ACCEPT_LINK, wtime=1)  # accept link not reachable
        return None

    def test_tc_04(self):
        """Adatok listázása"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        article_links = []
        try:
            pages = self.mp.get_elements(MainPage.HOME.PAGES, wtime=2)
            assert len(pages) > 0
            for page in pages:
                MainPage.do_click_on_webelement(page)
                article_titles = self.mp.get_elements(MainPage.HOME.ARTICLES_LINKS, wtime=0.1)
                for art in article_titles:
                    article_links.append(MainPage.get_attribute_on_webelement(art, 'href'))
        except:
            assert False
        else:
            assert True
        assert len(article_links) > 0  # there is an article at least
        with open(self.data_for_test.OUT_FILE_ARTICLE_LINKS, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(['Rank', 'Link'])
            for index, link in enumerate(article_links):
                spamwriter.writerow([index + 1, link])

        self.__logout()
        return None

    def test_tc_05(self):
        """Több oldalas lista bejárása"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        page_num = 0
        try:
            pages = self.mp.get_elements(MainPage.HOME.PAGES, wtime=1)
            for page in pages:
                MainPage.do_click_on_webelement(page)
                page_num += 1
        except:
            assert False
        else:
            assert True

        assert page_num > 0  # at least one page
        self.__logout()
        return None

    def test_tc_06(self):
        """Új adat bevitel"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        self.__new_article(self.data_for_test.UNIQUE_ARTICLE_WITH_COMMENTS['title'],
                           self.data_for_test.UNIQUE_ARTICLE_WITH_COMMENTS['about'],
                           self.data_for_test.UNIQUE_ARTICLE_WITH_COMMENTS['body'],
                           self.data_for_test.UNIQUE_ARTICLE_WITH_COMMENTS['tag'])  # asserts inserted
        try:
            # post a lot of comments (3)
            i = 0
            for comment in self.data_for_test.UNIQUE_ARTICLE_WITH_COMMENTS['comments']:
                self.mp.do_send_keys(MainPage.EDT_ART_FORM.COMMENT_TEXTAREA, comment, wtime=0.1)
                self.mp.do_click(MainPage.EDT_ART_FORM.POST_BUTTON, wtime=0.1)
                i += 1
        except:
            assert False
        else:
            assert True
        assert i > 0 and len(self.data_for_test.UNIQUE_ARTICLE_WITH_COMMENTS['comments']) == i
        self.__logout()
        return None

    def test_tc_07(self):
        """Ismételt és sorozatos adatbevitel adatforrásból"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        j = 1
        try:
            for i in self.data_for_test.ARTICLE_TEST_DATA.index:
                # store new articles up to ARTICLE_TEST_DATA_MAX_NUM
                if j <= self.data_for_test.ARTICLE_TEST_DATA_MAX_NUM:
                    title, about, body, tag1, tag2, tag3 = self.data_for_test.ARTICLE_TEST_DATA.iloc[i]
                    self.__new_article(title, about, body, tag1, tag2, tag3)
                    j += 1
        except:
            assert False
        else:
            assert True
        assert j > self.data_for_test.ARTICLE_TEST_DATA_MAX_NUM  # j new articles stored
        self.__logout()
        return None

    def test_tc_08(self):
        """Meglévő adat módosítás"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        self.mp.do_click(MainPage.NAV_BAR.SETTINGS_BUTTON, wtime=1)
        self.mp.get_url('settings', wtime=2)
        self.mp.do_send_keys(MainPage.SETTINGS_FORM.SHORTBIO_TEXTAREA, self.data_for_test.SETTINGS_SHORT_BIO, wtime=0.1)
        self.mp.do_click(MainPage.SETTINGS_FORM.UPDATE_SETTINGS_BUTTON, wtime=0.1)
        self.mp.do_click(MainPage.SETTINGS_FORM.UPDATE_SUCCESS_OK_BUTTON, wtime=0.1)
        self.mp.do_click(MainPage.NAV_BAR.HOME_BUTTON, wtime=0.1)
        self.mp.do_click(MainPage.NAV_BAR.SETTINGS_BUTTON, wtime=0.1)
        self.mp.get_url('settings', wtime=1)
        assert self.data_for_test.SETTINGS_SHORT_BIO == self.mp.get_element_attribute(
            MainPage.SETTINGS_FORM.SHORTBIO_TEXTAREA,
            'value', wtime=0.3)
        self.__logout()
        return None

    def test_tc_09(self):
        """Adat vagy adatok törlése"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        self.__new_article(self.data_for_test.UNIQUE_ARTICLE['title'],
                           self.data_for_test.UNIQUE_ARTICLE['about'],
                           self.data_for_test.UNIQUE_ARTICLE['body'],
                           self.data_for_test.UNIQUE_ARTICLE['tag'])
        assert self.__in_pop_tags(self.data_for_test.UNIQUE_ARTICLE['tag'])
        assert self.__delete_article_by_title(self.data_for_test.UNIQUE_ARTICLE['title'])
        assert not self.__in_pop_tags(self.data_for_test.UNIQUE_ARTICLE['tag'])
        self.__logout()
        return None

    def test_tc_10(self):
        """Adatok lementése felületről"""
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted

        pop_tags = self.mp.get_elements(self.mp.HOME.POPULAR_TAGS, wtime=0.2)
        with open(self.data_for_test.OUT_FILE_POPULAR_TAGS, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(['Rank', 'Popular_tag'])
            for index, tag in enumerate(pop_tags):
                spamwriter.writerow([index + 1, MainPage.get_element_text_on_webelement(tag)])

        pt_csv = pd.read_csv(self.data_for_test.OUT_FILE_POPULAR_TAGS)
        assert len(pop_tags) == len(pt_csv.index)
        self.__logout()
        return None

    def test_tc_11(self):
        """Kijelentkezés"""
        assert not self.mp.get_element(MainPage.NAV_BAR.LOGOUT_BUTTON, wtime=3)  # there is no 'Log out' button
        self.__login(self.data_for_test.GEN_USER)  # login, asserts inserted
        assert self.mp.get_element(MainPage.NAV_BAR.LOGOUT_BUTTON, wtime=3)  # there is 'Log out' button
        self.__logout()
        assert not self.mp.get_element(MainPage.NAV_BAR.LOGOUT_BUTTON, wtime=3)  # there is no 'Log out' button
        return None
