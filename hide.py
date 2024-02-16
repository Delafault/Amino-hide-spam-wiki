from aminofix import Client, SubClient, exceptions
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import os

os.system('cls' if os.name == 'nt' else 'clear')

print("""
█░█ █ █▀▄ █▀▀   █░█░█ █ █▄▀ █ █▀|ᵇʸ ᵈᵉˡᵃᶠᵃᵘˡᵗ
█▀█ █ █▄▀ ██▄   ▀▄▀▄▀ █ █░█ █ ▄█
""")

n = 0

def gd_print(value):
    green_color = '\033[32m'
    reset_color = '\033[0m'
    result = f"\n>{green_color} {value} {reset_color}\n"
    print(result)

def bd_print(value):
    red_color = '\033[31m'
    reset_color = '\033[0m'
    result = f"\n>{red_color} {value} {reset_color}\n"
    print(result)

def hide_wiki(sub_clientz, wiki, n):
    try:
        sub_clientz.hide(wikiId=wiki, reason="Чистка ленты от спама wiki постами")
        gd_print(f"Скрыли вики: {wiki} | №{n}")

    except exceptions.IpTemporaryBan:
        bd_print("Ошибка: вас забанили по ip. Скрипт продолжит работу через 360 секунд")
        sleep(360)
    except Exception as error:
        bd_print(f"Ошибка при скрытии вики {wiki}: {error}")

def main():
    global n
    s = 0
    while True:
        try:
            clientz = Client()
            clientz.login(email = input("E-mail: "), password = input("пароль: "))
            gd_print(f"Вошли в аккаунт '{clientz.profile.nickname}'")
            break
        except Exception as error:
            bd_print(f"Ошибка: {error}")

    while True:
        try:
            user_link = clientz.get_from_code(input("Ссылка на пользователя: "))
            comId = user_link.comId
            userId = user_link.objectId
            sub_clientz = SubClient(comId = comId, profile = clientz.profile)
            gd_print(f"Получили информацию о пользователе '{sub_clientz.get_user_info(userId).nickname}'")
            break
        except Exception as error:
            bd_print(f"Ошибка: {error}")

    executor = ThreadPoolExecutor(max_workers = 10)
    processed_wikis = set()

    while True:
        try:
            ww = sub_clientz.get_user_wikis(userId, s, 100)
            wikis_count = len(ww.wikiId)
            if wikis_count == 0:
                break
            futures = []
            for wiki in ww.wikiId:
                if wiki not in processed_wikis:
                    n += 1
                    future = executor.submit(hide_wiki, sub_clientz, wiki, n)
                    futures.append(future)
                    processed_wikis.add(wiki)
            for future in futures:
                future.result()
            s += wikis_count

        except exceptions.IpTemporaryBan:
            bd_print("Ошибка: вас забанили по ip. Скрипт продолжит работу через 360 секунд")
            sleep(360)
        except exceptions.AccountLimitReached or exceptions.TooManyRequests:
            bd_print("Ошибка: Слишком много запросов. Скрипт остановлен")
            exit()
        except Exception as error:
            bd_print(f"Ошибка: {error}")





if __name__ == '__main__':
    main()
    print("---")
    print()
    gd_print(f"Скрипт завершил свою работу! Было скрыто wiki: {n}")
