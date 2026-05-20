# How can I automatically save each recommendation on the app itself?
# How can I run this in a bash script?

# Required libraries
import requests
from letterboxdpy.list import List
import openai
from openai import OpenAI
import json

# Creating a new OpenAI client from the API key
client = OpenAI(
    api_key=""
)

# Parameters for last.fm API
music_url = "https://ws.audioscrobbler.com/2.0/"
music_params = {
    "method": "user.gettopartists",
    "user": "",
    "api_key": "",
    "format": "json",
    "limit": 50,         
    "period": "1month"    
}

# Parameters for GraphQL API for Hardcover
books_url = "https://api.hardcover.app/v1/graphql"
query = """
query {
  me {
    user_books(where: {status_id: {_eq: 3}}) {
      rating
      book {
        title
      }
    }
  }
}
"""

# Parameters for Spotify API
spotify_url = "https://api.spotify.com/v1/search"
# Adding spotify auth helpers
def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": "",
            "client_id": "",
            "client_secret": "",
        }
    )

    return response.json()["access_token"]

# Saving my access token
access_token = get_access_token()

spotify_headers = {
    "Authorization": f"Bearer {access_token}"
}

# Function to access top artists
def top_artists():
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

# Storing my top artists
top_artists = top_artists()

# Function to get similar artists
def similar_artists():
    # List to store similar artists
    similar_artists = []
    # Getting similar artists by iterating over the list of top artists
    for artist_name in top_artists:
        # Parameters for the API
        params = {
        "method": "artist.getsimilar",
        "artist": artist_name,
        "api_key": "",
        "format": "json",
        "limit": 10
        }
        # Calling the API
        response = requests.get(music_url, params=params)
        # Saving the output to a json file
        data = response.json()
        # Saving the artists names to the list
        for artist in data["similarartists"]["artist"]:
            similar_artists.append(artist["name"])
    # Returning the similar artists list
    return similar_artists

# Storing the similar artists
similar_artists = similar_artists()

# Function to access top movies
def top_movies():
    # Using letterboxdpy to web scrape movies from my list of favourites
    list_instance = List("cjc22", "my-favourites")
    # Lazy scraping
    list_instance.movies
    # Saving the movie names to the list
    top_movies = [
        movie["name"]
        for movie in list_instance["_movies"].values()
    ]
    # Returning the top movies list
    return top_movies

# Storting the top movies
top_movies = top_movies()

# Function to access read books
def top_books():
    # Calling the GraphQL API with the specific parameters
    response = requests.post("https://api.hardcover.app/v1/graphql",
    headers={
        "Authorization": f"Bearer "
    },
    json={"query": query}
    )   
    # Saving the output as a json
    result = response.json()
    # Accessing and saving the book titles
    titles = [
        entry["book"]["title"]
        for entry in result["data"]["me"][0]["user_books"]
    ]
    # Saving the titles
    return titles

# Storing the top books
top_books = top_books()

# Choice of what to generate
choice = input("Do you need albums, movies, or books? ").lower()
# Variables to store recommendations
album_recs = []

# Album input is given
if choice == "albums":
    # Using GPT to match the user's artists, movies and books to new albums
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": f"I have used Last FM to find similar artists to my Top 50 artists from the last month. I am providing you with a list of these artists, my favorite films, and my favorite books. Find the best albums by these artists which match the themes of these movies and books. I aim to discover new music every month so give me enough albums to last a month, as I think listening to albums is a dying skill when artists intend you to listen to their albums and not their compilations. This means around 30 albums, give or take. Albums tell a story. I am also trying to move away from indie and britpop landfill as I feel that lots of music nowadays just sounds the same, we as a society lack genuinely good music like old times. Give me a clear and concise response that consists of nothing but a list of albums, where each album is from a different artist, no text other than a list of albums please. This must be in structured JSON format consisting of attributes artist and album, making downstream API calls much easier: {similar_artists}, {top_movies}, {top_books}"}],
        max_tokens=4096,
        n=1
    )
    # Accessing the message content of the output and saving it to a variable
    response_message = response.choices[0].message.content
    # Cleaning the output for Spotify API
    clean = (
            response_message
            .replace("```json", "")
            .replace("```", "")
            .strip()
    )
    album_recs = json.loads(clean)

# Movie input is given
elif choice == "movies":
    # Using GPT to match the user's artists, movies and books to new movies
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": f"Based on the matching themes from the following list of my top 50 artists, my favorite films, and my favorite books match the main themes of all of these with movies. I aim to discover new movies every month. Give me the top 5 movies you recommend for me, based on my taste profile. These movies do not necessarily have to be music-themed too just because I like music. I also cannot have already watched them. Give me a clear and concise response that consists of nothing but a list of movies: {top_artists}, {top_movies}, {top_books}"}],
        max_tokens=4096,
        n=1
    )
    # Accessing the message content of the output and saving it to a variable
    response_message = response.choices[0].message.content
    print(response_message)
# Book input is given
elif choice == "books":
    # Using GPT to match the user's artists, movies and books to new books
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": f"Based on the matching themes from the following list of my top 50 artists, my favorite films, and my favorite books match the main themes of all of these with books. I like books which take me on a journey and make me feel alive. Give me the top 5 books you recommend for me, based on my taste profile. These books do not necessarily have to be music-themed too just because I like music. Give me a clear and concise response that consists of nothing but a list of books: {top_artists}, {top_movies}, {top_books}"}],
        max_tokens=4096,
        n=1
    )
    # Accessing the message content of the output and saving it to a variable
    response_message = response.choices[0].message.content
    print(response_message)
# Invalid input is given
else:
    print("Invalid input")

# Function to get the IDs of each album
def get_albumID():
    # List to store IDs
    album_ids = []
    # Iterating over each item in the JSON
    for rec in album_recs:
        # Accessing the Spotify API
        query = f"{rec['album']} {rec['artist']}"
        response = requests.get(
            spotify_url,
            headers=spotify_headers,
            params={
                "q":query,
                "type": "album", 
                "limit": 5
            }
        )

        # Saving the output
        data = response.json()
        # Saving the IDs
        items = data["albums"]["items"]
        album_id = items[0]["id"]
        album_ids.append(album_id)
    # Returning the IDs
    return album_ids

# Storing album IDs
album_IDs = get_albumID()

# Function to save these albums to my library
def save_album():
    # Arguments for the API
    uris = ",".join([f"spotify:album:{i}" for i in album_IDs])
    url = "https://api.spotify.com/v1/me/library"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    # Calling the API
    response = requests.put(
        url,
        headers=headers,
        params={"uris": uris}
    ) 

# Saving the albums
save_album()