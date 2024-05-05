1，Name: Mei Xu

2，Stevens: mxu25@stevens.edu

3，The URL of your public GitHub repo:https://github.com/MeiXu2910/Mei.git

4，An estimate of how many hours you spent on the project：About 60 hours.

5，A description of how you tested your code：Run step by step on the terminal according to the steps of each method, and solve the problem immediately.

6，Any bugs or issues you could not resolve: No,problems solved.

7，An example of a difficult issue or bug and how you resolved:In the go() method, the conditional statement “if direction in self.current_room.exits:” is repeated twice. After the first check, there is no second check to see if it is in the else clause. This results in "You go west "being printed even though the direction is not present in the exit of the room. I replaced the second if statement with an else clause to ensure that "There's no way to go {direction}." is printed only if the direction does not exist at the exit of the room.

8，
New Feature 1: Locking and Unlocking Rooms
Description: Added functionality to lock and unlock rooms in the game. Players can use new verbs lock and unlock to lock and unlock specific rooms. Locked rooms cannot be traversed in the specified direction until they are unlocked.
Usage Example: Players can input lock north to lock the room to the north and input unlock east to unlock the room to the east.
Application Location: Locked and unlocked rooms are distributed throughout the map, and players can find and interact with them by exploring the map.

New Feature 2: Command History
Description: The game now records the player's command history, allowing players to view previously entered commands. Using the new verb history, players can see the commands they have executed recently.
Usage Example: Players can input history to view the list of previously entered commands.
Application Location: This feature can be used at any time during the game, allowing players to review their command history as needed.

New Feature 3: Room Status Display
Description: The game now displays the status of rooms, such as whether they are locked or unlocked, in the room description. This allows players to intuitively understand the state of the room while viewing its description.
Usage Example: When a player enters a locked room, the game will display This room is locked. in the room description to indicate the room's status.
Application Location: Room status display appears when players enter rooms, providing immediate feedback to help players understand the room's situation better.