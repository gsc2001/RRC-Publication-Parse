#!/usr/bin/env python
"""
    :brief: Custom parser to create yml files for all the publications of a particular year
    :author: gsc2001
"""

import argparse
import requests
import yaml
from bs4 import BeautifulSoup

url = 'https://robotics.iiit.ac.in/publications.html'


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', '-y', type=str, required=True, help='Year for which yml needs to be created')
    args = parser.parse_args()
    return args


def get_html() -> str:
    res = requests.get(url)
    return res.text


def main():
    args = get_args()
    html_string = get_html()

    soup = BeautifulSoup(html_string, 'html.parser')
    container = soup.find_all('div', class_='container')[1]
    row = container.find_all('div', class_='row')[1]
    headings = row.find_all('h3')[1:]
    ols = row.find_all('ol')
    years = list(map(lambda h: h.text, headings))
    try:
        index = years.index(args.year)
    except AttributeError:
        print('Invalid Year')
        raise SystemExit(1)

    ol = ols[index]

    lis = ol.find_all('li')

    publications = []
    for li in lis:
        title = li.strong.string.strip(' ')
        authors = li.strong.next_element.next_element.strip(' ')
        venue = li.em.string.strip(' ')
        publication = {'title': title, 'authors': authors, 'venue': venue}
        if li.a is not None:
            if li.a.img is not None:
                publication.update({'link': {'display': li.a.img.get('alt'), 'url': li.a.get('href')}})
            else:
                publication.update({'link': {'url': li.a.get('href')}})
        publications.append(publication)

    print(yaml.dump(publications))


if __name__ == '__main__':
    main()
