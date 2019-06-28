
import re

class Parser:
  def __init__(self, regex, removeTokens):
    self.__regex = regex
    self.__removeTokens = removeTokens
    self.__parser = re.compile(self.__regex)

  def parse(self, string):
    parsing_results = self.__parser.search(string)
    if parsing_results:
      return self.__clean(parsing_results.group(0))
    else:
      return ""
  
  def __clean(self, string):
    tmp = string
    for token in self.__removeTokens:
      tmp = tmp.replace(token, " ")
    tmp = re.sub(" +", " ", tmp.strip())
    return tmp