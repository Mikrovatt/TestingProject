import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions


def pytest_addoption(parser) -> None:
    """ Функция для считывания параметров командной строки pytest """

    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='fr',
                     help="""Changing the browser language: ar, ca, cs, da, de, en-gb, el, 
                     es, fi, fr, it, ko, nl, pl , pt, pt-br, ro, ru, sk, uk, zh-hans, en """)


@pytest.fixture
def browser(request):
    """ Настройка среды окружения для запуска теста:
        1. Выбор браузера firefox или chrome, параметр browser_name
        2. Выбор языка для браузера, параметр language """

    # Список поддерживаемых языков на сайте
    languages = ['ar', 'ca', 'cs', 'da', 'de', 'en-gb', 'el', 'es', 'fi', 'fr', 'it',
                 'ko', 'nl', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sk', 'uk', 'zh-hans', 'en']

    browser_name = request.config.getoption("browser_name")
    language = request.config.getoption("language")
    browser = None

    # Проверка языка для браузера
    if language not in languages:
        raise pytest.UsageError(f"--language must be: {' '.join(languages)}")

    # Проверка выбора браузера
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        options = chromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': language})
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        options = firefoxOptions()
        options.set_preference('intl.accept_languages', language)
        browser = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser

    print("\nquit browser..")
    browser.quit()
