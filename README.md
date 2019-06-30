# movie-tools

Simple tools I use to organize my movie collection

# Getting Started

## Install

To get the movie-tools scripts, just download this repository.

In order to run them, you will need to install `python3`.

Lastly, some scripts retrieve metadata from online services (The Movie Database project). To be able to use these features, make sure to enter a valid [TMDB API Key](https://developers.themoviedb.org/3/getting-started/introduction) in the `config.json` file.

## List your movies

List all movies present in a directory using the `list-files.py` script. It will scan the directory recursively, and ouput a JSON file listing all movies. In the process, specific informations about the movies are extracted from filenames using regular expressions (ex: `title` and `year`). You can modify the regular expressions used, or the type of files matched by `list-files.py` in the `config.json` file.

The `list-files.py` script will also try to find subtitle files present in the same folder as its movie. Only subtitle file that match **every** information extracted from movies are matched.

To run `list-files.py`:

```
list-files.py <outputFile> <dir> [...<dir>]
```

Example of a `config.json` file:

```
...
  "regex_parsers": {
    "movie" : {
      "title" : [
        { "regex" : "^((\\d+|[a-zA-Z\\']+)[\\.\\-\\s])*", "remove" : [ ".", "-", "BrRip", "EXTENDED", "THEATRICAL EDITION" ] }
      ],
      "year" : [
        { "regex" : "(19|20)\\d{2}", "remove" : [] }
      ]
    },
    "subtitle" : {
      "title" : [
        { "regex" : "^((\\d+|[a-zA-Z\\']+)[\\.\\-\\s])*", "remove" : [ ".", "-", "BrRip", "EXTENDED", "THEATRICAL EDITION" ] }
      ],
      "year" : [
        { "regex" : "(19|20)\\d{2}", "remove" : [] }
      ],
      "language" : [
        { "regex" : "[\\.\\-\\s](eng|ENG|Eng|fr|FR|Fr)[\\.\\-\\s]", "remove" : [ ".", "-" ] }
      ]
    }
  },
  "extensions": {
    "movie" :  [
      ".mp4",
      ".mkv"
    ],
    "subtitle" : [
      ".srt"
    ]
  }
...
```

To learn more about regular expressions, see [an introduction](https://www.aivosto.com/articles/regex.html) and [python3 regex doc](https://docs.python.org/3/howto/regex.html).

## Reorganize your movies

// TODO

# Where does the data come from ?

A great thanks to [The Movie Database](https://www.themoviedb.org/) and their amazing [API](https://developers.themoviedb.org/4/getting-started) ! They are responsible for every bit of metadata used by movie-tools.

![The Movie Database Logo](tmdb.png)
