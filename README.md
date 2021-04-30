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

There are two files involved:

- *seedstats.py*, the script file
- *seedstats_config.py*, the config file. Store this is the same folder as *seedstats.py*

You will need to open *seedstats_config.py* with an editor and add your Archive-It login credentials.

`user_login = 'your_login'`

`user_pwd = 'your_pwd'`

# Usage

## Basic usage is:

`seedstats.py "string match"`

E.g. `seedstats.py "instagram.com"` will match any seeds matching "instagram.com".

## Options

You can optionally specify the collection number (if known) and the output file path where the CSV will be saved.

To specify the collection number, use the -c flag:

`seedstats.py "string match" -c 18804`

To specify the output path, use the -o flag (by default, it will save to the script folder): 

`seedstats.py "string match" -o path/to/folder/`






  
  

