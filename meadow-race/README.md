# The Big Meadow Race

LittleLeap Studios' first game, based on EP01 *Zippy and Tomo: The Big Meadow Race*.
For ages 3–7 on phones and tablets: no reading needed (the narrator speaks), one simple gesture, no way to lose.

**How it plays**
1. Big Oak start line: tap Judge Olly to blow the whistle. Zippy zooms off.
2. Press and hold anywhere to walk Tomo through the Meadow: flower path, Mushroom Woods (Snail says hello), Giggle Stream.
3. Tomo collects 10 strawberries on the way, and the game counts each one aloud.
4. Sunflower Hill: Zippy is napping, so Tomo tiptoes past.
5. Rainbow Bridge: Tomo breaks the ribbon, Olly whistles, Pip and Pop clap, Zippy arrives late and cheers Tomo on.
   Everyone chants "Slow and steady wins the race!" and the child counts the strawberries with Tomo.

**Grown-ups corner:** the 📺 button opens a multiplication-sum gate, then a link to the
LittleLeap Studios YouTube channel. Kids can't leave the game on their own. No ads, no sign-in, nothing stored.

## Files
- `index.html`: the whole game (canvas + Web Audio). Open it from any web server.
- `assets/`: drawings from the cast pose libraries (`_studio/cast/poses/<CHAR>/poses`) and EP01 background plates
  (`_studio/library/places/meadow-ep01`), resized for the web.

To try it locally: `cd meadow-race && python3 -m http.server`, then open http://localhost:8000.

## Voices
`voices/` holds the cast's own voices. 18 lines are taken straight from the EP01 recordings, like Olly's
"On your marks... get set... Go!", Zippy's "I'm the fastest... carrots..." and Pip and Pop's "Slow and steady!".
The other 23 lines are new game lines, such as instructions and the counting, made with the studio's Kokoro settings
for each character from `cast.json`. Re-run `python3 make_voices.py` on the Mac after changing lines;
`voices/lines.json` lists every line and where it came from.

## Changing it
- Channel link: `CHANNEL_URL` near the top of the script.
- Story lines and scene order: the `play()` function, one block per place.
- Sizes of the characters: the `SPR` table.
