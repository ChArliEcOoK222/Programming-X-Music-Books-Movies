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

# Storing my top artists
top_artists = artists()

# Storing my top movies
top_movies = ["T2 Trainspotting - Danny Boyle", "Trainspotting - Danny Boyle", "The Perks of Being a Wallflower - Stephen Chbosky", "The Breakfast Club - John Hughes", "Tunnel Rave - Tony Infante", "500 Days of Summer - Mark Webb", "The Madness of King George - Nicholas Hytner", "Django Unchained - Quentin Tarantino", "Almost Famous - Cameron Crowe", "Nuremberg - James Vaanderbilt", "Spike Island - Mat Whitecross"]

# Storing my books
top_books = ["Open Water - Caleb Azumah Nelson", "We Begin at the End - Chris Whitaker"]

# Using GPT to match the user's artists, movies and books to new albums
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": f"Based on the following list of my top 50 artists, my favorite films, and my favorite books match the main themes of all of these with albums. I aim to discover new music every month, so the albums must not be from the same artist. Give me enough albums to last a month, as I think listening to albums is a dying skill. Give me a clear and concise response that consists of nothing but a list of albums: {top_artists}, {top_movies}, {top_books}"}],
    max_tokens=4096,
    n=1
)

# Accessing the message content of the output and saving it to a variable
response_message = response.choices[0].message.content
print(response_message)