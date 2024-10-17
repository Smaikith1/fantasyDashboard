import numpy as np
import pandas as pd

filepath = '2023Data/'

wrs, ds, rbs = pd.read_excel(filepath+'wrs.xlsx', header=0), pd.read_excel(filepath+'def.xlsx', header=0), pd.read_excel(filepath+'rbs.xlsx', header=0)

ds.columns = ds.iloc[0,:]
ds = ds.iloc[1:, :]

rbs.columns = rbs.iloc[0,:]
rbs = rbs.iloc[1:, :]

wrs = wrs.fillna(0)
ds = ds.fillna(0)
rbs = rbs.fillna(0)

wrs = wrs[wrs['Pos'] == 'WR']
rbs = rbs[rbs['Pos'] == 'RB']

games = 5
wrs = wrs[wrs['GS']>games]
ds = ds[ds['GS']>games]
rbs = rbs[rbs['GS']>games]

wrs_s = {'Rec': 1, 'Yds': 0.1, 'TD': 6}
ds_s = {'Sk': 6,
        'Comb': 1,
        'Int': 7,
        'FF': 5,
        'TFL': 2.5,
        'PD': 5}
rbs_s = {'Yds': 0.1, 'TD': 6}

wrs['Fant Pts'], ds['Fant Pts'], rbs['Fant Pts'] = (np.full(len(wrs), 0), np.full(len(ds), 0),
                                                    np.full(len(rbs), 0))

for k in wrs_s.keys():
    wrs['Fant Pts'] += wrs_s[k]*wrs[k]

for k in ds_s.keys():
    ds['Fant Pts'] += ds_s[k] * ds[k]

for k in rbs_s.keys():
    rbs['Fant Pts'] += rbs_s[k]*rbs[k]

rbs = rbs[rbs['Fant Pts'] > 2]
wrs = wrs[wrs['Fant Pts'] > 50]

rbs['Value'] = rbs['Fant Pts']/rbs['G']
wrs['Value'] = wrs['Fant Pts']/wrs['G']
ds['Value'] = ds['Fant Pts']/ds['G']

ds = ds.sort_values(by='Fant Pts', ascending=False)

import matplotlib.pyplot as plt

plt.figure()

bins = 50
alpha = 0.85
xlim = 25

plt.subplot(3,1,1)
plt.hist(wrs['Value'], bins=bins, alpha=alpha)
plt.ylabel('WRs')
plt.xlim(0, xlim)

targets = ['Christian Kirk', 'Michael Pittman Jr.', 'Chris Olave', 'D.K. Metcalf*']

values = pd.Series(wrs['Value'])
values.index=wrs['Player']

for p in targets:

    plt.axvline(values[p], c='r')
    plt.text(values[p]+0.25, 2, p, rotation=90)

plt.subplot(3,1,2)
plt.hist(rbs['Value'], bins=bins, alpha=alpha)
plt.ylabel('RBs')
plt.xlim(0, xlim)

targets = ['Najee Harris', 'Bijan Robinson', 'Travis Etienne']

values = pd.Series(rbs['Value'])
values.index=rbs['Player']

for p in targets:

    plt.axvline(values[p], c='r')
    plt.text(values[p]+0.25, 2, p, rotation=90)

plt.subplot(3,1,3)
plt.hist(ds['Value'], bins=bins, alpha=alpha)
plt.ylabel('DPs')
plt.xlim(0, xlim)

targets = ['Khalil Mack*', 'Kyle Hamilton*+', 'Fred Warner*+', 'Patrick Queen*', 'Nick Bosa*', 'Julian Love*']

values = pd.Series(ds['Value'])
values.index=ds['Player']

for p in targets:

    plt.axvline(values[p], c='r')
    plt.text(values[p]+0.25, 2, p, rotation=90)

plt.legend(['wrs', 'rbs', 'dp'])

plt.xlabel('Fantasy Points Per Game Played')

plt.show()