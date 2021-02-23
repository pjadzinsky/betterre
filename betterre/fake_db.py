import os
import random

import pandas as pd
import numpy as np

from pyzipcode import ZipCodeDatabase


def fake_pm_by_quality(quality):
    """ the closer to 1, the better a pm is
    """
    how_bad = 1 - quality
    new_pm = dict()
    # zipcode and city
    if random.random() > 0.9:
        new_pm[0] = random.choice(ZIPCODES)
        new_pm[1] = zcdb[new_pm[0]]
    else:
        new_pm[0] = None
        new_pm[1] = None

    # description
    new_pm[2] = ""
    # button
    new_pm[3] = "<button class=""popmake-118"">Info</button>"

    # management_fee, in principle is uncorrelated with quality
    new_pm[4] = int(np.random.gamma(8))

    # average_rent
    average_rent = 1800 + 1700 * quality
    average_rent = (average_rent // 50) * 50
    new_pm[5] = int(average_rent)

    # vacancies
    new_pm[6] = int(np.random.gamma(20) + how_bad * np.random.gamma(30))
    # maintenance_calls
    calls = int(np.random.gamma(1) + 1 + how_bad * np.random.gamma(4))
    new_pm[7] = int(calls)

    # maintenance_cost
    call_cost = int((np.random.gamma(3) + 1) * (80 + 100 * how_bad))
    new_pm[8] = calls * call_cost

    # tenant_duration
    new_pm[9] = int(np.random.gamma(1.5) + 1 + 6 * quality)
    # unit_duration
    new_pm[10] = int(new_pm[9] + quality * 10)
    # units
    new_pm[11] = int(np.random.gamma(3) * 50 * quality)
    # experience
    new_pm[12] = new_pm[10] * 2 + np.random.randint(0, 20)
    return new_pm


def from_exported(n):
    """
    Grab first n files from exported file, this is mainly to create a df with correct columns

    :param n:
    :return:
    """
    df = pd.read_csv(os.path.expanduser('~/PycharmProjects/betterre/betterre/1-PM-Result-1-2021-01-25.csv'))
    return df.iloc[:n]


def add_noise(pm, zipcode, city):
    pm[0] = zipcode
    pm[1] = city

    # description
    pm[2] = ""
    # button
    pm[3] = "<button class=""popmake-118"">Info</button>"

    # pm[4] is management_fee

    # average_rent
    pm[5] += np.random.randint(-300, 300)

    # vacancies
    pm[6] += np.random.randint(30)

    # maintenance_calls
    pm[7] += np.random.randint(-1, 3)

    # maintenance_cost
    pm[8] += np.random.randint(-50, 50)

    # tenant_duration
    pm[9] += np.random.randint(0, 2)

    # unit_duration
    pm[10] += np.random.randint(-1, 2)

    # units
    pm[11] += np.random.randint(-200, 200)

    # experience
    pm[12] += np.random.randint(-1, 2)
    return pm


def faked_bad_2():
    """
    Fake a good property manager. Something similar to SPM but not necessailty the same

    :return:
    """
    new_pm = {}
    # management_fee, in principle is uncorrelated with quality
    new_pm[4] = np.random.randint(6, 8)

    # average_rent
    new_pm[5] = 1800

    # vacancies
    new_pm[6] = 45
    # maintenance_calls
    new_pm[7] = 11

    # maintenance_cost
    new_pm[8] = 335

    # tenant_duration
    new_pm[9] = 2
    # unit_duration
    new_pm[10] = 2
    # units
    new_pm[11] = 356
    # experience
    new_pm[12] = 7
    return new_pm


def faked_bad():
    """
    Fake a good property manager. Something similar to SPM but not necessailty the same

    :return:
    """
    new_pm = {}
    # management_fee, in principle is uncorrelated with quality
    new_pm[4] = np.random.randint(7, 10)

    # average_rent
    new_pm[5] = 2150

    # vacancies
    new_pm[6] = 21
    # maintenance_calls
    new_pm[7] = 7

    # maintenance_cost
    new_pm[8] = 550

    # tenant_duration
    new_pm[9] = np.random.randint(1, 3)
    # unit_duration
    new_pm[10] = new_pm[9]
    # units
    new_pm[11] = 753
    # experience
    new_pm[12] = 15
    return new_pm


def faked_good_1():
    """
    Fake a good property manager. Something similar to SPM but not necessailty the same

    :return:
    """
    new_pm = {}
    # management_fee, in principle is uncorrelated with quality
    new_pm[4] = np.random.randint(7, 9)

    # average_rent
    new_pm[5] = 2350

    # vacancies
    new_pm[6] = 14
    # maintenance_calls
    new_pm[7] = 3

    # maintenance_cost
    new_pm[8] = 855

    # tenant_duration
    new_pm[9] = 5
    # unit_duration
    new_pm[10] = 11
    # units
    new_pm[11] = 2200
    # experience
    new_pm[12] = 35
    return new_pm


def fake_expensive():
    """
    Fake a good property manager. But more expensive

    :return:
    """
    new_pm = {}
    # management_fee, in principle is uncorrelated with quality
    new_pm[4] = np.random.randint(10, 13)

    # average_rent
    new_pm[5] = 3100

    # vacancies
    new_pm[6] = 20
    # maintenance_calls
    new_pm[7] = 5
    # maintenance_cost
    new_pm[8] = 1105
    # tenant_duration
    new_pm[9] = 3
    # unit_duration
    new_pm[10] = 5
    # units
    new_pm[11] = 1350
    # experience
    new_pm[12] = 10
    return new_pm


def fake_pm_for_zipcode(zip, city):
    """
    Fake 4 property managers for this zip code, comming from the 4 methods that we have above
    fake_good, fake_expensive, fake_bad_1, fake_bad_2
    :param zip:
    :return:
    """
    pm1 = add_noise(faked_good_1(), zip, city)
    pm2 = add_noise(fake_expensive(), zip, city)
    pm3 = add_noise(faked_bad(), zip, city)
    pm4 = add_noise(faked_bad_2(), zip, city)

    city_df = pd.DataFrame([pm1, pm2, pm3, pm4])
    return city_df


def fake_df():
    zcdb = ZipCodeDatabase()

    zipcodes = zcdb.get_zipcodes_around_radius(94533, 20)
    cities = [z.city for z in zipcodes]
    zipcodes = [z.zip+"," for z in zipcodes]

    zips_and_cities_df = pd.DataFrame({"zip": zipcodes, "city": cities})
    zips_and_cities_df = zips_and_cities_df.groupby("city", as_index=False).agg(sum)

    df = from_exported(3)
    ints_to_cols = {i: df.columns[i] for i in range(df.shape[1])}

    dfs = []
    for _, row in zips_and_cities_df.iterrows():
        df = fake_pm_for_zipcode(row.zip, row.city)
        dfs.append(df)

    df = pd.concat(dfs)
    df.sort_index(axis=1, inplace=True)

    df.columns = [ints_to_cols[i] for i in range(df.shape[1])]
    df.rename({"Unnamed: 3": ""}, axis=1, inplace=True)

    df.to_csv('/tmp/faked_pms.csv', index=False)
    return df


if __name__ == "__main__":
    fake_df()