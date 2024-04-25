import json
import sys

class GameEngine:
    def __init__(self, map_filename):
        self.load_map(map_filename)
        self.current_room = self.start_room
        self.inventory = []

    def load_map(self, map_filename):
        try:
            with open(map_filename, 'r') as f:
                map_data = json.load(f)
                self.start_room = map_data["start"]
                self.rooms = {room["name"]: room for room in map_data["rooms"]}
        except FileNotFoundError:
            print("Error: Map file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid map file format.")
            sys.exit(1)

    def look(self):
        room = self.rooms[self.current_room]
        print(f"> {room['name']}\n\n{room['desc']}\n")
        self.print_exits(room)
        self.print_items(room)

    def print_exits(self, room):
        print("Exits:", ", ".join(room["exits"].keys()), "\n")

    def print_items(self, room):
        if "items" in room:
            print("Items:", ", ".join(room["items"]), "\n")

    def go(self, direction):
        room = self.rooms[self.current_room]
        exits = room["exits"]
        if direction in exits:
            next_room_name = exits[direction]
            if self.is_door_locked(room, direction):
                print("The door is locked.")
            else:
                self.current_room = next_room_name
                self.look()
        else:
            print("There's no way to go", direction + ".")

    def is_door_locked(self, room, direction):
        next_room_name = room["exits"][direction]
        next_room = self.rooms[next_room_name]
        return next_room.get("locked", False)

    def use(self, item):
        room = self.rooms[self.current_room]
        if item in self.inventory:
            exits = room["exits"]
            for direction, next_room_name in exits.items():
                next_room = self.rooms[next_room_name]
                if next_room.get("locked", False) and next_room.get("key") == item:
                    next_room["locked"] = False
                    print("You used", item, "to unlock the door to the", next_room["name"])
                    return
            print("You can't use", item, "here.")
        else:
            print("You don't have", item, "in your inventory.")

    def get(self, item):
        room = self.rooms[self.current_room]
        if "items" in room and item in room["items"]:
            room["items"].remove(item)
            self.inventory.append(item)
            print("You picked up", item)
        else:
            print("There's no", item, "here.")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            room = self.rooms[self.current_room]
            room["items"].append(item)
            print("You dropped", item)
        else:
            print("You don't have", item, "in your inventory.")

    def show_inventory(self):
        if self.inventory:
            print("Inventory:", ", ".join(self.inventory))
        else:
            print("Your inventory is empty.")

    def help(self):
        print("Available commands:")
        print("  go [direction]")
        print("  look")
        print("  get [item]")
        print("  drop [item]")
        print("  use [item]")
        print("  inventory")
        print("  quit\n")

    def quit(self):
        print("Goodbye!")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    game = GameEngine(sys.argv[1])
    game.look()

    while True:
        command = input("What would you like to do? ").strip().lower()
        if command == "quit":
            game.quit()
        elif command == "look":
            game.look()
        elif command.startswith("go"):
            _, direction = command.split(" ", 1)
            game.go(direction)
        elif command.startswith("get"):
            _, item = command.split(" ", 1)
            game.get(item)
        elif command.startswith("drop"):
            _, item = command.split(" ", 1)
            game.drop(item)
        elif command.startswith("use"):
            _, item = command.split(" ", 1)
            game.use(item)
        elif command.startswith("inventory"):
            game.show_inventory()
        elif command.startswith("help"):
            game.help()