from tqdm import tqdm
import os
import pandas as pd
import numpy as np
import itertools
from math import factorial
from itertools import permutations

df = pd.read_csv('destinyArmor.csv')
stat_names = ['Mobility (Base)', 'Resilience (Base)', 'Recovery (Base)', 'Discipline (Base)', 'Intellect (Base)',
              'Strength (Base)', 'Total (Base)']

hunter = df[df.Equippable == 'Hunter']

hunter = hunter[(hunter.Id.str.replace('"', '').isin(['6917529113067904764'])) | (
        (hunter.Type != 'Leg Armor') & (hunter['Tier'] == 'Legendary'))]
# hunter = hunter[(hunter.Name == 'St0mp-EE5') | ((hunter.Type != 'Leg Armor') & (hunter['Tier'] == 'Legendary'))]
hunter = hunter[hunter['Armor2.0']]
hunter = hunter[(hunter['Total (Base)'] >= 60) & (hunter['Type'] != 'Hunter Cloak')]


# Ensure all gear is masterwork
unmasterworked_gear = hunter[hunter['Masterwork Tier'] < 10.0]['Id']
_rows = hunter['Id'].isin(unmasterworked_gear)
hunter.loc[_rows, stat_names] = hunter.loc[_rows, stat_names].apply(lambda x: x + 2)

groups = hunter['Id'].groupby(df.Type)
item_id = groups.apply(list)
# item_id = [x for x in item_id]
armor_loadouts = itertools.product(*item_id)


def get_stats(_loadout):
    gear = hunter[hunter.Id.isin(_loadout)]
    return gear[stat_names].apply(sum).to_list()


def number_of_combinations(n, r):
    return int(factorial(n) / factorial(n - r))


cnt = number_of_combinations(len(hunter), 4)
print(f'Number of possible combinations: {cnt:,}')

# i = 0
# for loadout in tqdm(armor_loadouts, total=cnt):
#     hunter.loc[hunter.Id.isin(loadout), 'group'] = int(i)
    # break




_totals = []
for loadout in tqdm(armor_loadouts, total=cnt):
    _stat_totals = list(loadout) + get_stats(loadout)
    # print(_stat_totals)
    # if _stat_totals['Mobility (Base)'] >= 60
    if _stat_totals[7] >= 70:
        _totals.append(_stat_totals)
    break

totals = pd.DataFrame(_totals, columns=['Chest', 'Gauntlets', 'Helmet', 'Legs',
                                        'Mobility (Base)', 'Resilience (Base)', 'Recovery (Base)',
                                        'Discipline (Base)', 'Intellect (Base)', 'Strength (Base)', 'Total (Base)'])

totals.to_pickle('totals.pickle')
