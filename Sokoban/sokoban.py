#!/usr/bin/env python3

import argparse
import sys
import os

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("-i", help="Path to the file with the Sokoban instance.")
    return parser.parse_args(argv)


class SokobanGame(object):
    """ A Sokoban Game. """
    def __init__(self, string):
        """ Create a Sokoban game object from a string representation such as the one defined in
            http://sokobano.de/wiki/index.php?title=Level_format
        """
        lines = string.split('\n')
        self.h, self.w = len(lines), max(len(x) for x in lines)
        self.player = None
        self.walls = set()
        self.boxes = set()
        self.goals = set()
        for i, line in enumerate(lines, 0):
            for j, char in enumerate(line, 0):
                if char == '#':  # Wall
                    self.walls.add((i, j))
                elif char == '@':  # Player
                    assert self.player is None
                    self.player = (i, j)
                elif char == '+':  # Player on goal square
                    assert self.player is None
                    self.player = (i, j)
                    self.goals.add((i, j))
                elif char == '$':  # Box
                    self.boxes.add((i, j))
                elif char == '*':  # Box on goal square
                    self.boxes.add((i, j))
                    self.goals.add((i, j))
                elif char == '.':  # Goal square
                    self.goals.add((i, j))
                elif char == ' ':  # Space
                    pass  # No need to do anything
                else:
                    raise ValueError(f'Unknown character "{char}"')
    
    def is_wall(self, x, y):
        """ Whether the given coordinate is a wall. """
        return (x, y) in self.walls

    def is_box(self, x, y):
        """ Whether the given coordinate has a box. """
        return (x, y) in self.boxes

    def is_goal(self, x, y):
        """ Whether the given coordinate is a goal location. """
        return (x, y) in self.goals

def calculation(board,count,isAll):
    file = open("Instances/Problem"+str(count),"w")
    file.write("(define (problem simple)\n"
  "(:domain sokoban-domain)\n"
  "(:objects ")
    h=board.h
    w=board.w
    
    file = open("Instances/Problem"+str(count),"a")
    for i in range(1,h+1):
        for j in range(1,w+1):
            file.write("p"+(str(i)+"-"+str(j)+" "))
        file.write("\n")
    file.write("teleport1 teleport2)\n\n(:init\n")
    
    for i in range(1,h+1):
        for j in range(1,w):
            file.write("(neighbor p"+str(i)+"-"+str(j)+" p"+str(i)+"-"+str(j+1)+") ")
            file.write("(neighbor p"+str(i)+"-"+str(j+1)+" p"+str(i)+"-"+str(j)+") ")
        file.write("\n")
    file.write("\n\n")
    
    for i in range(1,h):
        for j in range(1,w+1):
            file.write("(neighbor p"+str(i)+"-"+str(j)+" p"+str(i+1)+"-"+str(j)+") ")
            file.write("(neighbor p"+str(i+1)+"-"+str(j)+" p"+str(i)+"-"+str(j)+") ")
        file.write("\n")
    file.write("\n\n")
    
    for i in range(1,h+1):
        for j in range(1,w-1):
            file.write("(neighbor_space p"+str(i)+"-"+str(j)+" p"+str(i)+"-"+str(j+2)+") ")
            file.write("(neighbor_space p"+str(i)+"-"+str(j+2)+" p"+str(i)+"-"+str(j)+") ")
        file.write("\n")
    file.write("\n\n")
    
    for i in range(1,h-1):
        for j in range(1,w+1):
            file.write("(neighbor_space p"+str(i)+"-"+str(j)+" p"+str(i+2)+"-"+str(j)+") ")
            file.write("(neighbor_space p"+str(i+2)+"-"+str(j)+" p"+str(i)+"-"+str(j)+") ")
        file.write("\n")
    file.write("\n\n")
    
    file.write("(has_player p"+str(board.player[0]+1)+"-"+str(board.player[1]+1)+")\n")
    
    for i in range(1,w+1):
        for j in range(1,h+1):
            if board.is_wall(i-1,j-1):
                file.write("(has_wall p"+str(i)+"-"+str(j)+")\n")
            if board.is_box(i-1,j-1):
                file.write("(has_box p"+str(i)+"-"+str(j)+")")
            
    file.write("(teleport teleport1) (teleport teleport2)) \n")
    
    file.write("(:goal (and ")
    for i in range(1,h+1):
        for j in range(1,w+1):
            if board.is_goal(i-1,j-1):
                file.write("(has_box p"+str(i)+"-"+str(j)+")")
    file.write("))\n)") 
    file.close()
    if(isAll):  
        # Greedy BFS for all files
        os.system("python fast-downward.py --overall-time-limit 60 --alias lama-first --plan-file Greedy_BFS_Plans/myplan"+str(count)+".txt Domain Instances/Problem"+str(count))
        # A* search for all files
        #os.system("python fast-downward.py --overall-time-limit 60 --alias seq-opt-bjolp --plan-file A_STAR_Plans/myplan"+str(count)+".txt Domain Instances/Problem"+str(count))
        
    else:
        # Greedy BFS
        os.system("python fast-downward.py --alias lama-first --plan-file Greedy_BFS_Plans/myplan.txt Domain Instances/Problem") 
        # A* search
        #os.system("python fast-downward.py --overall-time-limit 60 --alias seq-opt-bjolp --plan-file A_STAR_Plans/myplan.txt Domain Instances/Problem") 
        

    print('Solution: \n============\n')
    with open('myplan.txt', 'r') as file:
        lines=file.readlines()
        for line in lines:
            print(line)    
    # TODO - Some of the things that you need to do:
    #  1. (Previously) Have a domain.pddl file somewhere in disk that represents the Sokoban actions and predicates.
    #  2. Generate an instance.pddl file from the given board, and save it to disk.
    #  3. Invoke some classical planner to solve the generated instance.
    #  3. Check the output and print the plan into the screen in some readable form.

def main(argv):
    args = parse_arguments(argv)
    
    if(args.i=='benchmarks'):
        for count in range(1,51):
            path = 'benchmarks/sasquatch/level'+str(count)+'.sok'
            with open(path, 'r') as file:
                board = SokobanGame(file.read().rstrip('\n'))
            calculation(board,count,True)
    else:
        with open(args.i, 'r') as file:
            board = SokobanGame(file.read().rstrip('\n'))
        calculation(board,'',False)
    


if __name__ == "__main__":
    main(sys.argv[1:])
