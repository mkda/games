# Meadow Memory

A picture-pairs game with all 18 LittleLeap friends, for ages 3–7 on tablets and phones.

## How it plays
- On the title screen, the friends parade along the bottom. Tap any of them to hear them say their name.
- Pick a tray: 3, 4 or 6 pairs.
- Turn two cards over. Each friend says "I'm <name>!" in their own studio voice when their card opens.
- When the two cards match, the pair sparkles and the friend says "You found me! Hooray!". When they don't match, the cards wiggle and turn back. Every third miss, the narrator says something encouraging.
- Clear the board and the friends dance under confetti. Then play again, or pick another tray.
- Pip and Pop look alike, so they never appear on the same board.

## Grown-ups corner
The grown-ups corner works the same way as in the race. A multiplication question opens a link to https://www.youtube.com/@Little-Leap-Studios. The game shows no ads and collects nothing.

## Files
- `index.html`: the whole game, with no build step.
- `assets/`: one picture per friend, taken from the studio pose libraries without stretching or cutting. Also the logo, the sprout used on the card backs, and the meadow plate.
- `voices/`: `<id>_name.mp3`, `<id>_found.mp3` and the narrator lines. All are made with the studio's Kokoro settings (voice, speed and pitch from `cast.json`, at -18 LUFS). `lines.json` lists the text of each line.
- `make_assets.py`: rebuilds `assets/` and `voices/` from `~/Movies/AI Kids Stories Studio` on the Mac.

## Changing things
- To add a friend, add them to `CHARS` in `make_assets.py` and to `CAST` in `index.html`, then rerun the script.
- To keep two lookalike friends off the same board, list them in `LOOKALIKES` in `index.html`.
