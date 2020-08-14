from github import Github
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import requests
import oyaml
import re
from xml.etree import ElementTree
import os
from urllib.parse import urlparse

# I am honestly proud of this regex
# IMG_REGEXR = "!\[.*]\((.+)\)|<img\s.*?src=(?:'|\")([^'\">]+)(?:'|\")"
IMG_REGEXR = "(?:!\[[^\]]*\]\(([^\)]*)\))+|(?:<img\s.*?src=(?:'|\")([^'\">]+)(?:'|\"))"
first_image = None

def download_and_replace(match):
    global first_image
    print(match.group(0))
    if match.group(1) is not None:
        cap_group = match.group(1).strip()
    else:
        cap_group = match.group(2).strip()
    url = ""
    if len(cap_group) > 0:
        if 'github-readme-stats' in cap_group:
            return match.group(0)
        if 'http' in cap_group:
            if 'github.com' in cap_group:                
                url = cap_group.replace('github.com', 'raw.githubusercontent.com').replace('blob/','')
            else:
                url = cap_group
            file_name = os.path.basename(urlparse(url).path)
        else:
            url = "https://raw.githubusercontent.com/" +repo.full_name+"/master/"+cap_group
            file_name = os.path.basename(cap_group)
        path_from_root = '/assets/gabryxx7/img/GitHub/'+repo.name+'/'
        abs_path = os.path.abspath('../../../'+path_from_root)

        if os.path.exists(abs_path+'/'+file_name):
            print("Skipping: " +abs_path+'/'+file_name)
        else:
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            print("Downloading: " +abs_path+'/'+file_name +"\tFrom: " +str(url))
            f_img = requests.get(url, allow_redirects=True)
            open(abs_path+'/'+file_name, 'wb').write(f_img.content)

        print("Replaced string: " + match.group(0).replace(cap_group,path_from_root+file_name))
        if first_image is None:
            first_image = path_from_root+file_name
        return match.group(0).replace(cap_group,path_from_root+file_name)
    return cap_group

# First create the treeprocessor

class ImgExtractor(Treeprocessor):
    def run(self, doc):
        "Find all images and append to markdown.images. "
        self.md.images = []
        # print(dir(doc))
        # for image in doc.findall(".//img"):  #In xml.ElementTree the // means to look for all children and not just the direct ones https://docs.python.org/2/library/xml.etree.elementtree.html
        for image in doc.findall(".//*[@src]"): #This one looks for any sub element that has an attribute called src
            # 	Selects all subelements, on all levels beneath the current element. For example, .//egg selects all egg elements in the entire tree.
            self.md.images.append(image.get('src')) # Get simply gets the value of an attribute
            image.set('src', "test.png")

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
date: 2020-01-01
image: 
  path: ""
description: >
  Descr
links:
  - title: Source
    url: https://github.com/Gabryxx7/TheTower
""")

# Then play with your Github objects:
# print(dir(g.get_user().get_repos()[0]))
for repo in g.get_user().get_repos():
    if "orkshop" not in repo.name.lower():
        if 'abryxx7' in repo.owner.login.lower() and not repo.fork:
            print(repo.name)
            # print(repo.html_url)
            try:
                print(repo.get_readme().download_url)
                # print(repo.created_at)
                # print("https://raw.githubusercontent.com/" +repo.full_name+"/master/")
                # print(repo.full_name)
                # print(repo.trees_url)
                # print(repo.contents_url)
                # print(repo.archive_url)
                # print(repo.git_url)
        
                abs_path = os.path.abspath('../../../_projects/github/')
                file_name = str(repo.name)+".md"                                        
                if os.path.exists(abs_path+'/'+file_name):
                    print("Readme already exists: " +abs_path+'/'+file_name)
                else:
                    if not os.path.exists(abs_path):
                        os.makedirs(abs_path)
                    r = requests.get(repo.get_readme().download_url, allow_redirects=True)
                    if r.content is not None:
                        readme_text = r.content.decode('utf-8')
                        if readme_text is not None and len(readme_text.split('\n')) > 5:
                            # I tried with markdown but it did not work really work and I am not sure how to replace them in the final markdown                    
                            # html = md.convert(r.content)
                            # print(md.images)
                            readme_text = re.sub(IMG_REGEXR, download_and_replace, readme_text) # Calling a function for each match which will download the img and replace the path in the markdown file

                            header['title'] = repo.name
                            header['description'] = repo.description
                            header['caption'] = repo.description
                            header['date'] = repo.created_at
                            header['links'][0]['url'] = repo.html_url
                            header['image']['path'] = first_image

                            header_text = str(oyaml.dump(header, allow_unicode=True))

                            open(abs_path+'/'+file_name, 'w', encoding="utf-8").write("---\n"+header_text+"\n---\n\n"+str(readme_text))
                            first_image = None
            except Exception as e:
                print("No README.md " +str(e))
            print()