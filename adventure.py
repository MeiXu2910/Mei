import json
import sys

class Room:
    def __init__(self, name, desc, exits, items=None):
        self.name = name
        self.desc = desc
        self.exits = exits
        self.items = items if items else []

class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []

    def describe_room(self):
        print(f'> {self.current_room.name}\n\n{self.current_room.desc}\n')
        print(f'Exits: {" ".join(self.current_room.exits.keys())}\n')
        if self.current_room.items:
            print(f'Items: {", ".join(self.current_room.items)}\n')

    def go(self, direction):
        if direction in ["n", "s", "e", "w", "u", "d"]:
            direction = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}[direction]
        
        if direction in self.current_room.exits:
            if direction in self.current_room.locked_exits:
                required_item = self.current_room.locked_exits[direction]
                if required_item in self.inventory:
                    print(f"You unlock the {direction} exit with {required_item}.")
                    self.current_room.unlock_exit(direction, required_item)
                else:
                    print(f"The {direction} exit is locked. You need {required_item} to unlock it.")
                    return False
            self.current_room = self.current_room.exits[direction]
            print(f"You go {direction}.")
            print()
            return True
        else:
            print(f"There's no way to go {direction}.")
            return False

    def look(self):
        self.describe_room()

    def get(self, item):
        if item in self.current_room.items:
            self.current_room.items.remove(item)
            self.inventory.append(item)
            print(f"You pick up the {item}.\n")
        else:
            print(f"There's no {item} here.\n")

def show_inventory(self):
    if not self.inventory:
        print("You're not carrying anything.")
    else:
        print("Inventory:")
        for item in self.inventory:
            print(f" {item}")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.current_room.items.append(item)
            print(f"You drop the {item}.\n")
        else:
            print(f"You don't have {item} in your inventory.\n")

    def help(self):
        print("Commands: go, look, get, inventory, drop, quit, help")

def load_map(map_file):
    with open(map_file, 'r') as f:
        map_data = json.load(f)
    return map_data

def main():
    map_data = load_map(sys.argv[1])
    rooms = {}
    for room_data in map_data["rooms"]:
        room = Room(room_data["name"], room_data["desc"], room_data["exits"], room_data.get("items", []))
        rooms[room_data["name"]] = room

    for room_data in map_data["rooms"]:
        current_room = rooms[room_data["name"]]
        for direction, room_name in room_data["exits"].items():
            current_room.exits[direction] = rooms[room_name]

    player = Player()
    player.current_room = rooms[map_data["start"]]
    player.describe_room()

    while True:
        try:
            action = input("What would you like to do? ").strip().lower().split()
            if not action:
                continue
            verb = action[0]
            if verb == "go":
                if len(action) < 2:
                    print("Specify a direction to go.")
                    continue
                direction = action[1]
                if player.go(direction):
                    player.look()
            elif verb == "look":
                player.look()
            elif verb == "get":
                if len(action) < 2:
                    print("Specify an item to get.")
                    continue
                item = action[1]
                player.get(item)
            elif verb == "inventory":
                player.show_inventory()
            elif verb == "quit":
                print("Goodbye!")
                break
            elif verb == "help":
                player.help()
            elif verb == "drop":
                if len(action) < 2:
                    print("Specify an item to drop.")
                    continue
                item = action[1]
                player.drop(item)
            else:
                print("Unknown command. Type 'help' for instructions.")
        except EOFError:
            print("Type 'quit' to exit.")

if __name__ == "__main__":
    main()