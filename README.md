# Assignment Two : Fun with the Board Game Pente 

## Info

Run on port 8095 to evaluate. 

## Collaborators

Bryce Bernstein, Emilie Morocco, Hannah Scooler

## Goal

Your high-level goal is to create a **player evaluation system** that allows you to play a large number of games between two Pente players (or one player playing itself) to evaluate their relative strength. 

Note: If a player is deterministic (no randomness) then every game with the same starting state will result in the same outcome. 
Therefore, you will modify the Pente Player API to allow it to start a game from a board state where a couple of pieces have already been placed. 
This will allow your player evaluation system to make a couple of random moves at the beginning of the game and then run a game (using the players you are evaluating) from this starting position.

# Requirements

Your player evaluation system must do the following:

- Use Docker to create at least two containers. 
- One container should run the Pente Player API (using the code that you received). Call this Pente player Alice.
- One container should run code for the player evaluation framework.
- Modify Alice (along with the Pente Player API) to start playing a game with a couple of pieces already on the board.
- Use your player evaluation system to play Alice against herself many times to determine whether Alice does better as X or O.
- Make a minor modification to Alice's gameplay logic to create a new Pente player. Call this new Pente player Baab.
- Use your player evaluation system to play Alice against Baab many times to determine which player is stronger.

# Turning In the Assignment

Your team should submit a link to a repository that contains a compose.yaml file as well as all files necessary to build and run your docker containers.

If there is any other information that I need to make use of your player evaluation framework, please make sure that information is easy to find in your repository.
