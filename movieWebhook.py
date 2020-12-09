from urllib.request import urlopen, Request
import requests
import json
import credentials

def tmdbAPIMovie(id):
    tmdbData = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + str(credentials.tmdbapikey) + "&language=en-US")
    tmdbData = tmdbData.json()
    return(tmdbData)

def tmdbAPIDirector(id):
    tmdbData = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "/credits?api_key=" + str(credentials.tmdbapikey) + "&language=en-US")
    tmdbData = tmdbData.json()
    for item in tmdbData["crew"]:
        if (item["job"] == "Director"):
            dirName = item["name"]
            break
    return dirName

def writeFile(val):
    with open("counter", "r+") as f:
        f.seek(0)
        f.write(str(val))
        f.truncate()
    return None


headers = {
  'Content-Type': 'application/json',
  'trakt-api-version': '2',
  'trakt-api-key': credentials.traktclientid
}

request = Request('https://api.trakt.tv/users/jivandabeast/lists/weekly-movies/items', headers=headers)
response_body = urlopen(request).read()
data = json.loads(response_body)

with open("counter") as f:
    storedVal = f.readline()

i = 0

for item in data:
    if (str(i) == str(storedVal)):
        rawData = tmdbAPIMovie(item["movie"]["ids"]["tmdb"])
        movie = rawData["title"]
        altMovie = rawData["original_title"]
        director = tmdbAPIDirector(item["movie"]["ids"]["tmdb"])
        poster = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + rawData["poster_path"]
        i += 1
        writeFile(i)
        break
    i += 1

data = {}
data["content"] = "@everyone \n\n This weeks movie is: **" + movie + "**"
data["username"] = "Movie Bot"
data["embeds"] = []
embed = {}
embed["title"] = movie + " " + str(rawData["release_date"])
embed["description"] = "Directed by: " + director + "\n\n" + str(rawData["overview"])
embed["color"] = "7499559"
embed["footer"] = {}
embed["image"] = {}
embed["footer"]["icon_url"] = "https://static.netify.ai/logos/t/m/d/tmdb/icon.png"
embed["footer"]["text"] = "From the Movie Database"
embed["image"]["url"] = poster
data["embeds"].append(embed)

result = requests.post(credentials.discordwebhook, data=json.dumps(data), headers={"Content-Type": "application/json"})

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))