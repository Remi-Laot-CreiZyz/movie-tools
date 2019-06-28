import json
import sys
import os

sys.path.append(os.path.dirname(__file__))
import Parser

class Config:
  def __init__(self, group):
    self.__debug = False
    self.__group = group
    self.__data = {}

  def load(self):
    with open(os.path.dirname(__file__) + "/../../config.json", "r") as f:
      content = json.load(f)
      if "debug" in content:
        self.__debug = content["debug"]
      if self.__group in content:
        self.__data = content[self.__group]
      return self
  
  def isDebugOn(self):
    return self.__debug | ("debug" in self.__data and self.__data["debug"])
  
  def data(self):
    return self.__data

  def get(self, key):
    if key in self.__data:
      return self.__data[key]
    else:
      return None

__PARSERS = Config("regex_parsers").load()
__EXTENSIONS = Config("extensions").load()

def loadParsers():
  parsers = {}
  for groupname, group in __PARSERS.data().items():
    parsers[groupname] = {}
    for name, configs in group.items():
      parsers[groupname][name] = list(map(lambda cfg : Parser.Parser(cfg["regex"], cfg["remove"]), configs))
  return parsers
    
def loadExtensions(groupname):
  extensions = __EXTENSIONS.get(groupname)
  if not extensions:
    extensions = []
  return extensions

TMDB = Config("TheMovieDatabase").load()