# Journalify by Annabel Ng, Annabelle Park, and Rachel Xiao


<p align="center">
  <img src="https://github.com/rachelxiao907/Journalify/blob/main/journalify_logo.png">
</p>


## Description
Struggling to find the perfect song at the end of the day? Can’t quite put a finger on your emotions?

Introducing Journalify, your new favorite tool for soundtracking your day. Write your daily journal entry on our website and Journalify will generate a Spotify track based on your entry’s mood. No more endless scrolling: Journalify takes you directly to the Spotify track and saves your entries (and songs!) for each day.


## Launch Codes:

1. Clone this repository: `git clone https://github.com/rachelxiao907/Journalify.git`
2. Cd into the repo directory: `cd journalify`
3. Install the required modules: `pip install -r requirements.txt`
4. Log in to your Spotify account [here]('https://developer.spotify.com/') and create an app [here]('https://developer.spotify.com/dashboard/applications')
- Export your Spotipy client ID and secret key
- `export SPOTIPY_CLIENT_ID=<id from dashboard>`
- `export SPOTIPY_CLIENT_SECRET=<secret key>`
5. Cd into app directory: `cd app`
6. Start the Flask server: `python3 __init__.py`
7. Run local host in a browser `https://127.0.0.1:5000/`
