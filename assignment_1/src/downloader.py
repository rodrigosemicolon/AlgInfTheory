# -*- coding: utf-8 -*-

# Sergei Bugrov
# 7-9-17
#
# Downloads all available books in English language in .txt format from http://www.gutenberg.org,
# unpacks them from .zip archives, saves them to ../books/ folder, and deletes .zip files.
#
# usage : python gutenberg.py
#
# python version : 3.6.1

import requests, os, errno, zipfile, glob, shutil
from urllib.request import urlretrieve

from src.language import DEF_REFERENCE_PATH


def main(lang):
    if not os.path.exists('../example/books'):
        try:
            os.makedirs('../example/books/')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    if not os.path.exists('../example/books/' + lang):
        try:
            os.makedirs('../example/books/' + lang)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    n_books = 20  # numero de livros
    count = 0
    # STEP 1. BUILD A LIST OF URLS
    urls_to_books = []
    if not os.path.exists('..example/urls_to_books.txt'):
        page_w_books_url = 'http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=' + lang
        while 1 == 1:
            is_last_page = False
            print('Reading page: ' + page_w_books_url)
            page_w_books = requests.get(page_w_books_url, timeout=20.0)

            if page_w_books:
                urls = []
                content = str(page_w_books.content)
                while content.find('"http://aleph.gutenberg.org/') != -1:
                    count += 1

                    start = content.find('"http://aleph.gutenberg.org/')
                    urls.append(content[start + 1:content.find('"', start + 1)])
                    content = content.replace(content[start + 1:content.find('"', start + 1)], "")
                    if count == n_books:
                        break
                    # page_w_books = bs4.BeautifulSoup(page_w_books.text, "lxml")
                    # urls = [el.get('href') for el in page_w_books.select('body > p > a[href^="http://aleph.gutenberg.org/"')]
                # url_to_next_page = page_w_books.find_all('a', string='Next Page')
                url_to_next_page = content[content.find("harvest?offset="):content.find('"', content.find("harvest?offset=") + 1)].replace("amp;", "")
                if len(urls) > 0:
                    urls_to_books.append(urls)

                    if url_to_next_page:
                        page_w_books_url = "http://www.gutenberg.org/robot/" + url_to_next_page
                else:
                    is_last_page = True

            if is_last_page:
                break
            if count == n_books:
                break

        urls_to_books = [item for sublist in urls_to_books for item in sublist]

        # Backing up the list of URLs
        with open('../example/urls_to_books.txt', 'w') as output:
            for u in urls_to_books:
                output.write('%s\n' % u)

    # STEP 2. DOWNLOAD BOOKS

    # If, at some point, Step 2 is interrupted due to unforeseen
    # circumstances (power outage, lost of internet connection), replace the number
    # (value of the variable url_num) below with the one you will find in the logfile.log
    # Example
    #       logfile.log : Unzipping file #99 books/10020.zip
    #       the number  : 99
    url_num = 0

    if os.path.exists('../example/urls_to_books.txt') and len(urls_to_books) == 0:
        with open('../example/urls_to_books.txt', 'r') as f:
            urls_to_books = f.read().splitlines()

    for url in urls_to_books[url_num:]:

        dst = '../example/books/' + lang + "/" + url.split('/')[-1].split('.')[0].split('-')[0]

        with open('../example/logfile.log', 'w') as f:
            f.write('Unzipping file #' + str(url_num) + ' ' + dst + '.zip' + '\n')

        if len(glob.glob(dst + '*')) == 0:
            urlretrieve(url, dst + '.zip')

            with zipfile.ZipFile(dst + '.zip', "r") as zip_ref:
                try:
                    zip_ref.extractall("../example/books/" + lang + "/")
                    # print(dst)
                    print(os.listdir("../example/books/" + lang + "/"))
                    print(str(url_num) + ' ' + dst + '.zip ' + 'unzipped successfully!')
                except NotImplementedError:
                    print(str(url_num) + ' Cannot unzip file:', dst)

            os.remove(dst + '.zip')
            for qwerty in os.listdir("../example/books/" + lang + "/"):
                print(qwerty, qwerty[-4:])
                if os.path.isdir("../example/books/" + lang + "/" + qwerty):
                    shutil.rmtree("../example/books/" + lang + "/" + qwerty)
                elif qwerty[-4:] != ".txt":
                    os.remove("../example/books/" + lang + "/" + qwerty)

        url_num += 1


def get_file_encoding(filename):
    with open(filename, "r", errors="ignore") as book:
        text = book.read()
        # print(text)
        """
        for item in text:
            if "encoding:" in item:

                encoding.append(item.split("\b"))
        """
        line = re.findall(".*encoding:.+\n", text)[0]
        print(line)
        encoding = re.split(": ", str(line))
        print(encoding[-1])
        return encoding[-1].strip()


import re


def change_encoding(filename):
    lang = filename.split("/")[0]
    if not os.path.exists('../example/c_books'):
        try:
            os.makedirs('../example/c_books/')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    if not os.path.exists('../example/c_books/' + lang):
        try:
            os.makedirs('../example/c_books/' + lang)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    filepath = "../example/books/" + filename
    filepath2 = "../example/c_books/" + filename
    enc = get_file_encoding(filepath)
    # print("we got this ",enc)
    if not "US-ASCII" in enc and not "Windows" in enc and not "windows" in enc and not "ISO" in enc and not "iso" in enc:
        enc = enc.replace("-", "")
    if enc == "ISO Latin-1":
        enc = "iso-8859-1"
    if enc == "UTF16":
        enc = "UTF-8"
    # print(filepath)
    # print(enc)
    print(filepath, "\n", enc)
    with open(filepath, "r", encoding=enc.lower()) as pls:
        content = pls.read()
        with open(filepath2, "w", encoding="utf-8") as testwrite:
            testwrite.write(content)


BOOKS_PATH = "../example/books/"
BOOKS_PATH2 = "../example/books2/"


def convert_all_files():
    for f in os.walk(BOOKS_PATH):
        if f[0][len(f[0]) - 1] != "/":
            lang = f[0][len(f[0]) - 2:]
            for f2 in os.walk(BOOKS_PATH + lang + "/"):
                # print(f2)
                book_list = f2[2:]

                # print(book_list)
                content = ""
                for book in book_list[0]:
                    # print(lang,book)
                    change_encoding(lang + "/" + book)

                    # enc = get_file_encoding(f[0] + "/" + book)
                    # print("we got this ",enc)
                    # if not "US-ASCII" in enc and not "Windows" in enc and not "windows" in enc and not "ISO" in enc and not "iso" in enc:
                    #     enc = enc.replace("-", "")
                    # if enc == "ISO Latin-1":
                    #     enc = "iso-8859-1"
                    # if enc == "UTF16":
                    #     enc = "UTF-8"
                    with open("../example/c_books/" + lang + "/" + book, "r", encoding="utf-8") as book:
                        text = book.read()

                        text = text[text.find("START OF THIS PROJECT"):]
                        text = text[text.find("***")+3 :]

                        text = text[:text.find("***") -3]
                    content+=text
                with open(DEF_REFERENCE_PATH + lang + ".txt", "w", encoding="utf-8") as concatenated_book:
                    concatenated_book.write(content)

            # print(lang)
    return 0  # dicts


if __name__ == '__main__':
    """
    The main function is called when gutenberg.py is run from the command line
    """
    # id="fr/10061-8"
    # change_encoding(id)
    # convert_all_files()
    # lan_list=['af','cs','da','de','el','en','es','fi','fr','it','ja','no','pl','pt','ro','ru','sl']
    # for lan in lan_list:
    #     main(lan)
    # main("en")
    convert_all_files()
    # main("el")
