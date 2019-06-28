import requests
import json
import urllib.parse

TMDB_API = "https://api.themoviedb.org/3"

class TMDB_Handle:
  def __init__(self, api_key, language, debug=False):
    self.__api_key = api_key
    self.__language = language
    self.__debug = debug

  def search_movie(self, query, year="any", page=1):
    url_params = { "query" : query, "page" : page, "language" : self.__language, "include_adult" : False }
    if year != "any":
      url_params["year"] = year
    content = self.__get("/search/movie", url_params)
    if content:
      return content["results"]
    else:
      return []
  
  def get_movie_details(self, id):
    url_params = { "append_to_response" : "credits,alternative_titles", "language" : self.__language }
    content = self.__get("/movie/" + str(id), url_params)
    return content
  
  def getConfiguration(self):
    content = self.__get("/configuration")
    return content

  def __handle_response(self, response):
    content = json.loads(response.content)
    if response.ok:
      self.__info("received : " + str(response.text))
      return content
    else:
      self.__error("(code " + str(content["status_code"]) + ") " + str(content["status_message"]))
      return None

  def __get(self, endpoint, url_params={}, filter_language=True, filter_adult=True):
    url_params["api_key"] = self.__api_key
    keys = sorted(url_params.keys())
    url_params_string = "?"
    for key in keys:
      url_params_string += str(key) + "=" + urllib.parse.quote(str(url_params[key]))
      if key != keys[-1]:
        url_params_string += "&"
    url = TMDB_API + endpoint + url_params_string
    self.__info("requesting url : " + str(url))
    response = requests.get(url)
    content = self.__handle_response(response)
    return content
  
  def __info(self, message):
    if self.__debug:
      print("[INFO]  TMDB API - " + str(message))

  def __error(self, message):
    print("[ERROR] TMDB API - " + str(message))