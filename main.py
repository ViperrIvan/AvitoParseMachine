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

class ParserRoot(BoxLayout):
    results_text = StringProperty("Здесь будут результаты парсинга")
    is_parsing = BooleanProperty(False)

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
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "button"))).click()
            WebDriverWait(driver, 5)
            html = driver.page_source
            driver.quit()

            way_to_name = "html > body > div > div > buyer-pages-mfe-location > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > p > a"
            way_to_price = "html > body > div > div > buyer-pages-mfe-location > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > span > div > div > p > strong > span"

            soup = BeautifulSoup(html, 'html.parser')
            names = soup.select(way_to_name)

            results = []

            prices = soup.select(way_to_price)
            df = pd.DataFrame({"Name": [], "Price": []})
            for name, price in zip(names, prices):
                results.append(name)
                results.append(price)


            self._show_results(results)

        except Exception as e:
            self.results_text = f"Ошибка: {str(e)}"
        finally:
            self.is_parsing = False

    def _show_results(self, results):
        if not results:
            self.results_text = "Ничего не найдено"
            return

        formatted = "\n".join(
            f"{i}. {results[i-1].text}\n   {results[i].text}"
            for i in range(1, len(results), 2)
        )
        self.results_text = formatted


class ParserApp(App):

    def build(self):
        self.title = "AvitoParseMachine"
        Config.set('kivy', 'window_icon', 'C:/Users/IVD/PycharmProjects/PythonProject7/pumpkin.ico')
        return ParserRoot()


if __name__ == '__main__':
    ParserApp().run()
