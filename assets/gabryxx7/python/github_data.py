from github import Github
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import requests
import oyaml

# First create the treeprocessor

class ImgExtractor(Treeprocessor):
    def run(self, doc):
        "Find all images and append to markdown.images. "
        self.markdown.images = []
        for image in doc.findall('.//img'):
            self.markdown.images.append(image.get('src'))

# Then tell markdown about it

class ImgExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        img_ext = ImgExtractor(md)
        md.treeprocessors.add('imgext', img_ext, '>inline')

# Finally create an instance of the Markdown class with the new extension

md = markdown.Markdown(extensions=[ImgExtExtension()])

# First create a Github instance:

# using username and password
with open(("github_credentials.yaml"), "r") as cf:
    cred = oyaml.safe_load(cf)
g = Github(cred['username'], cred['password'])

# or using an access token
# g = Github("access_token")

# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

header = oyaml.safe_load("""
layout: project
title: title
icon: icon-github
caption: caption
description: >
  Descr
links:
  - title: Link
    url: https://github.com/Gabryxx7/TheTower
""")

# Then play with your Github objects:
# print(dir(g.get_user().get_repos()[0]))
for repo in g.get_user().get_repos():
    if "orkshop" not in repo.name:
        if 'abryxx7' in repo.owner.login and not repo.fork:
            print(repo.name)
            print(repo.html_url)
            try:
                print(repo.get_readme().download_url)
                r = requests.get(repo.get_readme().download_url, allow_redirects=True)
                readme_text = r.content.decode('utf-8')
                if len(readme_text.split('\n')) > 5:
                    header['title'] = repo.name
                    header['description'] = repo.description
                    header['caption'] = repo.description
                    header['links'][0]['url'] = repo.html_url
                    header_text = str(oyaml.dump(header, allow_unicode=True))
                    print("Header printed ")
                    open('../../../_projects/github/'+str(repo.name)+".md", 'w', encoding="utf-8").write("---\n"+header_text+"\n---\n\n"+str(readme_text))
                    # open('./readmes/'+str(repo.name)+".md", 'wb+').write(readme_text.decode('ascii'))
                    html = md.convert(r.content)
                    print(md.images)
            except Exception as e:
                print("No README.md " +str(e))
            print()
        # print('abryxx7' in repo.owner.login)