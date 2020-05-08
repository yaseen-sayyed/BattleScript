import random

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create black magic
fire = Spell("Fire", 20, 320, "black")
thunder = Spell("Thunder", 30, 600, "black")
blizzard = Spell("Blizzard", 50, 800, "black")
meteor = Spell("Meteor", 25, 400, "black")
quake = Spell("Quake", 14, 110, "black")

# Create white magic
cure = Spell("Cure", 25, 560, "white")
cura = Spell("Cura", 38, 1200, "white")

# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 250)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 800)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 99999)
hielixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 99999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 800)


player_spells = [fire, thunder, meteor, blizzard, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 3},
                {"item": elixir, "quantity": 4},
                {"item": hielixir, "quantity": 2},
                {"item": grenade, "quantity": 5}]

enemy_spells = [fire, thunder, meteor]

# Instantiate player and enemy
player2 = Person("Lancelot:", 3460, 170, 360, 34, player_spells, player_items)
player1 = Person("Arthur  :", 2860, 195, 320, 34, player_spells, player_items)
player3 = Person("Merlin  :", 3060, 185, 288, 34, player_spells, player_items)

enemy1 = Person("Imp    ", 2500, 45, 560, 325, enemy_spells, [])
enemy2 = Person("Morgana", 18200, 90, 450, 25, enemy_spells, [])
enemy3 = Person("Imp    ", 2500, 45, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True

print(bcolors.FAIL + bcolors.B0LD + "\nAN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=====================================================================")

    print("\n")
    print("                       HP                                                     MP")

    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    print("\n")

    for player in players:
        player.choose_action()
        choice = int(input("Choose Action:"))
        index = choice - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("\n" + bcolors.B0LD + player.name[:-1] + bcolors.ENDC + " attacked " + bcolors.FAIL +
                  enemies[enemy].name.replace(" ", "") + bcolors.ENDC + " for", bcolors.OKGREEN + str(dmg) + bcolors.ENDC, "points.")

            if enemies[enemy].get_hp() == 0:
                print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + bcolors.ENDC + " has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP" + bcolors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "damage " + bcolors.ENDC,
                      "to " + bcolors.FAIL + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + bcolors.ENDC + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose Item:")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "SORRY! You've run out of", item + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + bcolors.B0LD + "\n" + str(item.prop) + "HP healed with", item.name + bcolors.ENDC)

            elif item.type == "elixir":

                if item.name == "MegaElixir":
                    print(bcolors.OKGREEN + bcolors.B0LD + "HP/MP fully restored for all party members" + bcolors.ENDC)
                    for p in players:
                        p.hp = p.maxhp
                        p.mp = p.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + bcolors.B0LD + "HP/MP fully restored" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + item.name, "deals", item.prop, "damage" + bcolors.ENDC, "to" + bcolors.FAIL +
                      enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + bcolors.ENDC + " has died.")
                    del enemies[enemy]

    defeated_enemies = 0
    dead_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    if defeated_enemies == 3:
        print(bcolors.OKGREEN + "YOU W0N !!!" + bcolors.ENDC)
        running = False

    for player in players:
        if player.get_hp() == 0:
            dead_players += 1
    if dead_players == 3:
        print(bcolors.FAIL + "YOU LOST!!!" + bcolors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + bcolors.B0LD + enemies[0].name.replace(" ", "") + bcolors.ENDC + " attacked",
                  players[target].name[:-1].replace(" ", ""), "for",
                  bcolors.FAIL + str(enemy_dmg) + bcolors.ENDC, "points.")

        elif enemy_choice == 1:
            # Chose magic
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals " + enemy.name + " for", str(magic_dmg), "HP" + bcolors.ENDC)

            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + " deals", str(magic_dmg), "damage with "
                      + spell.name + bcolors.ENDC,
                      "to " + bcolors.FAIL + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + players[target].name.replace(" ", "") + bcolors.ENDC + " has died.")
                    del players[target]
            print("Enemy chose:", spell)


