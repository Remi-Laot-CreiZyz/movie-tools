#!/usr/bin/python3
# coding: utf-8

from optparse import OptionParser

import json

from helpers import Configuration
from helpers import TheMovieDatabase


TMDB = TheMovieDatabase.TMDB_Handle(Configuration.TMDB.get("api_key"), Configuration.TMDB.get("language"), Configuration.TMDB.isDebugOn())

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

def main():
  parser = OptionParser(usage="usage: %prog [options] directory [...directory]", version="%prog 1.0")
  (options, paths) = parser.parse_args()
  
  metadata = get_metadata("Jack+Reacher")
  if metadata:
    json_dump = json.dumps(metadata, indent=2)
    print(json_dump)

# ============================================================================== #

if __name__ == "__main__":
  main()