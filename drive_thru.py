import pandas as pd
import requests


def coordinates_range(x, y=None, step=1):
    if y is None:
        return range(x)
    else:
        coord = [x]
        i = coord[0]
        while i <= (y - step):
            i += step
            i = round(i, 2)
            coord.append(i)
        return coord


def starbucks_drive_thru(range_diff, output=False):
    assert isinstance(output, bool), "output variable must be True or False"

    latitude = coordinates_range(50, 60, range_diff)
    longitude = coordinates_range(-8, 2, range_diff)

    base_api_url = 'https://www.starbucks.co.uk/api/v1/store-finder?&place=United+Kingdom'

    stores = []
    for i in latitude:
        for j in longitude:
            url = base_api_url + f'&latLng={str(i)}%2C{str(j)}'
            page = requests.get(url)

            for store in page.json()['stores']:
                drive_thru = 0
                for amenity in store['amenities']:
                    if amenity['description'] == 'Drive-Through':
                        drive_thru = 1
                stores.append([store['name'], store['address'], drive_thru, store['coordinates']])

            if not str(page) == '<Response [200]>':
                print(f'ERROR: Coordinates ({i}, {j}) not found')
            else:
                print(f'Coordinates ({i}, {j}) success')

    df = pd.DataFrame(stores, columns=['StoreName', 'Address', 'DriveThru', 'Coordinates'])
    df_unique = df.drop_duplicates('Address')

    if output:
        bps = str(int(range_diff * 100))
        df_unique.to_excel(f'Starbucks/data/Stores_{bps}bp_Range.xlsx', index=False)

    return df_unique


starbucks_drive_thru(range_diff=1)
