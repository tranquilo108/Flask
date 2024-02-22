import re
import threading
import requests
import asyncio
import lxml
import aiohttp
from multiprocessing import Pool, Process
from bs4 import BeautifulSoup

all_links = []


def get_pages():
    pages = []
    flag = True
    count = 1
    while flag:
        link = f'https://books.toscrape.com/catalogue/page-{count}.html'
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'lxml')
        next = soup.find('li', class_='next')
        if next:
            count += 1
        else:
            flag = False
        pages.append(link)
    return pages


def get_all_links(page):
    global all_links

    r = requests.get(page)
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.find_all('div', class_='image_container')
    threads = []

    for link in links:
        t = threading.Thread(target=asyncio.run(
            get_all_image_links(f"https://books.toscrape.com/catalogue/{link.find('a').get('href')}")),
            args=(f"https://books.toscrape.com/catalogue/{link.find('a').get('href')}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


async def get_all_image_links(url):
    coroutines = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find_all('h1')[-1].text
    title = re.sub(r'[^a-zA-Z0-9_-]', '', title)
    img = soup.find('div', id='product_gallery').find('img').get('src')
    c = asyncio.ensure_future(download(name=title, url=f'https://books.toscrape.com/{img.replace("../../", " ")}'))
    coroutines.append(c)
    await asyncio.gather(*coroutines)


async def download(url, name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            img = await response.read()
            with open(f'images/{name}.{url.split(".")[-1]}', 'wb') as f:
                f.write(img)


def main():
    pages = get_pages()
    processes = []
    for page in pages:
        p = Process(target=get_all_links, args=(page,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main()
