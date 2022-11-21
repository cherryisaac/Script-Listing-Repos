import requests
import csv


# Github auth token required to run file/url more than 60 times per hour otherwise comment this out along with headers=headers
print("Please input auth token: ")
token1 = input("")
headers = { "Authorization" : "Bearer " + token1, 
          "Accept" : "application/vnd.github+json"}

organization = "codeclimate"

def get_repos():
    url = "https://api.github.com/orgs/"+organization+"/repos?sort=full_name&per_page=100&page=1"
    res = requests.get(url, headers=headers)
    repos = res.json()
    while 'next' in res.links.keys():
        res=requests.get(res.links['next']['url'],headers=headers)
        repos.extend(res.json())
    return repos
    

# Don't print to console because a LOT of results = slowdown; write to a file instead for results
def get_contributors(repo):
    repo_name = repo['full_name']
    url = "https://api.github.com/repos/"+repo_name+"/contributors?sort=full_name&per_page=100&page=1"
    return requests.get(url, headers=headers).json()  # , headers=headers

# Teams is likely to be empty
def get_teams(repo):
    repo_name = repo['full_name']
    url = "https://api.github.com/repos/"+repo_name+"/teams?sort=full_name&per_page=100&page=1"
    return requests.get(url, headers=headers).json()  # , headers=headers

repos = get_repos()
repo_name = [x['name'] for x in repos]
repo_size = [x['size'] for x in repos]
archived = [x['archived'] for x in repos]
license = [str(x['license']).split(": ")[0:3].pop().replace("'", "").split(',')[0:1].pop() for x in repos]  #use .split() for this one
private = [x['private'] for x in repos]
contributor_counts = [
    len(get_contributors(repo))
    for repo in repos
]
team_counts = [
    len(get_teams(repo))
    for repo in repos
]

repo_info = zip(*[repo_name, repo_size, archived, license, private, contributor_counts, team_counts])

#Export to csv portion---------------------------------------------------------------
with open('List_of_repos.csv', 'w') as csvfile: #Creating CSV file to be written to
    f = csv.writer(csvfile)

    header = ['Repo Name', '  Repo Size (MB)', '  Archived', '  License', '  Private', '  Contributors Count', '  Teams Count']
    f.writerow(header)

    for row in repo_info:
        f.writerow(row)

print("All Done!")
