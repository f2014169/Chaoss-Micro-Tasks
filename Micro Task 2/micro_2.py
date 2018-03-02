from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from subprocess import call
from pprint import pprint
import pandas as pd
import time
import matplotlib.pyplot as plt

start = time.clock()
   
parent = "chaoss"
name_of_repo = "grimoirelab-elk"

raw_index="elk_raw"                          #raw index name
enriched_index="elk_enriched"                #enriched index name

github_token = ""  #you need to enter your own git hub authentication token 

es = Elasticsearch('http://localhost:9200', verify_certs=False)

call("p2o.py --enrich --index " + raw_index +" --index-enrich " +  enriched_index + " -e http://localhost:9200 --no_inc --debug github "+ parent +" "+ name_of_repo +" -t "+ github_token + " --sleep-for-rate",shell=True)


s = Search(using=es, index=enriched_index)


s = s.source(['item_type','id_in_repo','created_at', 'time_to_close_days', 'state']) #choose only requied fields
 
s = s.filter('terms', item_type=['issue'])  #filter only issues

s = s.filter('range', created_at={'gte' : 'now-6M'}) #filter only the past 6 months data

s = s.filter('terms', state=['closed']) # filter only closed issues

s = s.sort({'created_at': { 'order' : 'asc'}})

result = s.execute()

result_list=[]

for i in result:
	result_list.append(i.to_dict())

issues = pd.DataFrame(result_list)



graph_issues = issues.plot(x=issues['id_in_repo'],kind='bar', figsize=(20,15), title ="Issues in the last 6 months",legend=True, fontsize=12)

plt.show()
