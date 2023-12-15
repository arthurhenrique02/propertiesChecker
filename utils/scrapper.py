import datetime
import logging
import shutil
import uuid
from pathlib import Path

import pandas as pd
from celery import shared_task
from selenium.webdriver.common.by import By

from utils import browser

from .save_changes import save_changes_on_db
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
    rand_uuid = str(uuid.uuid4())

    # rename file and move to project folder (file folder)
    shutil.move(
        f"{DOWNLOAD_DIR}\\Lista_imoveis_PB.csv",
        f"{FILES_DIR}\\{today.strftime("%Y-%m-%d").replace("-", "_")}.csv",
    ).encode("utf-8")

    # check if file was moved
    file_moved: bool = wait_download_or_move(
        base_path=FILES_DIR,
        file_name=f"{today.strftime('%Y-%m-%d').replace('-', '_')}.csv",
    )

    if not file_moved:
        logging.error("Não possivel mover o arquivo")
        return

    # compare_files
    compare_and_update_files.delay()


@shared_task
def compare_and_update_files():
    # get curr date
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    # try to read in different encodings
    for encoding in ["utf-8", "latin-1", "utf-16"]:
        try:
            # read file and file from a day before
            todays_file = pd.read_csv(
                f"{FILES_DIR}\\{(today).strftime('%Y-%m-%d').replace('-', '_')}.csv",
                encoding=encoding,
                sep=";",
                on_bad_lines="skip",
                header=1,
            )
            yesterdays_file = pd.read_csv(
                f"{FILES_DIR}\\{yesterday.strftime('%Y-%m-%d').replace('-', '_')}.csv",
                encoding=encoding,
                sep=";",
                on_bad_lines="skip",
                header=1,
            )
            break
        except UnicodeDecodeError:
            logging.error(f"Não foi possível ler o arquivo com o encoding {encoding}")
            continue

    # merge only different cells
    merged_csv = pd.merge(
        # sort values to avoid errors
        yesterdays_file.sort_values(by=[" N° do imóvel"]),
        todays_file.sort_values(by=[" N° do imóvel"]),
        # on=[" N° do imóvel", "Preço", "Valor de avaliação", "Desconto"],
        how="outer",
        indicator=True,
    ).drop_duplicates(keep=False)

    # get differences
    diffs = merged_csv[merged_csv["_merge"] == "right_only"]

    # check if there is any difference
    if diffs.empty:
        logging.info("Nenhuma alteração no arquivo")
        return

    # check all changes
    for index, row in diffs.iterrows():
        # row data
        data = {}
        msg = []
        for col in diffs.columns:
            # initialize var
            try:
                # try to get and y column
                x_col = row[col + "_x"]
                y_col = row[col + "_y"]

                if x_col != y_col:
                    msg.append(f"{today.strftime('%d/%m/%Y, %H:%M')} - "
                               f"{col} alterada: Valor antigo = {row[col + '_x']}; "
                               f"Novo valor = {row[col + '_y']}")

                    # save the changed value
                    data[col.strip()] = row[col + "_y"]

            except KeyError:
                # just add the col
                data[col.strip()] = row[col]

            # remove _merge key
            data.pop("_merge", None)

        # check if msg dont exists
        if not msg:
            msg.append(f"{today.strftime('%d/%m/%Y, %H:%M')} - "
                       f"Imóvel adicionado")

        # save on db after all changes
        save_changes_on_db(data, msg)
