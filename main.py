# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from asteroidfield import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from starfield import Starfield
from score import Score
from game import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()