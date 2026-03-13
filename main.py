import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import random
import math

# -----------------------------
# SETTINGS
# -----------------------------

GRID = 8
PADDING = 80
PINCH_THRESHOLD = 45

COLOR_GRID = (200,200,200)
COLOR_FILLED = (0,200,0)
COLOR_VALID = (0,255,0)
COLOR_INVALID = (0,0,255)

SHAPES = [
[[1]],
[[1,1]],
[[1],[1]],
[[1,1,1]],
[[1],[1],[1]],
[[1,1],[1,1]],
[[1,0],[1,1]],
[[0,1],[1,1]]
]

HAND_LINES = [
(0,1),(1,2),(2,3),(3,4),
(0,5),(5,6),(6,7),(7,8),
(5,9),(9,10),(10,11),(11,12),
(9,13),(13,14),(14,15),(15,16),
(13,17),(17,18),(18,19),(19,20),
(0,17)
]

# -----------------------------
# LOAD MEDIAPIPE MODEL
# -----------------------------

base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

# -----------------------------
# GAME STATE
# -----------------------------

grid = [[0]*GRID for _ in range(GRID)]

score = 0
highscore = 0

holding = False
current_shape = None
last_pinch = False

cursor_x = 0
cursor_y = 0

# -----------------------------
# GAME FUNCTIONS
# -----------------------------

def valid_place(shape,row,col):

    for r in range(len(shape)):
        for c in range(len(shape[0])):

            if shape[r][c]:

                gr=row+r
                gc=col+c

                if gr<0 or gc<0 or gr>=GRID or gc>=GRID:
                    return False

                if grid[gr][gc]==1:
                    return False

    return True


def place(shape,row,col):

    for r in range(len(shape)):
        for c in range(len(shape[0])):

            if shape[r][c]:
                grid[row+r][col+c]=1


def clear_lines():

    global score

    rows=[]
    cols=[]

    for r in range(GRID):
        if all(grid[r][c]==1 for c in range(GRID)):
            rows.append(r)

    for c in range(GRID):
        if all(grid[r][c]==1 for r in range(GRID)):
            cols.append(c)

    for r in rows:
        for c in range(GRID):
            grid[r][c]=0

    for c in cols:
        for r in range(GRID):
            grid[r][c]=0

    score += (len(rows)+len(cols))*10


def moves_possible(shape):

    for r in range(GRID):
        for c in range(GRID):

            if valid_place(shape,r,c):
                return True

    return False


def reset_game():

    global grid,score,highscore

    if score > highscore:
        highscore = score

    grid=[[0]*GRID for _ in range(GRID)]
    score=0

# -----------------------------
# CAMERA
# -----------------------------

cap=cv2.VideoCapture(0)

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    ret,frame=cap.read()
    if not ret:
        break

    frame=cv2.flip(frame,1)

    h,w,_=frame.shape

    overlay=frame.copy()

    grid_size=min(w,h)-PADDING*2
    cell=grid_size//GRID

    startx=(w-cell*GRID)//2
    starty=(h-cell*GRID)//2

    # -----------------------------
    # HAND DETECTION
    # -----------------------------

    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    mp_image=mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result=detector.detect(mp_image)

    pinch=False

    if result.hand_landmarks:

        for hand in result.hand_landmarks:

            pts=[]

            for lm in hand:

                x=int(lm.x*w)
                y=int(lm.y*h)

                pts.append((x,y))

                cv2.circle(frame,(x,y),4,(0,255,100),-1)

            for a,b in HAND_LINES:
                cv2.line(frame,pts[a],pts[b],(255,100,100),2)

            thumb=pts[4]
            index=pts[8]

            cursor_x=int(cursor_x*0.7 + index[0]*0.3)
            cursor_y=int(cursor_y*0.7 + index[1]*0.3)

            cv2.circle(frame,(cursor_x,cursor_y),10,(0,255,255),-1)

            dist=math.dist(thumb,index)

            if dist < PINCH_THRESHOLD:
                pinch=True

    # -----------------------------
    # SPAWN BLOCK
    # -----------------------------

    if pinch and not last_pinch and not holding:

        new_shape=random.choice(SHAPES)

        if not moves_possible(new_shape):

            reset_game()

        else:

            holding=True
            current_shape=new_shape

    # -----------------------------
    # PLACE BLOCK
    # -----------------------------

    if not pinch and last_pinch and holding:

        col=(cursor_x-startx)//cell
        row=(cursor_y-starty)//cell

        if valid_place(current_shape,row,col):

            place(current_shape,row,col)
            clear_lines()

        holding=False
        current_shape=None

    last_pinch=pinch

    # -----------------------------
    # DRAW GRID
    # -----------------------------

    for r in range(GRID):
        for c in range(GRID):

            x=startx+c*cell
            y=starty+r*cell

            cv2.rectangle(overlay,(x,y),(x+cell,y+cell),COLOR_GRID,1)

            if grid[r][c]==1:

                cv2.rectangle(
                    overlay,
                    (x+4,y+4),
                    (x+cell-4,y+cell-4),
                    COLOR_FILLED,
                    -1
                )

    # -----------------------------
    # BLOCK PREVIEW
    # -----------------------------

    if holding and current_shape:

        col=(cursor_x-startx)//cell
        row=(cursor_y-starty)//cell

        good=valid_place(current_shape,row,col)

        color=COLOR_VALID if good else COLOR_INVALID

        for r in range(len(current_shape)):
            for c in range(len(current_shape[0])):

                if current_shape[r][c]:

                    x=startx+(col+c)*cell
                    y=starty+(row+r)*cell

                    cv2.rectangle(
                        overlay,
                        (x,y),
                        (x+cell,y+cell),
                        color,
                        -1
                    )

    # -----------------------------
    # UI BLEND
    # -----------------------------

    frame=cv2.addWeighted(overlay,0.45,frame,0.55,0)

    cv2.putText(frame,f"Score: {score}",
    (30,50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.2,
    (255,255,255),
    3)

    cv2.putText(frame,f"High Score: {highscore}",
    (30,90),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255,255,255),
    2)

    cv2.putText(frame,
    "Pinch to spawn block",
    (30,h-30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (220,220,220),
    2)

    cv2.imshow("Hand Block Puzzle",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()