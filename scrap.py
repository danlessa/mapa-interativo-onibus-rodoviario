# %%

import requests as req
from bs4 import BeautifulSoup
from collections import defaultdict
from tqdm.auto import tqdm

# %%

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example'  # This is another valid field
}


URI_CITIES = 'https://deonibus.com/onibus-para'
SELECTOR_CITIES = ".tab-content > article > article.section-stations > a"
r = req.get(URI_CITIES, headers=headers)
soup = BeautifulSoup(r.content, features="html.parser")
cities_el = soup.select(SELECTOR_CITIES)


cities_slugs = {}

for city_el in cities_el:
    city_uri = city_el.attrs['href']
    city_slug = city_uri.split("/")[-1]
    # uf = city_uri.split("-")[-1].upper()
    name = city_el.text.strip() + f" / {uf}"
    cities_slugs[name] = city_slug
# %%
SELECTOR_DEPARTING = "#section-portfolio-routes > div.routes.leaving > a"
SELECTOR_ARRIVING = "#section-portfolio-routes > div.routes.arriving > a"
URI_CITY = "https://deonibus.com/onibus-para/{city_slug}"

cities_arrivals = defaultdict(list)
cities_departures = defaultdict(list)
for city, city_slug in tqdm(cities_slugs.items()):
    uri = URI_CITY.format(city_slug=city_slug)
    r = req.get(uri, headers=headers)
    soup = BeautifulSoup(r.content, features="html.parser")
    arrivals_el = soup.select(SELECTOR_ARRIVING)
    for el in arrivals_el:
        slug = el.attrs['href'].split("/")[-1].split("-para-")[0]
        cities_arrivals[city_slug].append(slug)

    departures_el = soup.select(SELECTOR_DEPARTING)
    for el in departures_el:
        slug = el.attrs['href'].split("/")[-1].split("-para-")[-1]
        cities_departures[city_slug].append(slug)
# %%
