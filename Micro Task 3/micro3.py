from datetime import datetime
from subprocess import call
from pprint import pprint
import pandas as pd
import time
import matplotlib.pyplot as plt
import requests
import json
from perceval.backends.core.git import Git

from perceval.backends.core.github import GitHub


start = time.clock()
   
parent = "chaoss"  #name of the user/organization u want to analyze

github_token = ""  #you need to enter your own git hub authentication token 


url="https://api.github.com/users/"+parent+"/repos"

resp=requests.get(url)

#check if we successfully pulled the repositories list
if resp.status_code!=200:
	print(str(resp.status_code)+" Resolve status Code Issue")
	quit()

resp=resp.json()

repo_list=[]

for repo in resp:
	repo_name = repo['name']
	repo_url=repo['html_url']     #github repository url
	repo_dir = '/tmp/'+repo_name
	
	print("Started "+repo_name)
	commit_count=0
	issue_count=0
	pull_count=0	
	git_commit = Git(uri=repo_url, gitpath=repo_dir)
	
	#count no of commits
	for commit in git_commit.fetch():
		date_diff=datetime.now()-datetime.strptime(commit['data']['CommitDate'][:-6], "%a %b %d %H:%M:%S %Y")
		if date_diff.days <=90:
			commit_count+=1


	items = GitHub(owner=parent, repository=repo_name, api_token=github_token)
	#count no of pull_requests,issues
	for item in items.fetch():
		date_diff=datetime.now()-datetime.strptime(item['data']['created_at'], "%Y-%m-%dT%H:%M:%SZ")		
		if date_diff.days <=90:		
			if 'pull_request' in item['data']:
				pull_count+=1
			else :
				issue_count+=1
	
	clubbed_data={'repo':repo_name,'commit':commit_count,'issue':issue_count,'pull':pull_count,'total':commit_count+issue_count+pull_count}
	repo_list.append(clubbed_data)

repo_table=pd.DataFrame(repo_list)
repo_table=repo_table[['repo','commit','issue','pull','total']]

repo_table.sort_values(by=['total'], ascending=False)

repo_table.to_csv('repository_data.csv',index=True)

graph_issues = repo_table.plot(x=repo_table['repo'],kind='bar', figsize=(20,15), title ="Issues in the last 6 months",legend=True, fontsize=12)

plt.show()


print("time taken :"+str(time.clock() - start)+" sec")
