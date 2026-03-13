# Hand Block Puzzle

Hand Block Puzzle is a gesture-controlled puzzle game where blocks are placed on a grid using hand movements detected by a webcam. The project uses computer vision and hand tracking to allow players to spawn and place blocks with a pinch gesture instead of using a mouse or keyboard.

---

## Overview

This project uses a webcam and real-time hand tracking to create an interactive puzzle game. The player controls the game using simple hand gestures.

Pinching the thumb and index finger together spawns a random block. Moving the hand moves the block, and releasing the pinch places the block onto the grid.

If a generated block cannot be placed anywhere on the grid, the game ends and the board resets.

---

## Features

* Real-time hand tracking using MediaPipe
* Pinch gesture detection
* Drag-and-drop block placement with hand movement
* Random block generation
* Row and column clearing system
* Score tracking
* High score tracking during gameplay
* Automatic reset when no valid moves remain
* Transparent overlay game interface

---

## How It Works

1. The webcam captures frames continuously.
2. MediaPipe detects the hand and predicts 21 landmark points.
3. The distance between the thumb tip and index finger tip is measured.
4. When the distance becomes small enough, the program detects a pinch gesture.
5. A random block is generated when the pinch begins.
6. The block follows the finger position.
7. When the pinch is released, the block is placed on the grid if the location is valid.

---

## Requirements

Python 3.9 – 3.11 recommended

Install the required packages:

```bash
pip install opencv-python mediapipe numpy
```

Download the MediaPipe hand tracking model:

```
hand_landmarker.task
```

Place this file in the same folder as `main.py`.

---

## Project Structure

```
hand_block_puzzle/
│
├── main.py
├── hand_landmarker.task
└── README.md
```

---

## Running the Game

Run the program with:

```bash
python main.py
```

The webcam window will open and the game will start.

Press **ESC** to close the application.

---

## Controls

| Gesture       | Action               |
| ------------- | -------------------- |
| Pinch fingers | Spawn a random block |
| Move hand     | Move the block       |
| Release pinch | Place the block      |
| ESC key       | Exit the game        |

---

## Game Rules

* Blocks must be placed on the 8×8 grid.
* Completing a full row or column clears it.
* Clearing lines increases the score.
* If a new block cannot be placed anywhere on the grid, the game ends.
* The board resets and the high score is updated if the current score is higher.

---

## Possible Improvements

Potential additions for future versions include:

* Block rotation using gestures
* Animated line clearing
* Sound effects
* Persistent high score storage
* Visual UI improvements
* Difficulty scaling

---

## Educational Purpose

This project demonstrates practical use of:

* Computer vision
* Real-time gesture recognition
* OpenCV rendering
* Game logic design
* Human–computer interaction using hand tracking


