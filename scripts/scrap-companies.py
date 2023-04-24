# %%

from datetime import datetime
import json
import requests as req
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

# %%

# Definitions

HEADERS = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example'  # This is another valid field
}

URI_COMPANIES = "https://deonibus.com/viacao"
SELECTOR_COMPANIES = "#companies > div > a"

URI_COMPANY_ROUTES = "https://deonibus.com/viacao/{company_slug}"
SELECTOR_ROUTES = ".tab-content > article.section-routes > a"

# %%

# Get all companies

r = req.get(URI_COMPANIES, headers=HEADERS)

if r.status_code == 200:
    soup = BeautifulSoup(r.content, features="html.parser")
    companies_els = soup.select(SELECTOR_COMPANIES)

    company_slugs = [el.attrs['href'].split("/")[-1].strip().lower()
                     for el
                     in companies_els]
else:
    raise Exception(f"Error: non-code 200 ({r.status_code})")
# %%


def retrieve_company_routes(company_slug: str) -> tuple:
    company_routes = []
    code = None
    uri = URI_COMPANY_ROUTES.format(company_slug=company_slug)
    r = req.get(uri, headers=HEADERS)
    if r.status_code == 200:
        code = 200
        soup = BeautifulSoup(r.content, features="html.parser")
        routes_els = soup.select(SELECTOR_ROUTES)
        for el in routes_els:
            source, destination = el.attrs['href'].split("/")[-1].split("-para-")
            row = (source, destination)
            company_routes.append(row)
    else:
        print(f"Non-200 code at {company_slug}")
        code = r.status_code

    return company_routes, code


companies_routes = {}
non_sucessful_slugs = []


for slug in tqdm(company_slugs):
    company_routes, code = retrieve_company_routes(slug)
    if code == 200:
        companies_routes[slug] = company_routes
    else:
        non_sucessful_slugs.append(slug)

# %%
non_sucessful_slugs_2 = []
for slug in tqdm(non_sucessful_slugs):
    company_routes, code = retrieve_company_routes(slug)
    if code == 200:
        companies_routes[slug] = company_routes
    else:
        non_sucessful_slugs_2.append(slug)
non_sucessful_slugs = non_sucessful_slugs_2
# %%
now = datetime.utcnow()

output_data = {}
output_data['slugs'] = company_slugs
output_data['non_sucessful_slugs'] = non_sucessful_slugs
output_data['routes'] = companies_routes
with open(f"data/{now}-company-routes.json", "w") as fid:
    json.dump(output_data, fid)
# %%
