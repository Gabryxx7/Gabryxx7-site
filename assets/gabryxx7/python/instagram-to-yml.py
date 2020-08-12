import json
import os
from datetime import datetime

class InstaPhoto:
  def __init__(self, title, filepath, caption, taken_at, location, url):
    self.title = title
    self.file = filepath
    self.caption = caption
    self.taken_at = taken_at
    self.location = location
    self.timestamp = datetime.fromisoformat(taken_at)
    self.url = url
  def __str__(self):
    return str(self.file)

date_to_filter = datetime.fromisoformat("2017-01-01T00:00:00+00:00")
print("TEST") 
instaphotos = [];
for f in os.scandir("."):
  if f.is_dir():
    print(f.path) 
    try:
      with open(f.path+'\media.json', encoding = 'cp850') as media:
        data = json.load(media)
        for photo_data in data["photos"]:         
          if len(instaphotos) > 0 and photo_data["taken_at"] == instaphotos[-1].taken_at:
            if not isinstance(instaphotos[-1].file, list):
              instaphotos[-1].file = [instaphotos[-1].file]
            instaphotos[-1].file.append(str(photo_data["path"]))
          else:
            if "location" in photo_data:
              instaphotos.append(InstaPhoto("", str(photo_data["path"]), str(photo_data["caption"]), photo_data["taken_at"], str(photo_data["location"]), "https://www.instagram.com/gabryxx7/"))
            else:
              instaphotos.append(InstaPhoto("", str(photo_data["path"]), str(photo_data["caption"]), photo_data["taken_at"], "", "https://www.instagram.com/gabryxx7/"))

    except FileNotFoundError: # parent of IOError, OSError *and* WindowsError where available
      print('No media.json in '+f.path)

instaphotos_filtered = list(filter(lambda x: x.timestamp >  date_to_filter, instaphotos))
instaphotos_filtered = list(filter(lambda x: len(x.caption.strip()) > 1, instaphotos_filtered))
instaphotos_filtered.sort(key=lambda x: x.timestamp, reverse=True)

with open("photos.yml", "w+", encoding = 'cp850') as yml_file:
  yml_file.write("preview_folder: /assets/gabryxx7/img/photos/\nfull_folder: /assets/gabryxx7/img/photos/\nphotos:")
  for photo in instaphotos_filtered:
    if not isinstance(photo.file, list):
      yml_file.write("\n  - file: "+str(photo.file.split("/",1)[1]))          
    else:
      yml_file.write("\n  - files: ")    
      for photo_file in reversed(photo.file):
        yml_file.write("\n    - "+str(photo_file.split("/",1)[1]))    
    yml_file.write("\n    title: " +str(photo.title))                       
    yml_file.write("\n    caption: |\n     "+str(photo.caption.replace("\n", "\n     ")))                         
    yml_file.write("\n    date: "+str(photo.timestamp.isoformat()))
    if len(str(photo.location)) > 1:                                         
      yml_file.write("\n    location: "+str(photo.location))                        
    yml_file.write("\n    url: "+str(photo.url))  

exit(1)