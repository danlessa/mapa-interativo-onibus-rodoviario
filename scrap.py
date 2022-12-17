# %%

import requests as req
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

# %%

# Definitions

MAX_THREADS = 30

HEADERS = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example'  # This is another valid field
}

URI_CITIES = 'https://deonibus.com/onibus-para'
SELECTOR_CITIES = ".tab-content > article > article.section-stations > a"

URI_CITY = "https://deonibus.com/onibus-para/{city_slug}"
SELECTOR_DEPARTING = "#section-portfolio-routes > div.routes.leaving > a"
SELECTOR_ARRIVING = "#section-portfolio-routes > div.routes.arriving > a"

# %%

# Get all cities

r = req.get(URI_CITIES, headers=HEADERS)

if r.status_code == 200:
    soup = BeautifulSoup(r.content, features="html.parser")
    cities_el = soup.select(SELECTOR_CITIES)

    cities_slugs = [el.attrs['href'].split("/")[-1].strip().lower()
                    for el
                    in cities_el]
else:
    raise Exception(f"Error: non-code 200 ({r.status_code})")
# %%


def retrieve_city_connections(city_slug: str) -> tuple:
    city_arrivals = []
    city_departures = []
    code = None
    uri = URI_CITY.format(city_slug=city_slug)
    r = req.get(uri, headers=HEADERS)
    if r.status_code == 200:
        code = 200
        soup = BeautifulSoup(r.content, features="html.parser")
        arrivals_el = soup.select(SELECTOR_ARRIVING)
        for el in arrivals_el:
            slug = el.attrs['href'].split("/")[-1].split("-para-")[0]
            city_arrivals.append(slug)

        departures_el = soup.select(SELECTOR_DEPARTING)
        for el in departures_el:
            slug = el.attrs['href'].split("/")[-1].split("-para-")[-1]
            city_departures.append(slug)
    else:
        print(f"Non-200 code at {city_slug}")
        code = r.status_code

    return city_arrivals, city_departures, code

cities_arrivals = {}
cities_departures = {}
non_sucessful_slugs = []
for slug in tqdm(cities_slugs):
    city_arrivals, city_departures, code = retrieve_city_connections(slug)
    if code == 200:
        cities_arrivals[slug] = city_departures
        cities_departures[slug] = city_departures
    else:
        non_sucessful_slugs.append(slug)

# %%
