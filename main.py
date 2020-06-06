import requests
import json
import pprint
from markdown import markdown

from dateutil.parser import *

github_username = "wisehackermonkey"  # thats me! wooh!

# returns date in YYYYMMDD format
def formated_date(d):
    d = parse(d)
    day = str(d.day).rjust(2,"0")
    month = str(d.month).rjust(2,"0")
    year = d.year 

    return "{}{}{}".format(year,month,day)

if __name__ == "__main__":
    results = requests.get(f"https://api.github.com/users/{github_username}/repos?per_page=100")

    json_results = json.loads(results.text)


    base_url = json_results[0]["owner"]["html_url"]
    repo_names = [repo['name'] for repo in json_results]
    repo_url = [repo['html_url'] for repo in json_results]
    repo_description = [repo['description'] for repo in json_results]
    repo_date = [formated_date(repo['created_at']) for repo in json_results]

    repo_data = list(zip(repo_names, repo_description, repo_url,repo_date))
    # "html_url": "https://github.com/wisehackermonkey/20181006_shooter",
    # "description": "First Person Shooter built in unity following a tutorial",
    # print(json_results)
    # print(repo_url)
    # print(repo_description)
    # print(repo_names)

    html_data = ""
    for repo in json_results[0:-1]:
        if repo["has_pages"] == True:
            repo_name =         repo["name"]
            repo_url =          repo["html_url"]
            repo_description =  repo["description"]
            repo_date =         repo["created_at"]
            repo_short_name = repo["full_name"]

            # convert repo date to YYYYMMDD
            repo_date = formated_date(repo_date)
            
            post_text = f"""
---------------
# [{repo_name}](https://{github_username}.github.io/{repo_name})
##### {repo_description}
##### [{repo_short_name}]({repo_url})
```
{repo_date}
```
---------------
    """
            html_data += markdown(post_text)


    print(html_data)
    with open("./BLOG.md","w") as f:
        f.write(html_data)
