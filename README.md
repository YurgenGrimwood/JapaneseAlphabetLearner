# Japanese alphabet learner

This is a project I made because I wanted an extension for chrome where I could slowly but surely learn Japanese kanji by adding them to a flashcard ish system.
In addition I thought I'd add the ability to brush up on hiragana and katakana as well.

This project is a screwed up Svelte application that compiles into the public folder to make a working extension for Chrome.
It takes the src folder and compiles it into a build folder, into the public folder.
It also takes any files from the extension folder and puts them in the public folder.
If you want your script to access any files, they will need to end up in the public folder, but this folder will be overwritten by the extension folder, so put it in there.

The main script imports the Svelte component App, which can be written like a normal Svelte application.
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

## Final comments

This was mostly written between 1am and 8am on different days.
The code is both messy, repetetive and in heavy need of both refactoring and a new UX.
Dependencies probably should get an update too.
Am I gonna do it? Probably not.
