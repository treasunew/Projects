import requests
import plotly.express as px

url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000"

header = {
    "Accept": "application/vnd.github.v3+json"
}
r = requests.get(url, header)

print(f"Status code: {r.status_code}")

response_dict = r.json()

print(response_dict.keys())
print((f"Total repositories: {response_dict['total_count']}"))
print((f"Complete results: {not response_dict['incomplete_results']}"))

repo_dicts = response_dict['items']

# NOTE 方案1
repo_names, stars, hover_texts = [], [], []
for repo_dict in repo_dicts:
    repo_names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])
    # 创建悬停文本
    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    hover_text = f"{owner}<br />{description}"
    hover_texts.append(hover_text)

# NOTE 方案2
repo_links, stars, hover_texts = [], [], []
for repo_dict in repo_dicts:
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)
    stars.append(repo_dict['stargazers_count'])
    # 创建悬停文本
    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    hover_text = f"{owner}<br />{description}"
    hover_texts.append(hover_text)


# 可视化
title = "Most-Starred Python Projects on GitHub"
labels = {'x': 'Repository', 'y': 'Stars'}
# NOTE 方案1
# fig = px.bar(x=repo_names, y=stars, title=title, labels=labels, hover_name=hover_texts)
# NOTE 方案2
fig = px.bar(x=repo_links, y=stars, title=title, labels=labels, hover_name=hover_texts)
fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
yaxis_title_font_size=20)
fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6)
fig.show()