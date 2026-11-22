# Meadow Memory

A picture-pairs game with all 18 LittleLeap friends, for ages 3–7 on tablets and phones.

## How it plays
- On the title screen, the friends parade along the bottom. Tap any of them to hear them say their name.
- Pick a level on the path of 8 trays. Each tray is a small picture of its board (cream = card showing, orange = card face down), with 1-5 difficulty dots and a short label for grown-ups (Very easy ... Hardest). The next level to try glows, and the level and its label stay at the top of the board while playing.
  1. All 6 cards showing: tap two friends that match.
  2. One card is face down.
  3. Two cards are face down.
  4. Three cards are face down (one of each pair, so the friend to find is always visible).
  5. Small memory: 3 pairs, all face down.
  6. Bigger memory: 4 pairs.
  7. Big memory: 6 pairs.
  8. Big memory with poses: Tomo, Zippy and Olly in two different drawings each. Only the same drawing matches.
  9. Expert: 16 cards (8 pairs).
  10. Expert with poses: 16 cards, Tomo, Zippy and Olly in 2-3 drawings each.
  11. Master: 20 cards, with the twins Pip and Pop on purpose.
  12. Champion: 20 cards, all poses (Tomo, Zippy and Olly in 3-4 drawings each).
  13. All friends: all 18 friends, 36 cards, every card showing.
  14. All friends: all 18 friends, 36 cards, all face down.
- A tapped card lifts up with a blue edge. Tap it again to put it back.
- After a win: play again, go to the next level (arrow), or back to the path.
- Turn two cards over. Each friend says "I'm <name>!" in their own studio voice when their card opens.
- When the two cards match, the pair sparkles and the friend says "You found me!". When they don't match, the cards wiggle and turn back. Every third miss, the narrator says something encouraging.
- Clear the board and the friends dance under confetti. Then play again, or pick another tray.
- Pip and Pop look alike, so they never appear on the same board.

## Grown-ups corner
The grown-ups corner works the same way as in the race. A multiplication question opens a link to https://www.youtube.com/@Little-Leap-Studios. The game shows no ads and collects nothing.

## Files
- `index.html`: the whole game, with no build step.
- `assets/`: one picture per friend, plus `pose_*.webp` (copied from the race game's pose drawings) for level 8, taken from the studio pose libraries without stretching or cutting. Also the logo, the sprout used on the card backs, and the meadow plate.
- `voices/`: `<id>_name.mp3`, `<id>_found.mp3` and the narrator lines. All are made with the studio's Kokoro settings (voice, speed and pitch from `cast.json`, at -18 LUFS). `lines.json` lists the text of each line.
- `make_assets.py`: rebuilds `assets/` and `voices/` from `~/Movies/AI Kids Stories Studio` on the Mac.

## Changing things
- To add a friend, add them to `CHARS` in `make_assets.py` and to `CAST` in `index.html`, then rerun the script.
- To keep two lookalike friends off the same board, list them in `LOOKALIKES` in `index.html`.
- To change the levels, edit `LEVELS` in `index.html` (`pairs`, `cover` = cards face down, -1 for all, `poses`). The pose drawings for level 8 are listed in `POSES`.
- Music (22 Nov 2026): the LittleLeap Studios score from the "Little Leap" sound, 432 Hz episode cues, in `music/`: `morning` on the level path, `cheeky` while playing, `tada` sting on a win. Mastered at -20 LUFS, streamed, and ducked under the voices. Made from `_studio/library/music/remix_v7/432/` on the Mac.
- Home screen (22 Nov 2026): the whole cast stands together on the meadow grass as a group photo (taller friends in the back row), at the series size canon (CANON.md, Zippy = 380). Johnatan, Julia and Tara have no canon height yet (placeholders 300 / 400 / 330 in `HEIGHT`). Tap a friend to hear their name.
- Little Sugar, Marco, Silvia, Muriel and Tara had a pale ground patch under their feet in the studio master drawings; it was removed from `assets/` (22 Nov 2026). Re-running `make_assets.py` brings it back, so cut it again or skip those five.
- Icons (22 Nov 2026): drawn in the game's own style (ink outline, meadow colours): a little cottage with a leaf roof for Home, an orange speaker with green waves for Sound (grey with a cross when off), and a grown-up with a child for the grown-ups corner.
- Tries (22 Nov 2026): every turn (two cards) adds a paw print next to the level tag, with the number; the last 10 paws are shown.
- Level passed (22 Nov 2026): a celebration screen (a friend from the board dances, 1-3 stars pop in, the tries are shown, "You found all the friends!"), then the next level starts by itself after 5 s; tapping anywhere goes on at once. Stars: 3 for at most 1.5 turns per pair, 2 for at most 2.5, else 1. After level 12 the screen says "Memory Champion!" and waits for a tap, then goes to the level path. Stars earned show on the path trays for this visit only (nothing is stored).
- Music and channel (22 Nov 2026): the grown-ups corner links to the channel and to the album (DistroKid HyperFollow page, all stores) and describes the music as gentle, healing orchestral music tuned to 432 Hz.
- Corners (22 Nov 2026): grown-ups corner bottom left; Credits (storybook icon) bottom right: game, YouTube channel, the album Little Leap by MKDA (432 Hz), AI note, © 2026 LittleLeap Studios, ℗ © 2026 MKDA. Credits has no links (children can open it); the links stay behind the grown-ups sum.
- Rotation (22 Nov 2026): each board takes the friends (and pose drawings) that have been on the fewest boards this visit, ties in random order, so all 18 friends come round before anyone repeats much (six small boards show all 18). Card positions, hidden cards and the dancing friend are random.
- Home music (22 Nov 2026): browsers allow sound only after a first touch, so the first tap anywhere starts "Good Morning, Meadow" on the home screen; it carries on over the level path and changes to "Tiptoe Adventure" on a board.
