#!/usr/bin/python3
# coding: utf-8

from optparse import OptionParser

import json
import os

from helpers import Configuration

# ============================================================================== #

MOVIE_EXTENSIONS = Configuration.loadExtensions("movie")
SUBTITLE_EXTENSIONS = Configuration.loadExtensions("subtitle")

PARSERS = Configuration.loadParsers()

TITLE_NOT_RECOGNIZED = "title_not_recognized"

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

def match_movie_with_subtitle(movie_details, subtitle_details):
  is_same = "title" in subtitle_details
  for key, value in movie_details.items():
    is_same = is_same and (key in subtitle_details and value == subtitle_details[key])
  return is_same

# ============================================================================== #

def main():
  parser = OptionParser(usage="usage: %prog [options] output input [...input]", version="%prog 1.0")
  (options, paths) = parser.parse_args()
  if len(paths) < 2:
    print("wrong number of arguments (use --help to display usage and options)")
  else:
    movies = []
    for path in paths[1:]:
      for root, directories, files in os.walk(path):
        movie_files = []
        subtitle_files = []
        # find movie and subtitle files in the directory
        for file in files:
          for ext in MOVIE_EXTENSIONS:
            if ext in file:
              movie_files.append(file)
          for ext in SUBTITLE_EXTENSIONS:
            if ext in file:
              subtitle_files.append(file)
        # parse movie filenames
        for movie in movie_files:
          movie_details = parse(movie, "movie")
          if not "title" in movie_details:
            movie_details["title"] = TITLE_NOT_RECOGNIZED
          subtitle_matches = []
          for subtitle in subtitle_files:
            subtitle_details = parse(subtitle, "subtitle")
            if match_movie_with_subtitle(movie_details, subtitle_details):
              subtitle_details["file"] = os.path.join(root, subtitle)
              subtitle_matches.append(subtitle_details)
          movie_details["subtitle_matches"] = subtitle_matches
          movie_details["file"] = os.path.join(root, movie)
          movies.append(movie_details)
    print("found " + str(len(movies)) + " movies")
    with open(paths[0], "w") as f:
      f.write(json.dumps(movies, indent=2))

# ============================================================================== #

if __name__ == "__main__":
  main()