#!/usr/bin/python3
# coding: utf-8

from optparse import OptionParser

import json
import os

# ============================================================================== #

def main():
  parser = OptionParser(usage="usage: %prog [options] output input [...input]", version="%prog 1.0")
  (options, paths) = parser.parse_args()
  if len(paths) < 2:
    print("wrong number of arguments (use --help to display usage and options)")
  else:
    movies = []
    for path in paths[1:]:
      with open(path, "r") as f:
        movies += json.load(f)

    output_path = paths[0]
    for movie in movies:
      if movie["title"] != "title_not_recognized":
        new_name = movie["title"]
        if "year" in movie:
          new_name += " (" + str(movie["year"]) + ")"
        ext = movie["file"].split(".")[-1]
        output_dir = os.path.join(output_path, new_name)
        # create output directory
        if not os.path.exists(output_dir):
          os.mkdir(output_dir)
        # move movie
        new_movie_path = os.path.join(output_dir, new_name + "." + ext)
        if os.path.exists(movie["file"]) and not os.path.exists(new_movie_path):
          os.rename(movie["file"], new_movie_path)
        elif not os.path.exists(new_movie_path):
          print("could not move " + movie["file"] + " to " + new_movie_path)
        for subtitle in movie["subtitle_matches"]:
          ext = subtitle["file"].split(".")[-1]
          suffix = ""
          if "language" in subtitle:
            suffix += "." + subtitle["language"].lower()
          else:
            suffix += ".eng"
          # move subtitles
          new_subtitle_path = os.path.join(output_dir, new_name + suffix + "." + ext)
          if os.path.exists(subtitle["file"]) and not os.path.exists(new_subtitle_path):
            os.rename(subtitle["file"], new_subtitle_path)
          else:
            print("could not move " + subtitle["file"] + " to " + new_subtitle_path)

# ============================================================================== #

if __name__ == "__main__":
  main()