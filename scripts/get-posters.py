#!/usr/bin/python3
# coding: utf-8

from optparse import OptionParser

import json
import os
import requests

from helpers import Configuration

# ============================================================================== #

image_endpoint = Configuration.TMDB.get("image_endpoint")
metadata_extension = ".metadata.json"

# ============================================================================== #

def main():
  parser = OptionParser(usage="usage: %prog [options] input [...input]", version="%prog 1.0")
  (options, paths) = parser.parse_args()
  if len(paths) < 1:
    print("wrong number of arguments (use --help to display usage and options)")
  else:
    movies = []
    for path in paths[0:]:
      for root, directories, files in os.walk(path):
        for file in files:
            if metadata_extension in file:
              movies.append({ "root" : root, "file" : file })
    count = 0
    for movie in movies:
      count += 1
      file = movie["file"]
      root = movie["root"]
      name = file[:-len(metadata_extension)]
      print("retrieving image for " + name + " (" + str(count) + "/" + str(len(movies)) + ")")
      with open(os.path.join(root, file), "r") as f:
        metadata = json.load(f)
        if metadata and "poster" in metadata:
          poster = metadata["poster"]
          if poster:
            poster_extension = poster.split(".")[-1]
            output = os.path.join(root, name + "." + poster_extension)
            image_url = image_endpoint + "/original" + poster
            with open(output, "wb") as out:
              response = requests.get(image_url)
              if response.ok:
                out.write(response.content)
              else:
                print("could not retrieve " + image_url)


# ============================================================================== #

if __name__ == "__main__":
  main()
