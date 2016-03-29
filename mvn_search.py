import argparse

from mvn_api import *

parser = argparse.ArgumentParser(description="Search artifacts in the Central Repository from terminal.")
parser.add_argument("-s", "--search", type=str, help="Basic search. Returns artifacts with search term in ArtifactId or GroupId")

parser.add_argument("-g", "--group", type=str, help="Returns all artifacts in specified group")
parser.add_argument("-a", "--artifact", type=str, help="Search all artifacts with specified id")

parser.add_argument("-c", "--class_name", type=str, help="Search by class name. Returns list of artifacts, down to the specific version containing the class")
parser.add_argument("-fc", "--fclass_name", type=str, help="Search by fully quantified class name. Returns list of artifacts, down to the specific version containing the class")

parser.add_argument("-cs", "--checksum", type=str, help="Search artifact by SHA-1 checksum")

parser.add_argument("-t", "--tag", type=str, help="Search for all artifacts having specified tag")

parser.add_argument("-st", "--start", type=str, help="Get search results from index start")
parser.add_argument("-r", "--rows", type=str, help="Number of search results to be displayed")
args = parser.parse_args()

start = 0
rows = 10
if args.start:
	start = args.start
if args.rows:
	rows = args.rows

if args.search:
	search_group_artifact(args.search, start, rows)

elif args.group and args.artifact:
	search_all_versions(args.group, args.artifact, start, rows)

elif args.group:
	search_artifacts_in_group(args.group, start, rows)

elif args.artifact:
	search_all_artifacts(args.artifact, start, rows)

elif args.class_name:
	search_by_class_name(args.class_name, start, rows, 0)
elif args.fclass_name:
	search_by_class_name(args.fclass_name, start, rows, 1)

elif args.checksum:
	search_by_checksum(args.checksum, start, rows)

elif args.tag:
	search_by_tag(args.tag, start, rows)

else:
	parser.print_help()