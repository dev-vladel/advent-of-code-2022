# --- Day 5: Supply Stacks ---
# The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, 
# but because the needed supplies are buried under many other crates, the crates need to be rearranged.

# The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator
# will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

# The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and 
# they want to be ready to unload them as soon as possible so they can embark.

# They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

#     [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 

# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2
# In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains 
# three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

# Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. 
# In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

# [D]        
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 
# In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

#         [Z]
#         [N]
#     [C] [D]
#     [M] [P]
#  1   2   3
# Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

#         [Z]
#         [N]
# [M]     [D]
# [C]     [P]
#  1   2   3
# Finally, one crate is moved from stack 1 to stack 2:

#         [Z]
#         [N]
#         [D]
# [C] [M] [P]
#  1   2   3
# The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, 
# and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

# After the rearrangement procedure completes, what crate ends up on top of each stack?

import re
from copy import deepcopy
from typing import List, NamedTuple, Tuple

CRATES_REGEX = re.compile(r"(\d+)(?=\D*$)")
MOVES_REGEX = re.compile(r".*?(\d+).*?(\d+).*?(\d+)")

Stack = List[str]
Move = NamedTuple("Move", count = int, source = int, destination = int)

file = open('day5-input.txt', 'r')
contents = file.read()

def process_crates_and_moves(contents: str) -> Tuple[List[Stack], List[Move]]:
    stacks_pre, moves_pre = contents.split('\n\n')
    stacks_splits = stacks_pre.splitlines()
    
    stacks_regex_result = CRATES_REGEX.search(stacks_splits[-1])
    number_of_stacks = int(stacks_regex_result.group(1))

    stacks: List[Stack] = [[] for _ in range(number_of_stacks)]

    for stack in stacks_splits[-2::-1]:
        for i in range(number_of_stacks):
            character = stack[4 * i + 1]
            if character != ' ':
                stacks[i].append(character)

    moves: List[Move] = []
    for move in moves_pre.splitlines():
        moves_regex_result = MOVES_REGEX.search(move)

        count, source, destination = map(int, moves_regex_result.groups())
        moves.append(Move(count = count, source = source, destination = destination))

    return stacks, moves

def apply_moves_part_one(stacks: List[Stack], move: Move):
    count, source, destination = move
    for step in range(count):
        stacks[destination - 1].append(stacks[source - 1].pop())

def apply_moves_part_two(stacks: List[Stack], move: Move):
    count, source, destination = move
    stacks[destination - 1].extend(stacks[source - 1][-count:])
    del stacks[source - 1][-count:]

stacks_part_one, moves = process_crates_and_moves(contents)
stacks_part_two = deepcopy(stacks_part_one)

for move in moves:
    apply_moves_part_one(stacks_part_one, move)
    apply_moves_part_two(stacks_part_two, move)

print('The answer for 1st part is:', ''.join(map(lambda x: x[-1], stacks_part_one)))

print('The answer for 2nd part is:', ''.join(map(lambda x: x[-1], stacks_part_two)))
