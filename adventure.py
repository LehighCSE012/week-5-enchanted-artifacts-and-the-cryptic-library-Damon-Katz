"""
part 5 now with dicts
"""

import random


def safe_input(prompt, default="skip"):
    """
    gets input and handles errors
    """
    try:
        return input(prompt).strip().lower()
    except OSError:
        return default


def display_player_status(player_stats):
    """
    display stats
    """
    print(
        f"Your current health: {player_stats['health']}, "
        f"Attack: {player_stats['attack']}"
    )


def handle_path_choice(player_stats):
    """
    random path choice
    """
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        new_health = min(player_stats['health'] + 10, 100)
        player_stats.update({'health': new_health})
    else:
        print("You fall into a pit and lose 15 health points.")
        new_health = max(player_stats['health'] - 15, 0)
        player_stats.update({'health': new_health})
        if player_stats['health'] == 0:
            print("You are barely alive!")
    return player_stats


def player_attack(monster_health):
    """
    player attack
    """
    print("You strike the monster for 15 damage!")
    return max(monster_health - 15, 0)


def monster_attack(player_stats):
    """
    monster attack
    """
    if random.random() < 0.5:
        print("The monster lands a critical hit for 20 damage!")
        new_health = max(player_stats['health'] - 20, 0)
        player_stats.update({'health': new_health})
    else:
        print("The monster hits you for 10 damage!")
        new_health = max(player_stats['health'] - 10, 0)
        player_stats.update({'health': new_health})
    return player_stats


def combat_encounter(player_stats, monster_health, has_treasure):
    """
    monster fight
    """
    print("\n--- Combat Encounter ---")
    while player_stats['health'] > 0 and monster_health > 0:
        monster_health = player_attack(monster_health)
        if monster_health == 0:
            print("You defeated the monster!")
            return player_stats, has_treasure
        player_stats = monster_attack(player_stats)
        display_player_status(player_stats)
        if player_stats['health'] == 0:
            print("Game Over!")
            return player_stats, False
    return player_stats, False


def check_for_treasure(has_treasure):
    """
    treasure check
    """
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")


def acquire_item(inventory, item):
    """
    add to invantory
    """
    inventory.append(item)
    print(f"You acquired a {item}!")
    return inventory


def display_inventory(inventory):
    """
    Shows invantory
    """
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for idx, item in enumerate(inventory, start=1):
            print(f"{idx}. {item}")


def discover_artifact(player_stats, artifacts, artifact_name):
    """
    handle artifact, uses get() update()
    """
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(
            f"\nYou discovered the {artifact_name.replace('_', ' ').title()}: "
            f"{artifact['description']}"
        )
        effect = artifact.get("effect") # uses get to avoid key error
        if effect == "increases health":
            new_health = min(player_stats['health'] + artifact['power'], 100)
            player_stats.update({'health': new_health}) # uses update to update health
            print(f"Your health increases by {artifact['power']}!")
        elif effect == "enhances attack":
            new_attack = player_stats['attack'] + artifact['power']
            player_stats.update({'attack': new_attack}) # uses update to update attack
            print(f"Your attack increases by {artifact['power']}!")
        elif effect == "solves puzzles":
            print("Your mind is enlightened by the staff's wisdom!")
        artifacts.pop(artifact_name)
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts


def find_clue(clues, new_clue):
    """
    check if you know this clue
    """
    if new_clue in clues: # uses in to check if clue is in set
        print("You already know this clue.")
    else:
        clues.add(new_clue) # uses add to add clue to set
        print(f"You discovered a new clue: {new_clue}")
    return clues


def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts=None):
    """
    Handle dungeon exploration, now with artifacts!
    """
    if artifacts is None:
        artifacts = {}
    print("\nEntering the dungeon...\n")
    for room in dungeon_rooms:
        if len(room) != 4:
            raise TypeError("Each dungeon room must be a tuple with exactly 4 elements.")
        try:
            room[1] = "modified"
        except TypeError:
            print("Error: Cannot modify room tuple. Tuples are immutable.")

        room_description, item, challenge_type, challenge_outcome = room
        print(f"\nRoom: {room_description}")

        if item is not None:
            print(f"You found a {item} in the room.")
            if item == "treasure":
                inventory.insert(0, item)
                print("You found a treasure and keep it at the top of your inventory!")
            else:
                acquire_item(inventory, item)

        if challenge_type == "puzzle":
            if "staff_of_wisdom" in inventory:
                bypass_choice = safe_input(
                    "Would you like to bypass this puzzle using your wisdom? (yes/no): ",
                    default="no"
                )
                if bypass_choice == "yes":
                    success_message, failure_message, health_change = challenge_outcome
                    bypass_health = abs(health_change)
                    new_health = min(player_stats['health'] + bypass_health, 100)
                    player_stats.update({'health': new_health})
                    print(
                        f"You bypass the puzzle using your wisdom! "
                        f"Your health increases by {bypass_health}."
                    )
                else:
                    puzzle_choice = safe_input(
                        "Do you want to solve or skip the puzzle? ",
                        default="skip"
                    )
                    if puzzle_choice == "solve":
                        success = random.choice([True, False])
                        success_message, failure_message, health_change = challenge_outcome
                        if success:
                            print(success_message)
                            player_stats['health'] += health_change
                        else:
                            print(failure_message)
                            player_stats['health'] += health_change
                    else:
                        print("You chose to skip the puzzle. No changes occur.")
            else:
                puzzle_choice = safe_input(
                    "Do you want to solve or skip the puzzle? ",
                    default="skip"
                )
                if puzzle_choice == "solve":
                    success = random.choice([True, False])
                    success_message, failure_message, health_change = challenge_outcome
                    if success:
                        print(success_message)
                        player_stats['health'] += health_change
                    else:
                        print(failure_message)
                        player_stats['health'] += health_change
                else:
                    print("You chose to skip the puzzle. No changes occur.")
        elif challenge_type == "trap":
            trap_choice = safe_input(
                "Do you want to disarm or bypass the trap? ",
                default="bypass"
            )
            if trap_choice == "disarm":
                success = random.choice([True, False])
                success_message, failure_message, health_change = challenge_outcome
                if success:
                    print(success_message)
                    player_stats['health'] += health_change
                else:
                    print(failure_message)
                    player_stats['health'] += health_change
            else:
                print("You chose to bypass the trap. You proceed with caution.")
        elif challenge_type == "library":
            print("A vast library filled with ancient, cryptic texts.")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            selected_clues = random.sample(possible_clues, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)
            if "staff_of_wisdom" in inventory:
                print("\nYour staff of wisdom reveals the true meaning of these clues!")
                print("You can now bypass a puzzle challenge in one of the other rooms.")
        elif challenge_type == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")

        if player_stats['health'] < 50 and "healing potion" in inventory:
            inventory.remove("healing potion")
            print("Your health is low. You used a healing potion from your inventory!")
            new_health = min(player_stats['health'] + 20, 100)
            player_stats.update({'health': new_health})

        display_inventory(inventory)
        print(f"Current health: {player_stats['health']}")
        print("-" * 40)

    print(f"\nYou exit the dungeon with {player_stats['health']} health.")
    return player_stats, inventory, clues


def main():
    """Main game loop. as provided by the professor"""
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle",
         ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap",
         ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle",
         ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    has_treasure = random.choice([True, False])

    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)

        if random.random() < 0.3:
            # uses keys to get the artifact name, not sure if this counts as it was provided but
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
                display_player_status(player_stats)

        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(
                player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:")
            display_inventory(inventory)
            print("Clues:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues.")


if __name__ == "__main__":
    main()
