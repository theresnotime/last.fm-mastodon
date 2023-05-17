import config
import requests
from mastodon import Mastodon


def getNowPlaying():
    url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={config.LAST_FM_USERNAME}&api_key={config.LAST_FM_API_KEY}&format=json&limit=1"
    r = requests.get(url, headers={"Accept": "application/json"}).json()
    track = r["recenttracks"]["track"][0]
    if "@attr" in track:
        if track["@attr"]["nowplaying"] == "true":
            artist = track["artist"]["#text"]
            track_name = track["name"]
            url = track["url"]
            return {"artist": artist, "track_name": track_name, "url": url}
        else:
            print("Nothing currently playing")
            return False


def post_mastodon(status):
    mastodon = Mastodon(access_token=config.ACCESS_TOKEN, api_base_url=config.API_URL)
    mastodon.toot(status)


if __name__ == "__main__":
    now_playing = getNowPlaying()
    if now_playing:
        status = f"currently listening to [{now_playing['artist']} — {now_playing['track_name']}]({now_playing['url']})"
        post_mastodon(status)
        print(f"[posted]: {status}")
