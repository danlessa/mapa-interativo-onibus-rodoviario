# %%

import json
import geocoder
from tqdm.auto import tqdm

# %%

with open('data/2022-12-17 14:46:49.632892-output.json', 'r') as fid:
    data = json.load(fid)

non_found_slugs = []
coords = {}
for slug in tqdm(data['slugs']):
    splitted_slug = slug.split("-")
    uf = splitted_slug[-1].upper()
    place = " ".join(splitted_slug[0:-1])
    address = f'{place}, {uf}, Brazil'
    g = geocoder.osm(address)
    if g.osm is not None:
        slug_coords = (g.osm['x'], g.osm['y'])
    else:
        print(f"Coords not found for {slug}")
        non_found_slugs.append(slug)
        slug_coords = (None, None)
    coords[slug] = slug_coords
# %%

from datetime import datetime
now = datetime.utcnow()

output = {'coords': coords, 'non_found_slugs': non_found_slugs}

with open(f'data/{now}-coords.json', 'w') as fid:
    json.dump(output, fid)
# %%
