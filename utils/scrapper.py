from celery import shared_task
from selenium.webdriver.common.by import By

from utils import browser


@shared_task
def get_properties_list():
    # go to Caixa`s site
    browser.get("https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp")

    # download  Paraiba's properties list
    browser.find_element(by=By.ID, value="cmb_estado").send_keys("PB")
    browser.find_element(by=By.ID, value="btn_next1").click()
