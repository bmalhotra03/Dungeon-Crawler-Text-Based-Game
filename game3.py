# Author: Brij Malhotra
# Filename: game3.py
# Version: 1
# Purpose: This simulates the text based adventure that is built around the json description file that is taken as a command line argument

import json
import re
import sys

# Load the dungeon description from a JSON file
def load_dungeon(file_path):
    with open(file_path, 'r') as file:
        dungeon = json.load(file)
    return dungeon

# Remove common stop words from input
def filter_input(player_input):
    stop_words = ['a', 'an', 'the', 'to', 'with', 'on', 'in', 'is']
    words = player_input.lower().split()
    filtered = [word for word in words if word not in stop_words]
    return ' '.join(filtered)

# Process player input
def process_input(player_input, current_room, dungeon):
    player_input = filter_input(player_input)
    # Regular expression to match game commands
    match = re.match(r'^(go|take|open|use|look)(\s+.*)?$', player_input)
    if not match:
        return "Invalid command. Try again."

    verb, args = match.groups()
    args = args.strip() if args else ''
    
    # Based on given command, appropriate function will be used
    if verb == 'go':
        return func_go(args, current_room, dungeon)
    elif verb == 'take':
        return func_take(args, current_room)
    elif verb == 'open':
        return func_open(args, current_room)
    elif verb == 'use':
        return func_use(args, current_room)
    elif verb == 'look':
        return func_look(args, current_room, dungeon)
    else:
        return "Unknown command."

# Handle the GO command
def func_go(direction, current_room, dungeon):
    direction = direction.upper()
    if direction in dungeon[current_room]:
        new_room = dungeon[current_room][direction.lower()]
        if new_room:
            return new_room, f"You move {direction} to the {new_room}."
        else:
            return current_room, "You can't go that way."
    else:
        return current_room, "Invalid direction."

# Handle the TAKE command
def func_take(obj, current_room):
    for item in dungeon[current_room]['objects']:
        if item['objID'] == obj:
            if 'TAKE' in item['interactions']:
                return current_room, f"You take the {obj}."
            else:
                return current_room, "You can't take this object."
    return current_room, "There is no such object here."

# Handle the OPEN command
def func_open(obj, current_room):
    for item in dungeon[current_room]['objects']:
        if item['objID'] == obj:
            if 'OPEN' in item['interactions']:
                return current_room, f"You open the {obj}."
            else:
                return current_room, "You can't open this object."
    return current_room, "There is no such object here."

# Handle the USE command
def func_use(args, current_room):
    objects = args.split()
    if len(objects) == 1:
        obj = objects[0]
        for item in dungeon[current_room]['objects']:
            if item['objID'] == obj:
                if 'USE' in item['interactions']:
                    return current_room, f"You use the {obj}."
                else:
                    return current_room, "You can't use this object."
        return current_room, "There is no such object here."
    elif len(objects) == 2:
        obj1, obj2 = objects
        for item in dungeon[current_room]['objects']:
            if item['objID'] == obj1 and 'USE' in item['interactions']:
                return current_room, f"You use the {obj1} on the {obj2}."
        return current_room, "Nothing happens."
    else:
        return current_room, "Invalid use command."

# Handle the LOOK command
def func_look(args, current_room, dungeon):
    if not args:
        return current_room, dungeon[current_room]['description']
    for item in dungeon[current_room]['objects']:
        if item['objID'] == args:
            return current_room, item['description']
    if args.upper() in ['NORTH', 'SOUTH', 'EAST', 'WEST']:
        direction = args.upper()
        if direction.lower() in dungeon[current_room] and dungeon[current_room][direction.lower()]:
            return current_room, f"You see {dungeon[current_room][direction.lower()]} to the {direction}."
        else:
            return current_room, "Nothing in that direction."
    return current_room, "You don't see anything special."

# Main game loop
def main(dungeon_file):
    
    global dungeon
    dungeon = load_dungeon(dungeon_file)
    current_room = list(dungeon.keys())[0]

    print("Welcome to the Star Wars text adventure!")
    print("You are a youngling aspiring to become a Jedi, now is the time to embark on your journey. Explore the rooms and interact with objects young Padawan.")
    print("Bring balance to the force.")
    print("Available commands: GO <direction>, TAKE <object>, OPEN <object>, USE <object> (<object>), LOOK <direction|object|nothing>")
    print(dungeon[current_room]['description'])

    while True:
        player_input = input("> ")
        if player_input.lower() in ['quit', 'exit']:
            print("Thank you for playing! May the Force be with you.")
            break
        current_room, response = process_input(player_input, current_room, dungeon)
        print(response)
        print(dungeon[current_room]['description'])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python game3.py <dungeon.json>")
    else:
        main(sys.argv[1])