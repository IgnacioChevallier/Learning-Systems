# Apply graph Tsetlin machines on board game winner prediction

I have also uploaded C-code to generate random games. 
Your task is to predict the winner of a game:

- At the end of the game
- Two moves before the end
- Five moves before the end

# Instructions

Run with the default board size (11x11):

```
./hex
```

Optionally change board size by defining BOARD_DIM at compile time:

```
gcc -DBOARD_DIM=7 -o hex hex.c
make
./hex
```

## What it does
It plays many random games (10,000,000 loop iterations).
Each move is placed randomly on an empty cell.
When a player connects their respective sides, it declares a winner.
If the win happened with many empty cells left (e.g., number_of_open_positions >= 75), it prints the winner and the final board state using X and O.