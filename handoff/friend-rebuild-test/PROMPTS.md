# Selected original prompts

The text inside each fenced block is reproduced verbatim, including spelling, capitalization, punctuation, and measurement notation. Codex-generated attachment wrappers and local file paths are not part of the prompt text and are recorded separately in `ASSET-MANIFEST.md`.

Messages that only made sense in response to an intermediate model, preview, or prior assistant wording were omitted. Setup, Git, documentation, and tooling instructions were also omitted because they do not describe the object to be built. Their durable physical requirements are consolidated in `DIMENSIONS-AND-REQUIREMENTS.md` without exposing the existing CAD implementation.

## Prompt 1 — initial request

```text
Initialize proejct.  I want to design a 3d-printable tablet stand for my 2024 Onn 8" tablet.  Before jumping ton CAD rendering, let's just chat to make sure you understand what I want.  ASCII art rendering is good enough for now. Iy's goinh to  permanently sit on top of a 32mm OD tube - I've done some test prints and a 32.2mm ID cylinder wraps the tube perfectly tight.  then I want the table to rest at a 10o angle on top of that tube.  I'm not exactly sure how I want the tablet to be held regarding design but it should be enought material to be sturdy but not suffocate the tablet inside.  a front bezel would be cool but not required - talk to ne about tradeoffs.  likewise, if the table just sits in a tray stable enough to hold it, that's good enough, but if we want to wrap all sides, that's cool too.  Must have routing for a slim USB-C cable on the right hand side center of the tablet.  USBC cable is .7mm wide and flat and the slim connector to the tablet only sticks out 0.256mm deep. see image. also attaching a CAD rendering of the table for dimensions. for style I'm thinking simple and sleek.
```

Original attachments: `assets/tinker.obj`, `assets/obj.mtl`, and `assets/codex-clipboard-e3e4e085-fe62-40d4-a042-9b47d908e367.png`.

## Prompt 2 — final tilt correction

```text
Make sure to record all dimensions and decision as we go along. Remember this in is this project. 

Also looks like tablet is 10o angle from laying flat on a table (horizontal). I want it 10o angle cverticle almost like a kiosk
```

## Prompt 3 — corner treatment, insertion, and cable relief

```text
filet the outside corners a bit so it's not so sharp. Also I want the usb cable in the case and the tablet to slide into it.  I'm ok if it doesn't line up perfectly and I have to plug it in and then slide but the right hand side of the case should be closed with groove for usb cable to plug remember.  remember that the cable is flat at the end and only extends 0.256" from the tablet - it's very low profile
```

## Prompt 4 — physical right-angle cable photo

```text
 here's the end of the USB-C cable I have. I bought that right angle to wrap immediately around the back fo the tablet, exiting in a groove in/on the collet on the tube so it's largely hidden until it reaches the exit of the holder.
```

Original attachment: `assets/IMG_7233 Large.jpeg`.

## Prompt 5 — downstream cable construction

```text
after what you see in that pic it just convertes to a 3.45mm round braided wire.
```
