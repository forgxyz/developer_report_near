# NEAR Developer Report
The purpose of this repository is to ensure the data collection behind the 2022 NEAR Developer Report, produced by [Flipside Crypto](https://flipsidecrypto.xyz/), is transparent and reproducible. Measurable activity is limited to public repositories on Github and we are using the list compiled by Electric Capital as of December 22, 2022.

The output of running this script is stored as a pickled DataFrame. The contribution activity data was collected around 15:00 UTC on December 22, 2022.

## Methodology
We are using the rules of contributions as defined by the developers behind the [Github Activity](https://github-activity.readthedocs.io/en/latest/) package:

> Here are the rules we follow for finding a list of contributors within a time window. A contributor is anyone who has:
> - Had their PR merged in that window
> - Commented on >= 2 issues that weren’t theirs
> - Commented >= 6 times on any one issue

Note: Python >3.11 is required for `tomllib`.

## Attribution
Thanks to [Electric Capital](https://github.com/electric-capital/crypto-ecosystems) for compiling a great list of repositories for crypto ecosystems.
