# Intro

Seedstats.py retrieves and proesses seed data from the Archive-It Partner Data API. It generates a CSV report on the crawling activity for one or more seed URLs based on a string match. The report includes:

- The seed ID
- Number of crawls for the seed
- Collection no.
- Collection name
- Date of first crawl
- Date of last crawl
- Total data collected

The most useful field in most cases is "Total data collected," which is not easily accessible through the Archive-It web application.


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

### Basic usage is:

`seedstats.py "string match"`

E.g., to collect stats on any seed matching "instagram.com," use:

`seedstats.py "instagram.com"` 


### Options

You can optionally specify the collection number (if known) and the output file path where the CSV will be saved.

To specify the collection number, use the -c flag:

`seedstats.py "string match" -c 18804`

To specify the output path, use the -o flag (by default, it will save to the script folder): 

`seedstats.py "string match" -o /path/to/folder/`

# Best Practises

The script makes multiple API requests, and can take a while to run if your input string matches multiple seeds, or if your seeds have an extensive crawl history. To speed things up, be as specific as possible with your search string, and specify a collection number.

If the script stops abruptly, try running it again. The API pages occasionally become unavailable, which will cause errors. Improved error handling could be added to a future version.

# Future Work

- Restricting the report by crawl date range would be useful (-d option flag).
- Improved error handling for data retrieval (connection drops, json load problems, etc.)  






  
  

