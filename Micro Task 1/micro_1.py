from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from subprocess import call
from pprint import pprint
import pandas as pd
import time
start = time.clock()
   

raw_index="mordred_raw"                          #raw index name
enriched_index="mordred_enriched"                #enriched index name
repo_url="https://github.com/chaoss/grimoirelab-mordred.git"     #github repository url

es = Elasticsearch('http://localhost:9200', verify_certs=False)

call("p2o.py --enrich --index " + raw_index +" --index-enrich " +  enriched_index + " -e http://localhost:9200 --no_inc --debug git  "+ repo_url,shell=True)


s = Search(using=es, index=enriched_index)
s.aggs.bucket('by_authors', 'terms', field='author_name', size=10000).metric('first_commit', 'min', field='author_date') #aggregate on the basis of author name and find oldest commit date for each of them
s = s.sort("author_date")


result = s.execute()


buckets_result = result['aggregations']['by_authors']['buckets']
buckets = []
for bucket in buckets_result:
    first_commit = bucket['first_commit']['value']/1000
    buckets.append(
        {'first_commit': datetime.utcfromtimestamp(first_commit),
        'author': bucket['key'],
	'commit_count': bucket['doc_count']}
        )

commiters = pd.DataFrame.from_records(buckets)
commiters.sort_values(by='first_commit', ascending=False, inplace=True)



per_month = commiters['first_commit'] \
    .groupby([commiters.first_commit.dt.year,
            commiters.first_commit.dt.month]) \
    .agg('count') #count number of commits per month

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\########################################################################")
pprint(per_month) #print the monthly commits table
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\########################################################################")
pprint(commiters) #print the author wise commits table

per_month.to_csv('commiters_per_month.csv')
line='Year,Month,Count'
with open('commiters_per_month.csv', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
commiters.to_csv('new_commiters.csv',columns=['first_commit', 'author','commit_count'],index=True)


print("time taken :"+str(time.clock() - start)+" sec")
