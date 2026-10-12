# Prompt for the Google Labs / AI Studio playground

Paste the block below into Google AI Studio's **Build** mode (or Gemini Canvas, or any Google Labs app builder).
Before pasting, replace the character list with the real AI Kids characters, and upload their pictures
(transparent PNGs work best) so the builder can use them.

---

```
Build a mobile-first web game for 7-year-old kids, played on phones and tablets by touch only.

CHARACTERS (from our "AI Kids" videos; use the uploaded pictures for each one):
- Robo: blue, cheerful robot kid
- Luna: pink, curious and kind
- Ziggy: orange, silly and bouncy
- Pixel: green, loves puzzles
- Nova: purple, dreamy space fan
- Bolt: red, super fast

RULES FOR THE AUDIENCE
- No reading required: every instruction is spoken aloud (use the browser speechSynthesis API, friendly
  high pitch, slightly slow) and shown with icons, never with text-only buttons.
- Big tap targets (at least 72x72 px), no drag precision, no double-tap, no timers that punish.
- No losing: wrong taps give a gentle wiggle and "Try again!", never a game over.
- Bright, soft colors, rounded shapes, bouncy animations, happy sound effects (Web Audio API beeps are fine).
- No ads, no links out, no text input, no data collection.
- Works in portrait and landscape; disable pinch-zoom and page scrolling while playing.

GAMES (a home screen with four huge picture buttons, plus a home button on every game):
1. Balloon Pop: balloons in each character's color float up with the character's face on them.
   Tap to pop. A star counter goes up. 20 pops = confetti party, then it starts again.
2. Memory Match: 12 face-down cards (6 character pairs). Flip two; matches stay up and the character
   says their name. All pairs found = confetti party. A restart button with a 🔄 icon.
3. Find the Friend: the game says "Find Luna!" and shows 4 characters. Tap the right one to earn a star.
   Tapping the big picture at the top repeats the name. 8 stars = confetti party.
4. Video corner (📺 button): links to our YouTube channel <PASTE CHANNEL URL> and a grid of our videos
   (thumbnail + title, opening on YouTube). Put it behind a "grown-ups only" gate: a random multiplication
   sum (e.g. 7 × 8) answered on a number pad, so kids can't leave the game on their own.

On the home screen show all characters; tapping one makes them say "Hi! I'm <name>".
Put the character list in one array at the top of the code so I can add more characters easily.
Single page, no backend, no login.
```

---

## Ideas to iterate on in the playground

- "Add a fourth game where kids tap the character whose color matches a big paint splash."
- "Make each character say a catchphrase from the videos when they appear." (add the catchphrases)
- "Add background music that loops softly, with the sound button muting it too."
- "Add a sticker book screen where every party unlocks a new character sticker."
