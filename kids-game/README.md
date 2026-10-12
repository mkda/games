# AI Kids Play

A touch-first web game for ~7-year-olds featuring the AI Kids video characters. No reading needed:
instructions are spoken aloud, buttons are pictures, and there's no way to lose.

**Play:** open `index.html` in any phone or tablet browser (no install, no internet needed after loading).

## Games
- 🎈 **Balloon Pop**: tap floating character balloons; 20 pops = party.
- 🃏 **Memory Match**: find the 6 character pairs.
- 🔍 **Find the Friend**: hear a name, tap that character; 8 right = party.

## Adding the real characters
1. Put each character's picture (transparent PNG, roughly square) in `characters/`, e.g. `characters/luna.png`.
2. Edit the `CHARACTERS` list at the top of the `<script>` in `index.html`:
   ```js
   { name: "Luna", color: "#ff7ab8", image: "characters/luna.png" },
   ```
   `name` is what the game says out loud; `color` tints balloons. With `image: null` a placeholder face is drawn.

## Linking the YouTube channel
The 📺 button on the home screen opens a video corner with links to the AI Kids YouTube channel and videos.
It sits behind a grown-ups question (a multiplication sum), so kids can't leave the game for YouTube on their own.
Fill in the `CHANNEL` block near the top of the `<script>`: the channel `url` and a list of `videos`
(`id` is the part after `watch?v=`, `character` is which character stars in it).
Mark the channel's videos as "made for kids" in YouTube Studio; the game itself collects no data and has no ads.

## Google Labs playground
See [GOOGLE_LABS_PROMPT.md](GOOGLE_LABS_PROMPT.md) for a ready-to-paste prompt that builds the same game
in Google AI Studio / Gemini, so you can keep iterating there.
