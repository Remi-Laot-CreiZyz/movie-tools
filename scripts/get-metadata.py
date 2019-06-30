#!/usr/bin/python3
# coding: utf-8

from optparse import OptionParser

import json
import time
import os

from helpers import Configuration
from helpers import TheMovieDatabase


TMDB = TheMovieDatabase.TMDB_Handle(Configuration.TMDB.get("api_key"), Configuration.TMDB.get("language"), Configuration.TMDB.isDebugOn())

MOVIE_EXTENSIONS = Configuration.loadExtensions("movie")
SUBTITLE_EXTENSIONS = Configuration.loadExtensions("subtitle")

PARSERS = Configuration.loadParsers()

# ============================================================================== #

def get_metadata(query, year="any"):
  results = TMDB.search_movie(query, year)
  if len(results) > 0:
    details = TMDB.get_movie_details(results[0]["id"])
    if details:
      metadata = {
        "title"              : details["title"],
        "tmdb_id"            : details["id"],
        "imdb_id"            : details["imdb_id"],
        "overview"           : details["overview"],
        "original_language"  : details["original_language"],
        "release_date"       : details["release_date"],
        "vote_average"       : details["vote_average"],
        "poster"             : details["poster_path"],
        "genres"             : [],
        "spoken_languages"   : [],
        "cast"               : [],
        "crew"               : [],
        "alternative_titles" : []
      }

      for genre in details["genres"]:
        metadata["genres"].append(genre["name"])

      for person in details["credits"]["cast"]:
        metadata["cast"].append({
          "character" : person["character"],
          "name"      : person["name"],
        })

      for person in details["credits"]["crew"]:
        metadata["crew"].append({
          "job"         : person["job"],
          "department"  : person["department"],
          "name"        : person["name"]
        })
      
      for title in details["alternative_titles"]["titles"]:
        metadata["alternative_titles"].append({
          "iso_3166_1" : title["iso_3166_1"],
          "title"      : title["title"]
        })
      return metadata
    else:
      return None
  else:
    return None

# ============================================================================== #

def parse(string, groupname):
  values = {}
  if groupname in PARSERS:
    for key, parsers in PARSERS[groupname].items():
      for parser in parsers:
        s = parser.parse(string)
        if s:
          values[key] = s
          break
  if ("year" in values) and ("title" in values) and (values["year"] in values["title"]):
    values["title"] = values["title"].split(values["year"])[0].strip()
  if "title" in values:
    return values
  else:
    return {}

# ============================================================================== #

def main():
  parser = OptionParser(usage="usage: %prog [options] input [...input]", version="%prog 1.0")
  (options, paths) = parser.parse_args()
  if len(paths) < 1:
    print("wrong number of arguments (use --help to display usage and options)")
  else:
    movies = []
    movie_files = []
    for path in paths[0:]:
      for root, directories, files in os.walk(path):
        # find movie and subtitle files in the directory
        for file in files:
          for ext in MOVIE_EXTENSIONS:
            if ext in file:
              movie_files.append({ "root" : root, "file" : file})
    count = 0
    # parse movie filenames
    for movie in movie_files:
      count += 1
      movie_details = parse(movie["file"], "movie")
      if "title" in movie_details:
        print("retrieving metadata (" + str(count) + "/" + str(len(movie_files)) + ")")
        time.sleep(0.500)
        # print(json.dumps(movie_details, indent=2))
        metadata = get_metadata(movie_details["title"], movie_details["year"] if "year" in movie_details else "any")
        ext = movie["file"].split(".")[-1]
        output = os.path.join(movie["root"], movie["file"][:-len(ext)] + "metadata.json")
        with open(output, "w") as f:
          f.write(json.dumps(metadata, indent=2))

# ============================================================================== #

if __name__ == "__main__":
  main()