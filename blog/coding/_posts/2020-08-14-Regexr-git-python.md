---
title: Extracting data with `python` and regular expressions `regEx`
excerpt_separator: <!--more-->
---

A big portion of my PhD is to deal with patterns. They present themselves in many ways: Movements, images and pixels, sounds etc... But since computers deal mostly with numbers and code, the easiest way is to reduce any pattern to text, or  code.

## What are regular expressions
Text, especially code, can easily be parsed by defining patterns and looking for them. Think about it as if you are reading a page of a book or even a website: You look for patterns, be it an email, a phone number, the structure of a sentence.

While the semantic of a sentence is not easy to parse and understand for a computer (see the whole branch of NLP), encoded and marked text can easily be captured by specifying patterns.
Emails for instance are defined by `username@domain` and we all know how to read them, we all know that `username` is anything that preceeds the `@` character, and anything after it is the `domain`.

I find this concept of patterns, text and encoding extremely fascinating and stimulating. I might make a post just about them but for now let's focus on this little project.

- Table of Contents
{:toc .large-only}

<!--more-->

## Downloading GitHub repositories data
### Downloading the `README.md` 
I wanted to port all of my GitHub projects on my website. Since the `README.md` files are already markdown, Jekyll will know how to render them. Of course I would also like to get all the images I use in the readmes. As the lazy programmer that I am, I would rather spend 2 hours writing some code that does it for me rather than manually copy-pasting each project's `README.md` file.

The first thing I needed to do is to find out whether GitHub had an API or not. Depending on the answer I could have used a python-based browser, for instance `beautifulsoup` or the `request` package to send `GET` and `POST`.

Luckily GitHub does have an API and of course there already was a package wrapped around it, (`PyGithub`)[https://github.com/PyGithub/PyGithub].
So let's start by importing it and getting my own info from github

```python
from github import Github
import oyaml

with open(("github_credentials.yaml"), "r") as cf:
    cred = oyaml.safe_load(cf)
g = Github(cred['username'], cred['password'])

for repo in g.get_user().get_repos():
    print(repo.name)

```

I made the mistake once of committing a `.py` file with my credentials in plain text. This time I am not making the same mistake. My username anf file are in a `yaml` file structured like this:

```yaml
username: "gabryxx7"
password: "password" # You wish...
```

I used a wonderful package called `oyaml` (ordered `yaml`) which is just a wrapper around `yaml`. I can't remember why I stiched to this one, something to do with the ordering, stumbled upon this issue while working on the `AI_Dating` project.
Anyways back to the topic. Once I got my own GitHub details, I am iterating through the list of repositories in my account.
As soon as I run the code I saw an enormous amount of new lines being printed. Well that was not because of my awesome curriculum and activities on GitHub, it was because of the new GitHub Classroom that we are using at the University of Melbourne for the `COMP30019` subject.
Every student in the subject can copy one of our workshop's template repository in our GitHub organisation/classroom. And since me and the other tutors are the owner of the organisation, we are also owners of all the repositories, which means all of those repositories appear in my list.
Besides that, there are lots of forks that I don't really use. In short, I only want **MY** repositories, the ones that I created. so with a very simple string comparison:

```python
for repo in g.get_user().get_repos():
    if "workshop" not in repo.name.lower():
        if 'gabryxx7' in repo.owner.login.lower() and not repo.fork:
            print(repo.name)
```

Now we are talking! If the name `workshop` appears in the title of the repository we'll just skip it. Same if the owner is not me.
Unfortunately, `PyGithub` documentation is not great so it's hard to know what variables or methods the repository object has.
In these cases I usually just go to the (source code repository)[https://github.com/PyGithub/PyGithub/blob/master/github/Repository.py] and with a simple `ctrl + f` I look for whatever I need. In this case I was looking for:

- The name of the repository
- The `README.md` file url
- The repository's date of creation
- The repository caption and description
- The repository's link

So after a few `ctrl+f` here and there I found everything I needed to create a Jekyll project out of the GitHub repo. Let's set up the `yaml` header for Jekyll:

```python
header = oyaml.safe_load("""
    layout: project
    title: title
    icon: icon-github
    caption: caption
    date: 2020-01-01
    image: ""
    path: ""
    description: >
    Descr
    links:
    - title: Source
        url: https://github.com/Gabryxx7
    """)
```
I find it easier to define it this way and then read it with yaml rather than defining the dictionary and adding every `(key,value)` pair to it.

So now we are ready to download our `README.md` and use them as jekyll projects!

```python
for repo in g.get_user().get_repos():
    if "orkshop" not in repo.name:
        if 'abryxx7' in repo.owner.login and not repo.fork:
            print(repo.name)
            try:
                print(repo.get_readme().download_url)        
                abs_path = os.path.abspath('../../../_projects/github/')
                file_name = str(repo.name)+".md"                                        
                if os.path.exists(abs_path+'/'+file_name):
                    print("Readme already exists: " +abs_path+'/'+file_name)
                else:
                    # Create the folder tree if it does not exist
                    if not os.path.exists(abs_path):
                        os.makedirs(abs_path)
                    # Download the readme/md
                    r = requests.get(repo.get_readme().download_url, allow_redirects=True)
                    if r.content is not None:
                        readme_text = r.content.decode('utf-8') # decode the binary content as 'utf-8' to allow for emojis
                        if readme_text is not None and len(readme_text.split('\n')) > 5:
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
            print() # new line separator
```

And there you have it! This little for loop will now dowlonad all of your readmes from GitHub and save them into the `_projects` folder with a nice `yaml` header.

But **WAIT!** the readmes often have images, which are relative to the repository, or they are even external links or links to the raw image file in github. Oh shoot! What's the point of having this nice project showcase if I then have to manually add the screenshots? And what if I change anything on github, I'd have to do it again manually and it would take ages! Plus I'd have to replace the relative paths in the code as well, besides downloading all the images.

### Downloading the images used in the `README.md`
Now it's the fun part where `regexr` come in super handy!
Images in `markdown` can be in a few different formats, including `html`. This is a few examples of how I used images in my `README.md` files.
I have never really paid much attention to how I put images in it, so they are often in the same line, with wrong spacings, with or without alternative text, sometimes relative paths, sometimes a full url, sometimes even from external websites!

```markdown
![Blynk App](Blynk1.jpg) ![Blynk App](/assets/gabryxx7/img/GitHub/ShrekIntruderAlert/Blynk2.jpg)

<img  alt="The Tower Logo" width="250" src="https://github.com/Gabryxx7/TheTower/blob/master/Textures/thetower1.png"/><br/>

<img src='https://github.com/Gabryxx7/TheTower/blob/master/Textures/thetower2.png' alt="The Tower Logo" width="250"/> <img src='https://github.com/Gabryxx7/TheTower/blob/master/Textures/thetower3.png' alt="The Tower Logo" width="250"/> 

<img alt="Gabryxx7 | Instagram" height="100px" src="http://gmarini.com/assets/gabryxx7/img/photos/202006/79841217_555270635156572_8260864494112333405_n.jpg" />

![Screenshot](tinderai1.png)

![](tinderai2.png)

![](https://github.com/Gabryxx7/TheTower/blob/master/Textures/thetowerasd.png)

```
Now let's say we want to download all of these images on our computer and then maybe reference them in the same `README.md` we downloaded earlier, but with their new path in our computer. Now that sounds like a mess! We need to extract the image filename, understand whether it's relative to the repository or not, and then even replace its occurrences with the new local path.
Man that's a lot of different patterns, how to deal with all of this?

Luckily we have our "friends" the regular expressions. It took me around an hour to get the right expression and I saved it here for future references (RegExr)[regexr.com/5a6b1].

```python
IMG_REGEXR = "(?:!\[[^\]]*\]\(([^\)]*)\))+|(?:<img\s.*?src=(?:'|\")([^'\">]+)(?:'|\"))"
```
Now that looks like some sort of alien language, does it? Let's break it down.
Before that, a quick explanation on regexp.

## How do regular expression work
Regular Expressions are used to define patterns in text. The idea is to define a pattern and then execute it on your string or document, and it will return you all the "matches" or occurrences of that pattern in your string/document.

They have a few important special features and characters, I'll go through the most common ones:

- `.`: The dot is a special characters than it matches **ANY** character except for a new line. This means that it will return as a match anything: spaces, commas, letters, digits, tabs etc...
- `|`: either/or, `a|b` matches either an `a` or a `b` but not both
- `\.` `\\`: Matches the actual character, in this case the actual dot and the actual forward slash respectively, no special meaning.
- `\w \d \s`: These three match a letter, a digit and a whitespace respectively
- `\W \D \S`: These three match anything BUT a letter, a digit and a whitespace respectively
- `*` `+` `?`: These two tell how many times you want a character to be matches, respectively: 0 or more, 1 or more, 0 or 1
- `[]`: Matches any one of the characters inside the square brackets. `[ab]` matches either a single `a` or a single `b` separately as separate matches.
- `[^]` Matches any character except for the one inside. `[^ab]` matches anything but a single `a` or a single `b`
- `[-]`: Matches any character in the range. `[a-g]` will match ay character between `a` and `g` separately, this is the same as `\w`. `[0-9]` will match any character between `0` and `9` separately, this is the same as `\d`

So we can now do something simple like `.*` which matches anything up to a new line. Running this will just tell us whether there is a match or not in the string. And well, this will always be true, even nothing will return `true` because the `*` matches 0 or more occurrences of `.`.
`gabriele` will match the word gabriele for instance. Another example is `[^a]+` which matches any character which is not an `a` but at least once.

An important features are groups, so that we can define a sequence of character
- `()` Everything in brackets is a "capture group". Every pattern found inside the capture group can be referenced after running the expression
and it's very useful to reference certain parts of the pattern you want to extract
- `(?:)` This is a non-capturing group, same as before but cannot be referenced, well what's the point then? You might ask. This is useful to define repetitions of a sub-pattern or characters

That's pretty much it for now, let's break down the regex above:

## RegEx to match markdown image sources
First of all, the expression is divided in two by the pipe character `|`, the first one matches the markdown for images, which is in the form of `![]()` while the second one matches the html `<img src=... />`.

- Markdown `(?:!\[[^\]]*\]\(([^\)]*)\))+`
    - `(?:`: Everything is surrounded by a non-capturing group
    - `!\[`: match an exclamation mark and an open square bracket
    - `[^\]]*`: MAtches anything up to a closed square bracket, there can also be nothing to match (so an empty square brackets `[]`)
    - `\]\(`: We are not at the closed square bracket, so let's match it and look for the open bracket
    - `([^\)]*)`: Now we are inside the round brackets and we need to capture the image url (or path). So this is a capture group and it matches any character up to a close round bracket `[^\)]`, it can also be empty thanks to the `*`.
    - `\)`: Now we are up to the closed round bracket, so let's match it
    - `)`: Closure of the non-capturing group
    - `+`: This one is important, it matches the whole pattern we just defined in the non-capturing group, at least once. This is important in case we have two images in the same line such as `![](test.png) ![caption](test2.png)`. This will retuurn both `test.png` and `test2.png`

- HTML `(?:<img\s.*?src=(?:'|\")([^'\">]+)(?:'|\"))`
    - `(?:`: Everything is surrounded by a non-capturing group
    - `<img`: Matches the open html image tag
    - `\s.*?`: Matches any amount of empty spaces
    - `src=`: Matches the source attribute in the html image tag
    - `(?:'|\")`: This is a non-capturing group and it matches either a `'` or a `"` quotation mark, we are opening the source string
    - `([^'\">]+)`: This is a capturing group and it matches anything but  a `'` or a `"` quotation mark
    - `(?:'|\")`: This is a non-capturing group and it matches either a `'` or a `"` quotation mark to close the source string
    - `)`: Closure of the non-capturing group


### Wrapping up
So there you have it, now we can use the `re` python package to match all of these in our `README.md` and replace the captured group with the new file's local path

```python
def download_and_replace(match):
    global first_image
    print(match.group(0))
    if match.group(1) is not None:
        cap_group = match.group(1).strip()
    else:
        cap_group = match.group(2).strip()
    url = ""
    if len(cap_group) > 0:
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

...

  readme_text = re.sub(IMG_REGEXR, download_and_replace, readme_text) # Calling a function for each match which will download the img and replace the path in the markdown file
  
...
```
The function is fairly simple but has a few catches:
- First we need to get our captured image path/url:
    - `match.group(0)` represents the **WHOLE** pattern, not just the captured groups
    - `match.group(1)` reference the first capture group (the markdown images)
    - `match.group(2)` reference the second capture group (the html images)
- If the input is not empty then we can keep going
    - If it's a link there will be `http` in the string
    - We cannot download images from github links, so we have to convert those to `raw.githubusercontent.com` links
    - If it's not a link then we concatenate the raw github link with the repository full name
- Now that we have our link we can send a request and download the binary blob
- Once we downloaded the file we just need to make sure the path exists, and write the content to our disk
- We then return the replacement for the **whole** match, this includes also the non-capturing group. So what we do is return the whole match but we substitute the captured group with the now file's local path

We then return the edited `README.md` output to the for loop to then write everything to the new `README.md` file with the `yaml` header.


So the final code looks something like this:

```python
from github import Github
import requests
import oyaml
import re
import os
from urllib.parse import urlparse

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


with open(("github_credentials.yaml"), "r") as cf:
    cred = oyaml.safe_load(cf)
g = Github(cred['username'], cred['password'])

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
    if "workshop" not in repo.name.lower():
        if 'gabryxx7' in repo.owner.login.lower() and not repo.fork:
            print(repo.name)
            try:
                print(repo.get_readme().download_url)
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
                            readme_text = re.sub(IMG_REGEXR, download_and_replace, readme_text)

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
```


And there you have it! A little python script to scrape your own github repository data and export their `README.md` as jekyll markdown posts, and their images in the correct jekyll `assets` folder.