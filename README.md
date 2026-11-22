# LittleLeap Studios games

Touch games for kids (ages 3–7) featuring the Meadow friends from the LittleLeap Studios YouTube channel.
We release one polished game at a time.

| Game | Based on | Folder |
|---|---|---|
| The Big Meadow Race | EP01 Zippy and Tomo: The Big Meadow Race | [`meadow-race/`](meadow-race/) |
| Meadow Memory | The whole cast, each saying their name | [`memory/`](memory/) |

Open `index.html` at the top of the repo to see the collection page, which links to every game.

## Play online (GitHub Pages)
- Collection: https://mkda.github.io/games/
- Meadow Memory: https://mkda.github.io/games/memory/ (installable, works offline)
- The Big Meadow Race: https://mkda.github.io/games/meadow-race/
- Meadow Memory privacy policy (used by the app stores): https://mkda.github.io/games/memory/privacy.html

Everything is self-contained: fonts (Fredoka, SIL OFL), pictures, voices and music are in each game's folder; nothing loads from other sites.
After changing any file in `memory/`, run `python3 memory/make_sw.py` (from inside `memory/`) to refresh the offline cache list.

Music in both games: the "Little Leap" album sound by MKDA, 432 Hz cues — https://distrokid.com/hyperfollow/mkda/little-leap

`GOOGLE_LABS_PROMPT.md` has a prompt for rebuilding or extending a game in Google AI Studio's Build mode.
