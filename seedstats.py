import json
import requests
from datetime import datetime,date
import dateutil.parser
import unicodecsv as csv
import os
from requests.auth import HTTPBasicAuth
import sys
import argparse

# Import the Archive-It username and pwd + API URLs from config file.
# Archive-It username and pwd are required for authentication by the Data API.
# Username and pwd will need to be set before running this script
from seedstats_config import *


class Data():
	def __init__(self,ts=0,csv_header=None,filename=None):
		self.ts = datetime.now().timestamp()
		self.csv_header = ['Seed','Seed ID','No. Crawls', 'Collection No.', 'Collection Name', 'First Crawl','Last Crawl', 'Total Data Bytes']
		self.filename = 'seed_report' + '_' + str(date.today()) + "_" + str(self.ts) + ".csv"


def main():
	d = Data()
    # Parse the command line arguments.
	# A seed URL or partial seed URL is a required argument.
	# Output path (-o) will default to the active directory, collection (-c) will default to all collections.
	parser = argparse.ArgumentParser()
	parser.add_argument('seed_url',help='A seed url or partial seed url is required, e.g., \'instagram.com\'')
	parser.add_argument('-o','--output_path',help='The output file path',action='store')
	parser.add_argument('-c','--collection',help='To restrict to a specific Archive-It collection number, default is all. Recommend restricting if possible to avoid searching through all collections.',action='store')
	args = parser.parse_args()

	arg_dict = (vars(args))
	string_match = arg_dict['seed_url']

	if arg_dict['output_path'] != None:
		output_path = arg_dict['output_path']
	else:
		output_path = os.getcwd()
	print('\nOutput path: ' + output_path)

	full_filepath = output_path + "/" + d.filename
	collection = arg_dict['collection']

	write_row_to_csv(d.csv_header,full_filepath)
	get_crawl_data_for_each_seed(string_match,collection,full_filepath)

# send authorization credentials to AIT
def authorize_and_get_json(url):
	target = requests.get((url), auth=(user_login,user_pwd))
	return json.loads(target.content)

# Get all collection names and ids and save them to a dict.
def get_collection_names(target_url):
	nameid_dict = {}
	target_json = authorize_and_get_json(target_url)

	for collection in target_json:
		name = (collection['name'])
		id = (collection['id'])
		nameid_dict[id] = name

	return nameid_dict


# Simple write to csv method. Writes a list object to a csv row.
def write_row_to_csv(list_row,outputfile):
	with open (outputfile, mode='ab') as f:
		writer = csv.writer(f)
		writer.writerow(list_row)

### Get a list of seeds matching a string value
def get_matching_seeds(url,str_match):

	match_list = []
	seed_data = authorize_and_get_json(url)

	for seed in seed_data:
		try:
			seed_id = (seed['id'])
			seed_url = (seed['url'])

			if str_match in seed_url:
				new_seed_list_item = [seed_id,seed_url]
				match_list.append(new_seed_list_item)

		except:
			print('error getting id or url')

	match_len = str(len(match_list))
	print('\nNumber of matching seeds: ' + match_len)
	print('\nMatching seeds: ' + str(match_list))
	return(match_list)

### Iterate through each seed to get their crawl numbers
def get_collection_number(crawl_num):
	collection_url = PLUCK_COLLECTION_URL + str(crawl_num)
	collection_num = authorize_and_get_json(collection_url)[0]
	return collection_num # return the collection number for a particular seed based on the crawl number

def get_crawl_date(crawl_num):  # Return the date of the first crawl for the seed
	start_date_url = PLUCK_START_DATE_URL + str(crawl_num)
	start_date = authorize_and_get_json(start_date_url)[0]
	return start_date

# Check if the crawl is a deleted or expired test crawl. If so, it should not contribute to the overall data count.
def is_test_crawl(crawl_id):
	crawl_url = CRAWL_URL + str(crawl_id)
	target_json = authorize_and_get_json(crawl_url)
	for item in target_json:
		type = (item['type'])
		if type == 'TEST_EXPIRED' or type=='TEST_DELETED':
			return True


def get_crawl_data_for_each_seed(str_match,targ_coll,f_path):

	if targ_coll != None:
		targ_coll_url = SEEDURL + '&collection=' + targ_coll
		seed_list = get_matching_seeds(targ_coll_url,str_match)
	else:
		seed_list = get_matching_seeds(SEEDURL,str_match)

	print("\n>>>>>>>>>>>>> Collecting seed data >>>>> ")
	nameid_dict = get_collection_names(COLLECTION_DATA_URL)
	for seed in seed_list:

		index = (seed_list.index(seed) + 1)
		print("\n>>>>>>>>>>>>> Collecting seed data for " + seed[1] + " seed no. " + str(index) + " of " + str(len(seed_list)))

		data_size = 0
		crawl_url = CRAWL_URL_FOR_SEEDS + str(seed[0])
		print("List of crawl IDs for this seed: " + crawl_url)

		try:
			crawl_list = authorize_and_get_json(crawl_url)

			if len(crawl_list) != 0:
				first_crawl_date = get_crawl_date((crawl_list)[0])
				last_crawl_date = get_crawl_date((crawl_list)[-1])

				# getting crawl data for each crawl associated with a seed in the matching seed list
				print("\nChecking crawls:")
				for crawl_job in crawl_list:
					collection_num = get_collection_number(crawl_job)
					crawl_stats_url = CRAWL_STATS_URL + str(crawl_job) + "?limit=1000000" # high limit to get all instances

					print(crawl_stats_url)

					try:
						target_json = authorize_and_get_json(crawl_stats_url)
					except:
						continue

					for item in target_json:
						# item must be a dict (error handling)
						if isinstance(item,dict):

							try:
								if (item['seed_id'] == seed[0]):
									seed_data_size_for_crawl = item['warc_new_content_bytes']
									if seed_data_size_for_crawl != None and is_test_crawl(crawl_job) != True:
										data_size = data_size + seed_data_size_for_crawl

							except:	 # Awkward error handling b/c not all items seem to have a seed_id
								if (item['seed'] == seed[1]):
									seed_data_size_for_crawl = item['warc_new_content_bytes']
									if seed_data_size_for_crawl != None and is_test_crawl(crawl_job) != True:
										data_size = data_size + seed_data_size_for_crawl


				print('\nSeed: ' + str(seed))
				print('No. Crawls: ' + str(len(crawl_list)))
				print('Collection: ' + str(collection_num))
				print('Collection Name: ' + nameid_dict[collection_num])
				print('First Crawl: ' + first_crawl_date)
				print('Last Crawl: ' + last_crawl_date)
				print('Total Data for Seed: ' + str(data_size))

				this_row = [seed[1],seed[0],str(len(crawl_list)),str(collection_num),nameid_dict[collection_num],first_crawl_date,last_crawl_date,str(data_size)]

				write_row_to_csv(this_row,f_path)
		except:
			print('there is a problem with ' + seed)
			except_row = [seed[1],seed[0],'error','error','error','error','error','error']
			write_row_to_csv(except_row)

if __name__ == "__main__":
    main()
