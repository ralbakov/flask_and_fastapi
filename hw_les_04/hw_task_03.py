'''
Используется асинхронный подход
'''

import os
import asyncio
import aiohttp
import time
import argparse

parser = argparse.ArgumentParser(description='Input url')
parser.add_argument(
    '--url',
    nargs='+',
    type=str,
    default=["https://img2.akspic.ru/attachments/originals/8/4/6/5/7/175648-vektornaya_grafika-illustracia-grafika-vektor-dizajn-7680x4320.png",
        "https://img2.akspic.ru/attachments/originals/7/8/4/1/7/171487-smertelnyj_udar_zaka_snajdera-detstrouk-dik_grejson-betmen-darksajd-7680x4320.jpg",
        "https://img2.akspic.ru/attachments/originals/8/6/4/5/7/175468-seealpsee-gora-oblako-rastenie-zelenyj-8170x5338.jpg",
        "https://img2.akspic.ru/attachments/originals/7/6/4/5/7/175467-anime-izuku_midoriya-vse_vozmozhno-moj_geroj_akademii-anime_art-7680x4800.jpg",
        "https://img3.akspic.ru/attachments/originals/8/9/7/4/7/174798-harlej_devidson-motocikl-harli-harley_davidson_sportster-harley_davidson_fat_boy-10000x6672.jpg",
        "https://img3.akspic.ru/attachments/originals/5/7/7/3/7/173775-zima-alpy-franciya-kanada-gora-7927x5288.jpg"
       ],
    help='enter url address')
args = parser.parse_args()
urls = args.url

async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            file_name = os.path.basename(url)
            with open(file_name, 'wb') as file:
                file.write(await response.read())
            print(f"Время загрузки файла {file_name} -- {time.time()-start_time:.2f} секунд")

async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_file(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
start_time = time.time()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f'Общее время выполнения всех загрузок {time.time()-start_time:.2f} секунд')