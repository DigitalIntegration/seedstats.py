# Intro

Seedstats.py retrieves data from the Archive-It Partner Data API. It generates a CSV report on the crawling activity for one or more seed URLs based on a string match. The report includes:

- The seed ID
- Number of crawls for the seed
- Collection no.
- Collection name
- Date of first crawl
- Date of last crawl
- Total data collected


# Requirements

- Python3
- Archive-It login credentials


# Setup

There are two files required:

- *seedstats.py*, the script file
- *seedstats_config.py*, the config file. Store this is the same folder as *seedstats.py*

You will need to open *seedstats_config.py* with an editor and add your Archive-It login credentials.


# Usage

Basic usage is:

seedstats.py "string match"
  
  

