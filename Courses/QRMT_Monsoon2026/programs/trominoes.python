"""
Animated Recursive Tromino Tiling
=================================

Demonstrates both the tiling AND the recursive control flow.

Required external library:
    matplotlib

Install with:
    pip install matplotlib

Controls:
    Press ENTER in the terminal to advance to the next conceptual step.

For automatic animation instead, set:
    INTERACTIVE = False
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import random

# ============================================================
# PARAMETERS
# ============================================================

N = 3                    # Board is 2^N x 2^N
SIZE = 2 ** N
#MISSING = (1, 1)         # (row, column) of original missing square

MISSING = (
    random.randrange(SIZE),
    random.randrange(SIZE)
)

INTERACTIVE = True       # True: press ENTER for every step
DELAY = 0.7              # Used only when INTERACTIVE = False



# ============================================================
# GLOBAL DISPLAY DATA
# ============================================================

trominoes = []
step_number = 0

fig, ax = plt.subplots(figsize=(8, 8))


# ============================================================
# PAUSE
# ============================================================

def pause():
    """Wait for the lecturer to advance the animation."""

    plt.draw()

    if INTERACTIVE:
        input("Press ENTER to continue...")
    else:
        plt.pause(DELAY)


# ============================================================
# DRAWING
# ============================================================

def draw_board(message="",
               active_board=None,
               next_board=None):

    ax.clear()

    # --------------------------------------------------------
    # Basic board
    # --------------------------------------------------------

    for r in range(SIZE):
        for c in range(SIZE):

            ax.add_patch(
                Rectangle(
                    (c, SIZE - 1 - r),
                    1, 1,
                    fill=False,
                    edgecolor="gray",
                    linewidth=0.7
                )
            )

    # --------------------------------------------------------
    # Original missing square
    # --------------------------------------------------------

    mr, mc = MISSING

    ax.add_patch(
        Rectangle(
            (mc, SIZE - 1 - mr),
            1, 1,
            facecolor="black",
            edgecolor="black"
        )
    )

    # --------------------------------------------------------
    # Trominoes already placed
    # --------------------------------------------------------

    cmap = plt.colormaps["tab20"]

    for i, tromino in enumerate(trominoes):

        colour = cmap(i % 20)

        for r, c in tromino:

            ax.add_patch(
                Rectangle(
                    (c, SIZE - 1 - r),
                    1, 1,
                    facecolor=colour,
                    edgecolor="black",
                    linewidth=1
                )
            )

        # Number each tromino
        avg_r = sum(r for r, c in tromino) / 3
        avg_c = sum(c for r, c in tromino) / 3

        ax.text(
            avg_c + 0.5,
            SIZE - avg_r - 0.5,
            str(i + 1),
            ha="center",
            va="center",
            fontsize=8
        )

    # --------------------------------------------------------
    # Highlight the CURRENT recursive problem
    # --------------------------------------------------------

    if active_board is not None:

        top, left, size = active_board

        ax.add_patch(
            Rectangle(
                (left, SIZE - top - size),
                size, size,
                fill=False,
                edgecolor="red",
                linewidth=4
            )
        )

    # --------------------------------------------------------
    # Highlight the NEXT recursive sub-problem
    # --------------------------------------------------------

    if next_board is not None:

        top, left, size = next_board

        ax.add_patch(
            Rectangle(
                (left + 0.08,
                 SIZE - top - size + 0.08),
                size - 0.16,
                size - 0.16,
                fill=False,
                edgecolor="blue",
                linewidth=4,
                linestyle="--"
            )
        )

    # --------------------------------------------------------
    # Axes
    # --------------------------------------------------------

    ax.set_xlim(-0.2, SIZE + 0.2)
    ax.set_ylim(-0.2, SIZE + 0.2)

    ax.set_aspect("equal")

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(message, fontsize=13)

    plt.draw()
    plt.pause(0.01)


# ============================================================
# PLACE ONE TROMINO
# ============================================================

def place_tromino(squares):
    trominoes.append(squares)


# ============================================================
# RECURSIVE TILING ALGORITHM
# ============================================================

def tile(top, left, size, missing, depth=0, name="ROOT"):

    global step_number

    indent = "    " * depth

    # ========================================================
    # PAUSE 1:
    # We have ENTERED a recursive problem
    # ========================================================

    step_number += 1

    print()
    print(indent + "=" * 45)
    print(indent + f"ENTER {name}")
    print(indent + f"Board size     : {size} x {size}")
    print(indent + f"Missing square : {missing}")
    print(indent + f"Recursion depth: {depth}")
    print(indent + "=" * 45)

    draw_board(
        message=(
            f"Enter {name}: {size} x {size} problem\n"
            f"Recursion depth = {depth}"
        ),
        active_board=(top, left, size)
    )

    pause()


    # ========================================================
    # BASE CASE
    # ========================================================

    if size == 2:

        squares = [
            (r, c)
            for r in range(top, top + 2)
            for c in range(left, left + 2)
            if (r, c) != missing
        ]

        place_tromino(squares)

        print(indent + "BASE CASE")
        print(indent + "Place one tromino and return.")

        draw_board(
            message=(
                f"{name}: BASE CASE\n"
                f"Tile the remaining three squares"
            ),
            active_board=(top, left, size)
        )

        pause()

        print(indent + f"RETURN from {name}")

        return


    # ========================================================
    # DIVIDE INTO FOUR QUADRANTS
    # ========================================================

    half = size // 2

    middle_row = top + half
    middle_col = left + half

    centre = {
        "TL": (middle_row - 1, middle_col - 1),
        "TR": (middle_row - 1, middle_col),
        "BL": (middle_row,     middle_col - 1),
        "BR": (middle_row,     middle_col)
    }


    # Determine quadrant containing missing square

    mr, mc = missing

    if mr < middle_row and mc < middle_col:
        missing_quadrant = "TL"

    elif mr < middle_row and mc >= middle_col:
        missing_quadrant = "TR"

    elif mr >= middle_row and mc < middle_col:
        missing_quadrant = "BL"

    else:
        missing_quadrant = "BR"


    print(indent +
          f"Missing square lies in quadrant {missing_quadrant}")


    # ========================================================
    # PLACE CENTRAL TROMINO
    # ========================================================

    central_tromino = [
        centre[q]
        for q in ("TL", "TR", "BL", "BR")
        if q != missing_quadrant
    ]

    place_tromino(central_tromino)


    # ========================================================
    # PAUSE 2:
    # Central tromino has created FOUR deficient sub-problems
    # ========================================================

    print(indent + "Place central tromino.")
    print(indent + "Now there are FOUR smaller deficient boards.")

    draw_board(
        message=(
            f"{name}: central tromino placed\n"
            "Four smaller sub-problems have been created"
        ),
        active_board=(top, left, size)
    )

    pause()


    # ========================================================
    # Determine the missing square for each sub-problem
    # ========================================================

    new_missing = {}

    for q in ("TL", "TR", "BL", "BR"):

        if q == missing_quadrant:
            new_missing[q] = missing
        else:
            new_missing[q] = centre[q]


    # ========================================================
    # Description of four recursive sub-problems
    # ========================================================

    subproblems = [

        (
            "TL",
            top,
            left
        ),

        (
            "TR",
            top,
            left + half
        ),

        (
            "BL",
            top + half,
            left
        ),

        (
            "BR",
            top + half,
            left + half
        )
    ]


    # ========================================================
    # FOUR RECURSIVE CALLS
    # ========================================================

    for quadrant, sub_top, sub_left in subproblems:

        # ====================================================
        # PAUSE 3:
        # Highlight EACH sub-problem BEFORE recursion
        # ====================================================

        print()
        print(indent +
              f"Next recursive call: {quadrant}")

        print(indent +
              f"Missing square for {quadrant}: "
              f"{new_missing[quadrant]}")

        draw_board(
            message=(
                f"{name}: about to recurse into {quadrant}\n"
                f"Next problem: {half} x {half}"
            ),
            active_board=(top, left, size),
            next_board=(sub_top, sub_left, half)
        )

        pause()


        # ====================================================
        # THE ACTUAL RECURSIVE CALL
        # ====================================================

        tile(
            top=sub_top,
            left=sub_left,
            size=half,
            missing=new_missing[quadrant],
            depth=depth + 1,
            name=quadrant
        )


        # ====================================================
        # PAUSE 4:
        # Show that control has RETURNED from the sub-problem
        # ====================================================

        print(indent +
              f"Returned from {quadrant}")

        draw_board(
            message=(
                f"Returned from {quadrant}\n"
                f"Continue solving {name}"
            ),
            active_board=(top, left, size)
        )

        pause()


    # ========================================================
    # RETURN FROM CURRENT RECURSIVE CALL
    # ========================================================

    print(indent + f"All four sub-problems of {name} are complete.")
    print(indent + f"RETURN from {name}")


# ============================================================
# RUN THE DEMONSTRATION
# ============================================================

plt.ion()

draw_board(
    message=(
        f"Initial {SIZE} x {SIZE} board\n"
        "Black square is missing"
    ),
    active_board=(0, 0, SIZE)
)

pause()

tile(
    top=0,
    left=0,
    size=SIZE,
    missing=MISSING,
    depth=0,
    name="ROOT"
)


# ============================================================
# FINISHED BOARD
# ============================================================

draw_board(
    message=(
        f"Complete tiling\n"
        f"{len(trominoes)} trominoes"
    )
)

plt.ioff()
plt.show()


# ============================================================
# VERIFY THE COUNT
# ============================================================

expected = (SIZE * SIZE - 1) // 3

print()
print("=" * 50)
print("FINISHED")
print("=" * 50)
print(f"Board size      : {SIZE} x {SIZE}")
print(f"Missing square  : {MISSING}")
print(f"Trominoes used  : {len(trominoes)}")
print(f"Expected number : {expected}")
