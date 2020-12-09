# Fortune API

![Python application](https://github.com/lbacik/fortune-api/workflows/Python%20application/badge.svg)

This is simple REST API for fortune app: https://github.com/lbacik/fortune

## Usage

Probably the best way to check/use this app - is to utilize the docker image from
https://hub.docker.com/repository/docker/lbacik/fortune-api - just run:

    docker run --rm -p 127.0.0.1:8080:8080 lbacik/fortune-api

And you can start the fun:

    ➜  ~ http localhost:8080/fortune
    HTTP/1.1 200 OK
    Content-Length: 93
    Content-Type: application/json
    
    {
        "fortune": "Rotten wood cannot be carved.\n\t\t-- Confucius, \"Analects\", Book 5, Ch. 9\n"
    }
        
## API

Only GET requests are accepted for the time being. And there are two types of available requests possible:

    GET http://localhost:8080/fortune/<path>
    
Where the `<path>` part is optional - to random one fortune form pointed directory/file.

    GET http://localhost:8080/fortune/<path>?explore
    
Where the `<path>` part is optional (again :)) - to show the files in `path` or the fortunes in the file (if the 
`path` points to the file).

It is also possible to pass more than one source (as a source list, with probability) by POST request:

    POST http://localhost:8080/fortune
    Content-Type: application/json    
    
    {
      "sources": [
        {
          "path": "<path>>",
          "probability": <int>
        },
        {
          "path": "<path>",
          "probability": <int>
        },
        
        ...

      ]
    }

The `probability` can be 0 (it is the default in cli interface - it means that it will be calculated later by "equal divide" 
between all the sources with probability set to 0).

## Example

    ➜  ~ http 'localhost:8080/fortune?explore'
    HTTP/1.1 200 OK
    Content-Length: 435
    Content-Type: application/json
    
    [
        "tao",
        "education",
        "computers",
        "art",
        "humorists",
        "debian",
        "cookie",
        "men-women",
        "songs-poems",
        "pratchett",
        "pets",
        "law",
        "linuxcookie",
        "sports",
        "medicine",
        "fortunes",
        "startrek",
        "disclaimer",
        "science",
        "ascii-art",
        "ethnic",
        "platitudes",
        "perl",
        "definitions",
        "magic",
        "riddles",
        "politics",
        "zippy",
        "drugs",
        "linux",
        "work",
        "wisdom",
        "food",
        "kids",
        "goedel",
        "news",
        "love",
        "literature",
        "miscellaneous",
        "knghtbrd",
        "translate-me",
        "people",
        "paradoxum"
    ]

    ➜  ~ http 'localhost:8080/fortune/literature'
    HTTP/1.1 200 OK
    Content-Length: 77
    Content-Type: application/json
    
    {
        "fortune": "Reputation, adj.:\n\tWhat others are not thinking about you.\n"
    }

