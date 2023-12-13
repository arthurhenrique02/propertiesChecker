import datetime
import logging
import shutil
from pathlib import Path

import pandas as pd
from celery import shared_task
from selenium.webdriver.common.by import By

from utils import browser

from .wait import wait_download_or_move

BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_DIR = f"{Path.home()}\\Downloads"
FILES_DIR = f"{BASE_DIR}\\files"


@shared_task
def download_and_move_properties_list():
    # go to Caixa`s site
    browser.get("https://venda-imoveis.caixa.gov.br/sistema/download-lista.asp")

    # download  Paraiba's properties list
    browser.find_element(by=By.ID, value="cmb_estado").send_keys("PB")
    browser.find_element(by=By.ID, value="btn_next1").click()

    # wait for file to be downloaded
    file_downloaded: bool = wait_download_or_move(DOWNLOAD_DIR, "Lista_imoveis_PB.csv")

    if not file_downloaded:
        logging.error("Não possível baixar o arquivo")
        return

    # get curr date
    today = datetime.datetime.now()

    # rename file and move to project folder (file folder)
    shutil.move(
        f"{DOWNLOAD_DIR}\\Lista_imoveis_PB.csv",
        f"{FILES_DIR}\\{today.strftime("%Y-%m-%d").replace("-", "_")}.csv",
    )

    # check if file was moved
    file_moved: bool = wait_download_or_move(
        base_path=FILES_DIR,
        file_name=f"{today.strftime('%Y-%m-%d').replace('-', '_')}.csv")

    if not file_moved:
        logging.error("Não possivel mover o arquivo")
        return

    # compare_files
    compare_files.delay()


@shared_task
def compare_files():
    # get curr date
    today = datetime.datetime.now()

    # try to read in different encodings
    for encoding in ["utf-8", "latin-1", "utf-16"]:
        try:

            # read file and file from a day before
            todays_file = pd.read_csv(
                f"{FILES_DIR}\\{today.strftime('%Y-%m-%d').replace('-', '_')}.csv",
                encoding=encoding,
                sep=';',
                on_bad_lines='skip'
            )
            yesterdays_file = pd.read_csv(
                f"{FILES_DIR}\\{(today - datetime.timedelta(days=1)).strftime('%Y-%m-%d').replace('-', '_')}.csv",
                encoding=encoding,
                sep=";",
                on_bad_lines='skip'
            )

            break
        except UnicodeDecodeError:
            logging.error(f"Não foi possível ler o arquivo com o encoding {encoding}")
            continue

    diff = pd.concat([todays_file, yesterdays_file]).drop_duplicates(keep=False)

    # TODO:
    # find a way to get the diff and save on mongodb
    # check if's empty
    if diff.empty:
        logging.info("Nenhuma alteração no arquivo")
        return
