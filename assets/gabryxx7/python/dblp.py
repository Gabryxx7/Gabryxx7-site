import dblplib as dblp
import oyaml as yaml

def getAuthor(name):
    ret = name
    if 'arini' in name:
        ret = '<ins><strong>'+str(name)+'</strong></ins>'
    return ''.join(i for i in ret if not i.isdigit()).strip() # removing numbers and trimming spaces
#do a simple author search for michael ley
authors = dblp.search('Gabriele Marini')
author = authors[0]
print(author.name)
extras = []
obj = []
for p in author.publications:
    p_obj = {}
    p_obj['name'] = str(p.title)
    p_obj['type'] = str(p.type)
    p_obj['releaseDate'] = str(p.mdate)
    p_obj['year'] = str(p.year)
    p_obj['month'] = str(p.month)
    p_obj['journal'] = str(p.journal)
    p_obj['editors'] = [str(e) for e in p.editors]
    p_obj['publisher'] = str(p.booktitle)
    p_obj['pages'] = str(p.pages)
    p_obj['publisherDBLP'] = str(p.publisher)
    p_obj['school'] = str(p.school)
    p_obj['authors'] = [getAuthor(str(a)) for a in p.authors]
    p_obj['website'] = str(p.ee)
    obj.append(p_obj)

with open('extra_publications.yml', "r") as pf:
    extras = yaml.safe_load(pf)
with open('publications.yml', "w") as pf:
    yaml.dump(extras, pf)
    yaml.dump(obj, pf)