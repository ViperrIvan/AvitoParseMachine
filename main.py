from abc import ABC, abstractmethod
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from kivy.config import Config
from typing import List, Dict

# Абстракции (интерфейсы)
class IParser(ABC):
    @abstractmethod
    def parse(self, url: str) -> List[Dict[str, str]]:
        pass

class IDataHandler(ABC):
    @abstractmethod
    def save(self, data: List[Dict[str, str]], filename: str) -> None:
        pass
    
    @abstractmethod
    def format(self, data: List[Dict[str, str]]) -> str:
        pass

class IWebDriverFactory(ABC):
    @abstractmethod
    def create_driver(self):
        pass

# Реализации
class ChromeDriverFactory(IWebDriverFactory):
    def create_driver(self):
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(options=options)

class AvitoParser(IParser):
    def __init__(self, driver_factory: IWebDriverFactory):
        self.driver_factory = driver_factory
        self._selectors = {
            'name': "html > body > div > div > buyer-pages-mfe-location > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > h2 > a",
            'price': "html > body > div > div > buyer-pages-mfe-location > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > span > div > div > p > strong > span",
            'popup1': "styles-module-root-EEwdX.styles-module-root_size_s-_OIDv.styles-module-root_preset_overlay-_8Li4",
            'popup2': "styles-module-root-YyvDu"
        }

    def parse(self, url: str) -> List[Dict[str, str]]:
        driver = self.driver_factory.create_driver()
        try:
            driver.get(url)
            self._handle_popups(driver)
            return self._extract_data(driver.page_source)
        finally:
            driver.quit()

    def _handle_popups(self, driver):
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, self._selectors['popup1']))).click()
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, self._selectors['popup2']))).click()

    def _extract_data(self, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, 'html.parser')
        names = soup.select(self._selectors['name'])
        prices = soup.select(self._selectors['price'])

        return [{
            'Name': name.text,
            'Price': price.text,
            'Url': f"https://www.avito.ru/{name['href']}"
        } for name, price in zip(names, prices)]

class ExcelDataHandler(IDataHandler):
    def save(self, data: List[Dict[str, str]], filename: str = 'results.xlsx') -> None:
        pd.DataFrame(data).to_excel(filename, sheet_name='Results', index=False)

    def format(self, data: List[Dict[str, str]]) -> str:
        if not data:
            return "Ничего не найдено"
        return "\n".join(
            f"{i}. {item['Name']}\n{item['Price']}\n{item['Url']}"
            for i, item in enumerate(data, 1)
        )

# UI Component
class ParserRoot(BoxLayout):
    results_text = StringProperty("Здесь будут результаты парсинга")
    is_parsing = BooleanProperty(False)

    def __init__(self, parser: IParser, data_handler: IDataHandler, **kwargs):
        super().__init__(**kwargs)
        self._parser = parser
        self._data_handler = data_handler

    def start_parsing(self):
        if self.is_parsing:
            return

        url = self.ids.url_input.text.strip()
        if not url:
            self.results_text = "Заполните все поля"
            return

        self.is_parsing = True
        self.results_text = "Парсинг начат..."

        try:
            data = self._parser.parse(url)
            self.results_text = self._data_handler.format(data)
            self._data_handler.save(data)
        except Exception as e:
            self.results_text = f"Ошибка: {str(e)}"
        finally:
            self.is_parsing = False

# App
class ParserApp(App):
    def build(self):
        self.title = "AvitoParseMachine"
        Config.set('kivy', 'window_icon', 'C:/Users/IVD/PycharmProjects/PythonProject7/pumpkin.ico')
        
        # Dependency Injection
        driver_factory = ChromeDriverFactory()
        parser = AvitoParser(driver_factory)
        data_handler = ExcelDataHandler()
        
        return ParserRoot(parser, data_handler)

if __name__ == '__main__':
    ParserApp().run()
