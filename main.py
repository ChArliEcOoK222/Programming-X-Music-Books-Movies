# Required libraries
import requests
import openai
from openai import OpenAI

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

# Storing my top movies
top_movies = ["T2 Trainspotting - Danny Boyle", "Trainspotting - Danny Boyle", "The Perks of Being a Wallflower - Stephen Chbosky", "The Breakfast Club - John Hughes", "Tunnel Rave - Tony Infante", "500 Days of Summer - Mark Webb", "The Madness of King George - Nicholas Hytner", "Django Unchained - Quentin Tarantino", "Almost Famous - Cameron Crowe", "Nuremberg - James Vaanderbilt", "Spike Island - Mat Whitecross"]

# Storing my books
top_books = ["Open Water - Caleb Azumah Nelson", "We Begin at the End - Chris Whitaker", "Tomorrow, and Tomorrow, and Tomorrow - Gabrielle Zevin"]

# Choice of what to generate
choice = input("Do you need albums, movies, or books? ").lower()

# Using this to generate output based on user preference
if choice == "albums":
    # Using GPT to match the user's artists, movies and books to new albums
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": f"I have used Last FM to find similar artists to my Top 50 artists from the last month. I am providing you with a list of these artists, my favorite films, and my favorite books. Find the best albums by these artists which match the themes of these movies and books. I aim to discover new music every month so give me enough albums to last a month, as I think listening to albums is a dying skill when artists intend you to listen to their albums and not their compilations. Albums tell a story. I am also trying to move away from indie and britpop landfill as I feel that lots of music nowadays just sounds the same, we as a society lack genuinely good music like old times. Give me a clear and concise response that consists of nothing but a list of albums, where each album is from a different artist, no text other than a list of albums please: {similar_artists}, {top_movies}, {top_books}"}],
        max_tokens=4096,
        n=1
    )
    # Accessing the message content of the output and saving it to a variable
    response_message = response.choices[0].message.content
    print(response_message)
elif choice == "movies":
    # Using GPT to match the user's artists, movies and books to new albums
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": f"Based on the matching themes from the following list of my top 50 artists, my favorite films, and my favorite books match the main themes of all of these with movies. I aim to discover new movies every month. Give me the top 5 movies you recommend for me, based on my taste profile. These movies do not necessarily have to be music-themed too just because I like music. Give me a clear and concise response that consists of nothing but a list of movies: {top_artists}, {top_movies}, {top_books}"}],
        max_tokens=4096,
        n=1
    )
    # Accessing the message content of the output and saving it to a variable
    response_message = response.choices[0].message.content
    print(response_message)