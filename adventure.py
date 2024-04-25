import json
import sys

class TextAdventure:
    def __init__(self, map_filename):
        self.map_filename = map_filename
        self.load_map()

    def load_map(self):
        try:
            with open(self.map_filename, 'r') as file:
                self.map_data = json.load(file)
                self.validate_map()
                self.current_room = self.map_data["start"]
                self.inventory = []
                print("> " + self.get_room_description())
        except FileNotFoundError:
            print("Error: Map file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")
            sys.exit(1)

    def validate_map(self):
        # Check if map contains 'start' and 'rooms' keys
        if "start" not in self.map_data or "rooms" not in self.map_data:
            print("Error: Map file must contain 'start' and 'rooms' keys.")
            sys.exit(1)

        # Validate each room
        room_names = set()
        for room in self.map_data["rooms"]:
            if "name" not in room or "desc" not in room or "exits" not in room:
                print("Error: Each room must have 'name', 'desc', and 'exits' keys.")
                sys.exit(1)
            if room["name"] in room_names:
                print("Error: Room names must be unique.")
                sys.exit(1)
            room_names.add(room["name"])
            for direction, exit_room in room["exits"].items():
                if exit_room not in room_names:
                    print(f"Error: Exit '{exit_room}' from room '{room['name']}' leads to non-existing room.")
                    sys.exit(1)

    def get_room_description(self):
        room = self.get_current_room_data()
        description = room["desc"]
        exits = ", ".join(room["exits"].keys())
        items = ", ".join(room.get("items", []))
        return f"{description}\n\nExits: {exits}\nItems: {items}"

    def get_current_room_data(self):
        for room in self.map_data["rooms"]:
            if room["name"] == self.current_room:
                return room

    def process_command(self, command):
        # Split command into verb and target
        command_parts = command.lower().split(maxsplit=1)
        verb = command_parts[0]
        target = command_parts[1] if len(command_parts) > 1 else None

        # Execute verb
        if verb == "go":
            self.go(target)
        elif verb == "look":
            print("> " + self.get_room_description())
        elif verb == "get":
            self.get_item(target)
        elif verb == "inventory":
            self.show_inventory()
        elif verb == "quit":
            self.quit_game()
        else:
            print("Error: Invalid command.")

    def go(self, direction):
        room = self.get_current_room_data()
        exits = room["exits"]
        if direction in exits:
            next_room = exits[direction]
            # 检查下一个房间是否存在
            if next_room in self.get_room_names():
                self.current_room = next_room
                print("> " + self.get_room_description())
            else:
                print(f"Error: Exit '{direction}' from room '{room['name']}' leads to non-existing room '{next_room}'.")
        else:
            print(f"Error: There's no way to go '{direction}'.")

    def get_item(self, item):
        room = self.get_current_room_data()
        if "items" in room and item in room["items"]:
            self.inventory.append(item)
            room["items"].remove(item)
            print("You pick up the {}.".format(item))
        else:
            print(f"Error: There's no '{item}' in this room.")
                

    def show_inventory(self):
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print("  " + item)
        else:
            print("You're not carrying anything.")

    def quit_game(self):
        print("Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    game = TextAdventure(sys.argv[1])

    # Game loop
    while True:
        command = input("What would you like to do? ").strip()
        game.process_command(command)