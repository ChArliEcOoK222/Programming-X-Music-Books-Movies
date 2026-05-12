# How do I connect to last.fm API?
# How do I connect to letterboxd API?
# How do I connect to Goodreads API?
# How do I get my top artists, movies, and books?
# How do I get similar artists, movies and books?
# How do I theme match using OpenAI?

# Required libraries
import requests

# Parameters for each API
music_url = "https://ws.audioscrobbler.com/2.0/"
music_params = {
    "method": "user.gettopartists",
    "user": "cj_cook22",
    "api_key": "7fd857a9cfc3ae569900007a35e2359b",
    "format": "json",
    "limit": 100,         
    "period": "overall"    
}

# Function to access top artists
def artists():
    # Calling the last.fm API with the specific parameters
    response = requests.get(music_url, params=music_params)
    # Saving the output to a json file
    data = response.json()
    # Converting the json file to a list
    top_artists = [
        artist["name"]
        for artist in data["topartists"]["artist"]
    ]
    # Returning the top artists list
    return top_artists