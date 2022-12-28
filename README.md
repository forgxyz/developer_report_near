# NEAR Developer Report
The purpose of this repository is to ensure the data collection behind the 2022 NEAR Developer Report, produced by [Flipside Crypto](https://flipsidecrypto.xyz/), is transparent and reproducible. Measurable activity is limited to public repositories on Github and we are using the list compiled by Electric Capital as of December 22, 2022.

The output of running this script is stored as a pickled DataFrame. The contribution activity data was collected around 17:00 UTC on December 28, 2022.

## Methodology
We are using the rules of contributions as defined by the developers behind the [Github Activity](https://github-activity.readthedocs.io/en/latest/) package:

> Here are the rules we follow for finding a list of contributors within a time window. A contributor is anyone who has:
> - Had their PR merged in that window
> - Commented on >= 2 issues that weren’t theirs
> - Commented >= 6 times on any one issue

An important note, here, is that this is not capturing dev activity by commits or lines added, as many other approaches do. Our reasoning is a desire to caputre "collaborative development" where an Issue or PR is opened, discussed, reviewed, and worked on in tandem with multiple devs. This does mean that certain activity may not be counted in this report. For example, in QAing the `github_activity` data dump, we noticed [Near-Lands](https://github.com/vgrichina/near-lands) was not included because all activity (in 2022) was without an issue or PR. Future iterations of this report may include a more comprehensive definition of activity.

## Attribution
Thanks to [Electric Capital](https://github.com/electric-capital/crypto-ecosystems) for compiling a great list of repositories for crypto ecosystems.

### Pecularities
Note: Python >3.11 is required for `tomllib`.
Snowflake connector is only compatible up to 3.9.x, so you must ignore the full `requirements.txt` and install the packages manually. `load.py` is used to load the result to our (Flipside) warehouse.