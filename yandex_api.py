import sys
import time

import pyautogui
from bs4 import BeautifulSoup

import requests

import pyperclip
import keyboard as key

import pandas as pd

df = pd.read_csv('poi.csv', delimiter='|')


def get_comments(id: str) -> tuple[float, int, int]:
    response = requests.get(f"https://yandex.ru/maps-reviews-widget/{id}?comments")
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.body

    m = 0.0
    com_amount = 0
    rev_amount = 0
    try:
        m = float(body.p.string.replace(",", "."))
        amount_str = soup.find_all("a", {"class": "mini-badge__rating"})[0].string
        com_amount, rev_amount = [x.split()[0] for x in amount_str.split(" • ")]
    except Exception as e_:
        pass
    return m, com_amount if isinstance(com_amount, int) else 0, rev_amount if isinstance(rev_amount, int) else 0


def address_to_id(address: str):
    pyperclip.copy(address)
    pyautogui.click(115, 133)

    key.press('ctrl+a')
    key.release('ctrl+a')
    key.press('ctrl')
    key.press('v')
    key.release('ctrl')
    key.release('v')
    key.press('enter')
    key.release('enter')
    time.sleep(1)
    pyautogui.click(54, 360)
    time.sleep(0.3)
    pyautogui.click(952, 702)
    time.sleep(0.3)
    pyperclip.copy('document.getElementsByClassName("card-title-view__title-link")[0].getAttribute("href");')
    time.sleep(0.2)
    key.press('ctrl')
    key.press('v')
    key.release('ctrl')
    key.release('v')
    time.sleep(0.7)
    key.send("enter")

    time.sleep(0.7)
    pyautogui.tripleClick(1023, 706)
    key.press('ctrl+c')
    key.release('ctrl+c')
    time.sleep(0.3)
    print(pyperclip.paste())
    if "/" in str(pyperclip.paste()):
        return str(pyperclip.paste()).split("/")[-2]
    else:
        return None


file = open("results.txt", "a")

for index, v in df.iterrows():
    if int(index) > 210\
            :
        try:
            request_row = v['name'].replace(",", "") + " " + v['address_name']
            print(request_row)
            if v['address_name'] == "Нет" or v['address_comment'] == "Нет" or not int(v['lat']) or not int(v['lon']):
                print("skip")
            else:
                y_id = address_to_id(request_row)
                if y_id:
                    mean, comments_amount, review_amount = get_comments(y_id)
                    file.write(str([index, v['id'], y_id, mean, comments_amount, review_amount]) + '\n')
        except Exception as e:
            print(e)
        finally:
            key.press('ctrl+l')
            key.release('ctrl+l')

# 355 275
#
# while True:
#     x, y = pyautogui.position()
#     print(x, y)
