# Tetris-Pygame
Tetris with Pygame 

## Overview
This is the implementation of the Tetris game with Python's `Pygame` library. The grid is of `20` rows and `10` columns. At the beginning of the game or when a previous tetromino has settled, a new one will pop out from the top of the screen. The initial row can be any random one as long as the tetromino does not spill out of the screen. The player can move the tetrominoes with `arrow` keys and even make them move down faster using the `down arrow` key. The game can be paused by pressing the `p` key and restarted using the `s` key.

## Row vanishing
<div class="row">
  <img src="https://github.com/sbInfin1/Tetris-Pygame/blob/master/screenshots/before_vanish_35.JPG" width="360" height="540" title="before_vanish_35"/>
  <img src="https://github.com/sbInfin1/Tetris-Pygame/blob/master/screenshots/after_vanish_35.JPG" width="360" height="540" title="after_vanish_35"/>
</div>

Here, we can see a special case of row vanishing. When the complete tetromino (`T-shaped` pink color) was settled it could not move down because of its size being larger than the gap. But as soon as a row vanishes, the original `T-tetromino` is reduced to a smaller size as such it can now fit through the gap and settle below. But, instead it remains hanging in the air. This is not a bug, but many implementations of Tetris allow it to remain hanging.  

## More interesting cases of Row vanishing
<div class="row">
  <img src="https://github.com/sbInfin1/Tetris-Pygame/blob/master/screenshots/before_vanishing_36.JPG" width="360" height="540" title="before_vanish_35"/>
  <img src="https://github.com/sbInfin1/Tetris-Pygame/blob/master/screenshots/after_vanishing_36.JPG" width="360" height="540" title="after_vanish_35"/>
</div>
