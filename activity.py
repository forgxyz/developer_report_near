import github_activity as ga
import tomllib as tl
import os
import pandas as pd

columns = ['state', 'id', 'title', 'url', 'createdAt', 'updatedAt', 'closedAt',
        'labels', 'number', 'authorAssociation', 'author', 'mergedBy',
        'mergeCommit', 'baseRefName', 'comments', 'org', 'repo', 'thumbsup']
results = pd.DataFrame(columns=columns)

since = '2021-12-31'
until = '2022-12-31'
directory = 'electric'

for file in os.listdir(directory):
    print(file)
    with open(f'{directory}/{file}', 'rb') as f:
        config = tl.load(f)
        # test_url = config['repo'][0]['url'].split('https://github.com/')[1]
        for url in config['repo']:
            target = url['url'].split('https://github.com/')[1]
            res = ga.get_activity(target, since)
            results = pd.concat([results, res])


results.to_pickle('results.pkl')
