from argparse import ArgumentParser
import os
import pandas as pd
import numpy as np
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from utils import convert_to_matrix

ap = ArgumentParser()
ap.add_argument('data', help='Path to input data spreadsheet')
ap.add_argument('output', help='Path to save output images to')
ap.add_argument('hemisphere', help='Which hemisphere to generate images for', choices=['northern', 'southern'])
args = ap.parse_args()

if not os.path.exists(args.output):
    os.makedirs(args.output)

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.maximize_window()

for entity_type in ['Insects', 'Fish', 'Sea Creatures']:
    df = pd.read_excel(args.data, sheet_name=entity_type)
    ids = df['Unique Entry ID'].tolist()
    if args.hemisphere == 'northern':
        avs = df[[c for c in df.columns if c[:2] == 'NH']].values
    else:
        avs = df[[c for c in df.columns if c[:2] == 'SH']].values

    for id_, av in tqdm(zip(ids, avs), total=len(avs), desc=f'Generating {entity_type.lower()} assets'):
        mask = np.array(convert_to_matrix(av)).ravel()

        with open('index.html') as f:
            html_file = f.read()
            soup = bs4.BeautifulSoup(html_file, 'lxml')

        items = soup.find_all('td', {'class': 'item'})

        for ix, m in enumerate(mask):
            if m == 1:
                items[ix]['class'].append('active')

        html = soup.prettify(soup.original_encoding)
        with open('edited.html', 'w') as f:
            f.write(html)

        driver.get(f'file://{os.getcwd()}/edited.html')
        element = driver.find_element_by_tag_name('tbody')
        element.screenshot(f'{args.output}/{id_}.png')

os.remove('edited.html')
driver.quit()
