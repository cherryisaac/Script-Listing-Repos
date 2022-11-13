import requests
import csv


# Github auth token required to run file/url more than 60 times per hour otherwise comment this out along with headers=headers
print("Please input auth token:")
token1 = input("")
headers = { "Authorization" : "Bearer " + token1, 
          "Accept" : "application/vnd.github+json"}


organization = "codeclimate"

def get_repos():
    url = "https://api.github.com/orgs/"+organization+"/repos"
    return requests.get(url, headers=headers).json()

# Don't print to console because a LOT of results = slowdown; write to a file instead for results
def get_contributors():
    res = []
    repos = [x['full_name'] for x in get_repos()]
    for x in repos:
        url = "https://api.github.com/repos/"+x+"/contributors?per_page=100"
        res.append(requests.get(url, headers=headers).json())
    return res

# Teams is likely to be empty
def get_teams():
    res = []
    repos = [x['full_name'] for x in get_repos()]
    for x in repos:
        url = "https://api.github.com/repos/"+x+"/teams"
        res.append(requests.get(url, headers=headers).json())
    return res

repo_name = [x['name'] for x in get_repos()]
repo_size = [x['size'] for x in get_repos()]
archived = [x['archived'] for x in get_repos()]
license = "" #use .split() for this one
private = [x['private'] for x in get_repos()]
contributors_count = 0
# for x in get_contributors():
#     contributors_count+=1
# print("contributors:", contributors_count)
teams_count = 0
for x in get_teams():
    teams_count+=1
# print("teams:", teams_count)

#Export to csv portion---------------------------------------------------------------
with open('List_of_repos.csv', 'w') as csvfile: #Creating CSV file to be written to
    f = csv.writer(csvfile)
    # f.writerow(get_contributors(()))

    header = ['Repo Name', '  Repo Size(MB)', '  Archived', '  License', '  Private', '  Contributors Count', '  Teams Count']
    f.writerow(header)
     
    for x in get_repos():
        license = str(x['license']).split(": ")
        f.writerow([x['name'],' ',x['size'],' ',x['archived'],' ',license[0:3].pop().replace("'", "").split(',')[0:1].pop(),' ',x['private'],' ', contributors_count ,' ', teams_count])    

print("Completed")