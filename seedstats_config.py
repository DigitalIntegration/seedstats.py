#### Insert your Archive-It username and pwd here, between quotes
user_login = ''
user_pwd = ''
#####

#### You shouldn't need to modify these constants
SEEDURL = 'http://partner.archive-it.org/api/seed?limit=-1'
CRAWL_STATS_URL = 'https://partner.archive-it.org/api/reports/seed/'
CRAWL_URL_FOR_SEEDS = 'https://partner.archive-it.org/api/seed_report_entry?limit=-1&pluck=crawl_job&seed='
PLUCK_COLLECTION_URL = "https://partner.archive-it.org/api/crawl_job?pluck=collection&id="
PLUCK_START_DATE_URL = "https://partner.archive-it.org/api/crawl_job?pluck=original_start_date&id="
COLLECTION_DATA_URL = "https://partner.archive-it.org/api/collection?limit=-1"
CRAWL_URL = "https://partner.archive-it.org/api/crawl_job?id="
