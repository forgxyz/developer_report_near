import github_activity as ga
import logging
import tomllib as tl
import os
import sys
import time
import pandas as pd

from datetime import datetime, timedelta, timezone

# logging config
logging.basicConfig(filename='.log/activity.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# python 3.11 required for tomllib
# note - must set GITHUB_ACCESS_TOKEN environment variable

# define output dataframe
columns = ['state', 'id', 'title', 'url', 'createdAt', 'updatedAt', 'closedAt',
           'labels', 'number', 'authorAssociation', 'author', 'mergedBy',
           'mergeCommit', 'baseRefName', 'comments', 'org', 'repo', 'thumbsup', 'ingestion_range', '_ingested_at']
results = pd.DataFrame(columns=columns)

# set location of resource files
directory = 'electric'

# set range of data to be ingested, assumed to be quarterly
range_start = '2019-01-01'
num_quarters = 16

# partition the ingestion range into quarters
slices = pd.DataFrame()
slices['date'] = pd.date_range(start=range_start, periods=num_quarters, freq='Q')

# loop through the quarters
since = range_start

for i, range_end in enumerate(slices['date']):
    quarter_results = pd.DataFrame(columns=columns)
    until = range_end.strftime('%Y-%m-%d')

    for file in os.listdir(directory):
        with open(f'{directory}/{file}', 'rb') as f:
            config = tl.load(f)

            for url in config['repo']:
                # request the activity data from the github api
                target = url['url'].split('https://github.com/')[1]
                org = target.split('/')[0]
                repo = target.split('/')[1]

                try:
                    res = ga.get_activity(target, since, until)
                except Exception as e:

                    print("Stopped due to exception.")

                    logging.exception(msg=f'Failed to get activity for {target} in {file} from {since} to {until}.')
                    
                    # store the results that were successfully ingested prior to the exception
                    results.to_pickle(f'data/exception/results_{since}_{until}_{file[:-5]}.pkl')
                    sys.exit(1)

                res['ingestion_range'] = f'{since}_{until}'

                # set _ingested_at column to current utc timestamp
                res['_ingested_at'] = datetime.now(timezone.utc).timestamp()

                # append the response to overall results df
                quarter_results = pd.concat([quarter_results, res])
                results = pd.concat([results, res])

                # save the intermediate results to a pickle file, just in case
                if len(res.index) > 0:
                    res.to_pickle(f'data/repo/results_{since}_{until}_{org}_{repo}.pkl')
                else:
                    with open('.log/empty_log.txt', 'a+') as f:
                        f.write(f'{since}_{until}_{file}_{org}_{repo} is empty\n')
    
    quarter_results.to_pickle(f'data/quarterly/results_{since}_{until}.pkl')

    # wait 40 min before starting the next run
    print(f'{since} to {until} complete. Sleeping for 40 minutes... Start time: {datetime.now().strftime("%H:%M:%S")}')
    
    # but only if it's not the last run
    if i < num_quarters - 1:
        time.sleep(2400)

    since = (datetime.strptime(until, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

# save the final results to a pickle file
results.to_pickle(f'data/final/results_{range_start}_{num_quarters}.pkl')
