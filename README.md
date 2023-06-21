#CONNECT 4

####VIDEO DEMO: https://youtu.be/fQ5FFsJQDTc

####DESCRIPTION: 

This is a Connect 4 game designed by Nick Diplos for Harvard University's CS50.

This game can be played both through the web or through a terminal (using 'X' and 'O' as the symbols by default).

Below are details about each py file and the purpose. 

**helpers.py**

This contains global variables that are used throughout. Here, the default height and width of the board as well as the symbols can be changed. It also includes the default values for calculating the board score. 

**main.py** 
This is the main file that runs when playing throughthe terminal. Objects for each player are created here and each turn is taken through this file.

**board.py** 
This file ceates a board with each 'slot' being an object. It contains functions to display the board, it also contains a special function that will print a desired attribute of a slot for testing purposes if required.

The board has several attributes: 

1.  ID: Every slot has a unique ID
2.  State: A slot's state is -1 if the slot is unavilable, 0 if empty but cannot be moved into on the next move, or 1 if it's empty can be moved into on the next move
3. p1_win and p2_win: The global variable PLAYER_WINS (in helpers) can be used to access these attributes more easily. The defualt value is 0, meaning the slot, at least currently, can not result in a win. A value of 2 means that this slot an result in a win for a particular player (i.e p1_win = 2 means player 1 can win). A value of 1 means it will result in 4-in-a-row but this is not easily achievable. For example:

 
 <p>`|_|_|X|X|X|O|_| `</p>
 <p>`|_|_|O|O|O|X|_| `</p>


While 'X' has got a potential 4-in-a-row (second slot on the first row), this is unlikely to be achieved as it would require an 'X' symbol in the slot below. Unless 'O' is forced into the slot above or does not play optimally, 'O' will then block this score. 

4. Display: This is what should be displayed to a user (i.e '_', 'X' or 'O')


**connect.py**
This file is mostly for actions that are are involved with making a move on the board (i.e choosing a column)

**lines.py**
This file contains functions that will generate 'lines' in the board. It's important during searching to consider all the horizontal, vertical and diagonal lines and consider each slot. One of the more complex functions in this file is 'connctions'.

Let's look at this function further:
> connections(all_lines, allowed_states, allowed_displays, allowed_p1win, allowed_p2win, length)

Suppose we would want to search for the following on the board: 
All lines of length 4, where 'O' or '_' are the only displayed attributes. 

connections(all_lines, [-1, 0, 1], ['O', '_',], [0, 1, 2], [0, 1, 2], 4)

Now suppose we want to search for the following on the board:
All lines of length 5, which MUST contain an 'X' but can contain any other symbol too.

connections(all_lines, [-1, 0, 1], ['X', '*', '_', 'O'], [0, 1, 2], [0, 1, 2], 4)

The addition of '*' means that it will only show lines that always include an 'X'.


**evaluating.py**

This file is for evaluating the state of a board, including score. To calculate the board score (which is done at the start of a players turn before they have moved), the program considers:

1.  If the current player can win
2.  For the current counters for a player on the board, the number of potential wins.
3.  The number of 'lines' are then calculated:
For the example below, there are 4 potential wins for 'O' when considering the horizontal (i.e the 'O' could be the last counter in the row, second to last, second or first)

 <p>`|_|_|_|_|_|_|_| `</p>
<p></p> `|_|_|_|O|_|_|_| `</p>

There are then two diagonal lines which could include 'O' (with a positive and negative gradient)

There is also 1 vertical line.

So overall there are 7 lines. 

A score is then generated based on this users the scores defined in helpers.

4. This same calculation is done for the opposing player and is substracted from the current players score. 

5. There is a final check to see whether there are some important moves, for example, can the next player win and will that need to be blocked?


**AI.py**

This is used when it's a computers turn and using alpha-beta pruning. 

**app.py**
This contains all the flask functions that to show the program on the web

**gameclass.py**
A game via the web is created via a 'game' object that stores important data, this is tracked using 'session' 


###Future Implementations/Considerations
1. The scoring is complex, most likely far too complex. I would then to simplify this, as well as the searching within lines.py, at a later point. 
2. Javascript animations would improve the user experience when playing on the web
4. There is supposed to be sounds when a user moves into a slot (which you may hear in certain browsers!). This is a known bug that will need to be fixed in the future. 
