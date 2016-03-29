import requests
import json
import logging

from datetime import datetime

start = None
rows = None
num_found = None

UTF_8 = 'utf-8'

def search_group_artifact(search_term, start, rows):
	url = 'http://search.maven.org/solrsearch/select?q={}&start={}&rows={}&wt=json'
	url = url.format(search_term, start, rows)	
	
	globals()['start'] = int(start) + 1
	globals()['rows'] = int(rows)
	
	print 'Searching for {} appearing as either artifactId or groupId....'.format(search_term)
	perform_search(url)

def search_all_versions(group_id, artifact, start, rows):
	url = 'http://search.maven.org/solrsearch/select?q=g:\"{}\"+AND+a:\"{}\"&core=gav&rows=20&wt=json'
	url = url.format(group_id, artifact, start, rows)
	
	globals()['start'] = int(start) + 1
	globals()['rows'] = int(rows)

	print 'Searching for artifactId {} in groupId {} ....'.format(artifact, group_id)
	perform_search(url)

def search_artifacts_in_group(group_id, start, rows):
	url = 'http://search.maven.org/solrsearch/select?q=g:\"{}\"&guice={}&rows={}&wt=json'
	url = url.format(group_id, start, rows)
	
	globals()['start'] = int(start) + 1
	globals()['rows'] = int(rows)

	print 'Searching for all artifacts in groupId {} ....'.format(group_id)
	perform_search(url)

def search_all_artifacts(artifact, start, rows):
	url = 'http://search.maven.org/solrsearch/select?q=a:\"{}\"&start={}&rows={}&wt=json'
	url = url.format(artifact, start, rows)
	
	globals()['start'] = int(start) + 1
	globals()['rows'] = int(rows)

	print 'Searching for all artifacts with id {} ....'.format(artifact)
	perform_search(url)

def search_by_class_name(class_name, start, rows, flag):
	url = None
	if (flag == 0):
		url = 'http://search.maven.org/solrsearch/select?q=c:\"{}\"&start={}&rows={}&wt=json'
	else:
		url = 'http://search.maven.org/solrsearch/select?q=fc:\"{}\"&start={}&rows={}&wt=json'
	url = url.format(class_name, start, rows)
	
	globals()['start'] = int(start) + 1
	globals()['rows'] = int(rows)

	print 'Searching for all artifacts with class name {} ....'.format(class_name)
	perform_search(url)

def search_by_checksum(checksum, start, rows):
	url = 'http://search.maven.org/solrsearch/select?q=1:\"{}\"&start={}&rows={}&wt=json'
	url = url.format(checksum, start, rows)
	
	globals()['start'] = int(start) + 1
	globals()['rows'] = int(rows)

	print 'Searching for artifact having SHA-1 checksum {} ....'.format(checksum)
	perform_search(url)

def search_by_tag(tag, start, rows):
	url = 'http://search.maven.org/solrsearch/select?q=tags:{}&start={}&rows={}&wt=json'
	url = url.format(tag, start, rows)
	
	globals()['start'] = int(start) + 1
	globals()['rows'] = int(rows)

	print 'Searching for artifacts with tag {} ....'.format(tag)
	perform_search(url)



def perform_search(url):
	r = requests.get(url)
	if (r.status_code != 200):
		logging.warning('HTTP status code:', r.status_code)
		return
	
	json_dict = r.json()
	get_results(json_dict)

def get_results(json_dict):
	num_found = json_dict['response']['numFound']
	globals()['num_found'] = int(num_found)
	print '{} search results found\n'.format(num_found)
	if (num_found == 0):
		suggestions_list = json_dict['spellcheck']['suggestions']
		if (len(suggestions_list) == 0):
			print 'No suggestions'
			return

		print 'Suggestions:'
		suggestions = suggestions_list[1]['suggestion']
		for suggestion in suggestions:
			print suggestion
		return

	parse_json(json_dict)

def parse_json(json_dict):
	version = None
	latest_version = None
	version_count = None
	
	docs = json_dict['response']['docs']
	for doc in docs:
		maven_id = doc['id']
		group_id = doc['g']
		artifact_id = doc['a']
		if 'latestVersion' in doc:
			latest_version = doc['latestVersion']
			version_count = doc['versionCount']
		else:
			version = doc['v']
		updated = datetime.fromtimestamp(float(doc['timestamp']) / 1000.0).strftime('%Y-%m-%d')

		if 'p' in doc:
			packaging = doc['p']
		download = doc['ec']
		download = [download_type.encode(UTF_8)
					for download_type in download]

		artifact_id = 'Id: {}\nGroupId: {}\nArtifactId: {}\n'.format(maven_id, group_id, artifact_id)
		artifact_version = None
		if (version is None):
			artifact_version = 'Latest Version: {}\nVersion Count: {}\n'.format(latest_version, version_count)
		else:
			artifact_version = 'Version: {}\n'.format(version)
		artifact_details = 'Last Updated: {}\nPackaging: {}\nAvailable also: {}\n'.format(updated, packaging, download)
		print artifact_id + artifact_version + artifact_details

	print 'Showing results {} to {} out of {} results'.format(start, min(start + rows - 1, num_found), num_found)

#Bad of way testing if code works
test = None
if test:
	search_by_class_name('junit', 0, 10, 0)
	print SEPARATOR
	search_by_class_name('org.specs.runner.JUnit', 0, 10, 1)
	print SEPARATOR
	search_by_checksum('35379fb6526fd019f331542b4e9ae2e566c57933', 0, 10)
	print SEPARATOR
	search_by_tag('sbtplugin', 0, 10)
	print SEPARATOR
