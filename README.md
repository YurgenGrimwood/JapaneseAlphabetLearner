# Japanese alphabet learner

This is a project I made because I wanted an extension for chrome where I could slowly but surely learn Japanese kanji by adding them to a flashcard ish system.
In addition I thought I'd add the ability to brush up on hiragana and katakana as well.

This project is a screwed up Svelte application that compiles into the public folder to make a working extension for Chrome.
It takes the extension settings from the extension folder, and the scripts from src. The background and injection scripts are really just leftovers, but the main script imports the Svelte component App, which can be written like a normal Svelte application.
Why did I do it like this? No reason in particular, I just wanted data-binding...

## Commands

Build to public once:
```bash
npm run build
```
Builds, and rebuilds on change:
```bash
npm dev
```
Builds, and rebuilds on change:
```bash
npm start
```

Dunno why there's two different ones, leftover from boilerplate.


## Final comments

This was mostly written between 1am and 8am on different days.
The code is both messy, repetetive and in heavy need of both refactoring and a new UX.
Am I gonna do it? Probably not.
