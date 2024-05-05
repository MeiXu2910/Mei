import json
import sys

class Room:
    def __init__(self, name, desc, exits, items=None, locked=False):
        self.name = name
        self.desc = desc
        self.exits = exits
        self.items = items if items else []
        self.locked = locked

    def describe_room(self):
        print(f'> {self.name}\n\n{self.desc}\n')
        if self.items:
            print(f'Items: {", ".join(self.items)}\n')
        print(f'Exits: {" ".join(self.exits.keys())}\n')

class Player:
    def __init__(self):
        self.current_room = None
        self.inventory = []
        self.command_history = []

    def add_to_history(self, command):
        self.command_history.append(command)

    def show_history(self):
        print("Command History:")
        for command in self.command_history:
            print(command)

    def describe_room(self):
        print(f'> {self.current_room.name}\n\n{self.current_room.desc}\n')
        if self.current_room.items:
            print(f'Items: {", ".join(self.current_room.items)}\n')
        print(f'Exits: {" ".join(self.current_room.exits.keys())}\n')

    def lock_room(self, room_name):
        if room_name in self.current_room.exits.values():
            room = [r for r in self.current_room.exits.values() if r.name == room_name][0]
            room.locked = True
            print(f"The {room_name} is now locked.")
        else:
            print(f"There's no exit to {room_name}.")

    def unlock_room(self, room_name):
        if room_name in self.current_room.exits.values():
            room = [r for r in self.current_room.exits.values() if r.name == room_name][0]
            room.locked = False
            print(f"The {room_name} is now unlocked.")
        else:
            print(f"There's no exit to {room_name}.")
        

    def go(self, direction):
        if direction in ["n", "s", "e", "w", "u", "d"]:
            direction = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}[direction]
        
        if direction in self.current_room.exits:
            self.current_room = self.current_room.exits[direction]
            print(f"You go {direction}.\n")
            #print()
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
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} anywhere.")

    def show_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.current_room.items.append(item)
            print(f"You drop the {item}.")
        else:
            print(f"You don't have {item} in your inventory.")

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
        room = Room(room_data["name"], room_data["desc"], room_data["exits"], room_data.get("items", []), room_data.get("locked", False))
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
            player.add_to_history(" ".join(action))
            if verb == "go":
                if len(action) < 2:
                    print("Sorry, you need to 'go' somewhere.")
                    continue
                direction = action[1]
                if direction in player.current_room.exits:
                    next_room = player.current_room.exits[direction]
                    if next_room.locked:
                        print(f"The {next_room.name} is locked. You can't go there.")
                    else:
                        if player.go(direction):
                            player.look()
                else:
                    print(f"There's no way to go {direction}.")
            elif verb == "look":
                player.look()
            elif verb == "get":
                if len(action) < 2:
                    print("Sorry, you need to 'get' something.")
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
                    print("Sorry, you need to 'drop' something.")
                    continue
                item = action[1]
                player.drop(item)
            elif verb == "history":  # 新添加的 history 命令
                player.show_history()
            elif verb == "lock":  # 新添加的 lock 命令
                if len(action) < 2:
                    print("Sorry, you need to specify a room to lock.")
                    continue
                room_name = " ".join(action[1:])
                player.lock_room(room_name)
            elif verb == "unlock":  # 新添加的 unlock 命令
                if len(action) < 2:
                    print("Sorry, you need to specify a room to unlock.")
                    continue
                room_name = " ".join(action[1:])
                player.unlock_room(room_name)
            else:
                print("I don't understand that command.")
        except EOFError:
            print("Use 'quit' to exit.")


if __name__ == "__main__":
    main()