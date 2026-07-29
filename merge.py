import requests

PLAYLISTS = [
   ("JioHotstar",
    "https://jhsevetns-fhd.rtxcric.workers.dev/playlist.m3u"),
   ("SonyLiv",
    "https://raw.githubusercontent.com/doctor-8trange/zyphora/refs/heads/main/data/sony.m3u"),
   ("FanCode",
    "https://raw.githubusercontent.com/doctor-8trange/zyphx8/refs/heads/main/data/fancode.m3u"),
   ("ICC",
    "https://raw.githubusercontent.com/doctor-8trange/nexphi0/refs/heads/main/data/icc.m3u")
]

def get_playlist(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

merged = "#EXTM3U\n"

for label, url in PLAYLISTS:
    playlist = get_playlist(url)
    lines = playlist.splitlines()

    if lines and lines[0].startswith("#EXTM3U"):
        lines = lines[1:]

    for line in lines:
        if line.startswith("#EXTINF"):
            if 'group-title="' in line:
                start = line.find('group-title="') + 13
                end = line.find('"', start)
                old_group = line[start:end]
                line = line.replace(
                    f'group-title="{old_group}"',
                    f'group-title="{label} | {old_group}"'
                )
            else:
                line = line.replace(
                    "#EXTINF:",
                    f'#EXTINF:-1 group-title="{label}",',
                    1
                )

        merged += line + "\n"
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(merged)

print("Merged 4 playlists successfully!")
