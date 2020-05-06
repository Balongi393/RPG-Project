from Classes.game import Player, colors
from Classes.magic import spell
from Classes.inventory import item
import random

#Creating Black Magic
makichu = spell("Makichu", 25, 600, "black")
durmatsain = spell("Durmat sain", 25, 550, "black")
laviosa = spell("Laviosa", 25, 630, "black")
hagalulu = spell("Hagalulu", 40, 460, "black")
dagardala = spell("Dagardala", 20, 540,"black")

#Creating White Magic
cure1 = spell("Brackium Emendo", 25, 700, "white")
cure2 = spell("Episkey", 40, 2000, "white")

#Create items
potion = item("Potion", "potion", "Heals 50 HP", 200)
highpotion = item("High_Potion", "potion", "Heals 100 HP", 400)
superpotion = item("Super_Potion", "potion", "Heals 500 HP", 1000)
elixer = item("Elixer", "elixerl", "Fully restores HP/MP of one party member", 9999)
highelixer = item("Mega_Elixer", "elixerh", "Fully restores party's HP/MP", 9999)

grenade = item("Grenade", "attack", "Done 500 damage", 500)

player_magic = [makichu, durmatsain, laviosa, hagalulu, dagardala, cure1, cure2]
enemy_magic = [makichu, durmatsain, cure1, cure2]
player_item = [{"item": potion, "quantity": 15},
               {"item": highpotion, "quantity": 5},
               {"item": superpotion, "quantity": 5},
               {"item": elixer, "quantity": 5},
               {"item": highelixer, "quantity": 2},
               {"item": grenade, "quantity": 5}]

#instantiate People
player1 = Player("Pdani Pad  ", 3500, 200, 265, 30, player_magic, player_item)
player2 = Player("Lal Bonga  ", 3890, 200, 355, 30, player_magic, player_item)
player3 = Player("Lal Naara  ", 4100, 200, 400, 30, player_magic, player_item)

enemy1 = Player("Pola Jutt  ", 2000, 175, 200, 225, enemy_magic, [])
enemy2 = Player("Mola Jutt  ", 15000, 175, 600, 225, enemy_magic, [])
enemy3 = Player("Kola Jutt  ", 4000, 175, 300, 225, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(colors.FAIL + colors.BOLD + "AN ENEMY ATTACKS!" + colors.ENDC)

while running:
    print("============================================")
    print("\n\n")
    print(colors.BOLD + "NAME                     HP                                     MP" + colors.ENDC)
    for player in players:
        player.get_status()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_status()

    for player in players:
        player.choose_action()
        choice = input("\tChoose your action : ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_enemy(enemies)
            enemies[enemy].take_damage(dmg)
            print(colors.FAIL + "\n\tYou attacked " + enemies[enemy].name + "for", dmg, "points of damage." + colors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("\tChoose magic : ")) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(colors.FAIL + "\n\tNot Enough MP\n" + colors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(colors.HEADER + "\n\t" + spell.name + " heals for " + str(magic_dmg) + " HP." + colors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_enemy(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(colors.OKBLUE + "\n\t" + spell.name + " done " +  str(magic_dmg), " points of damage to " + enemies[enemy].name  + colors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choise = int(input("\tChoose items : ")) - 1

            if item_choise == -1:
                continue

            item = player.items[item_choise]["item"]
            if player.items[item_choise]["quantity"] == 0:
                print(colors.FAIL + "\n\t" + "None left..." + colors.ENDC)
                print("\n")
                continue

            player.items[item_choise]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print("\t" + colors.OKGREEN + item.name + " heals for " + str(item.prop) + colors.ENDC)

            if item.type == "elixerh":
                    player.hp = player1.maxhp
                    player.mp = player1.maxmp
                    print("\n\t" + colors.OKGREEN + item.name + " Fully restores party's HP/MP "  + colors.ENDC)
            elif item.type == "elixerl":
                if item.name == "Mega_Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player1.maxhp
                    player.mp = player1.maxmp
                    print("\n\t" + colors.OKGREEN + item.name + " Fully restores HP/MP of one party member "  + colors.ENDC)
            if item.type == "attack":
                enemy = player.choose_enemy(enemies)
                enemies[enemy].take_damage(item.prop)
                print("\n\t" + colors.FAIL + item.name + " done " + str(item.prop) + " points of damage to " + enemies[enemy].name +  colors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died")
                    del enemies[enemy]

        # Check If Battle is Over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check If Player won
    if defeated_enemies == 3:
        print("============================================")
        print("\t" + colors.OKGREEN + colors.BOLD + "You Win" + colors.ENDC)
        running = False

    # Check If Enemy Won
    elif defeated_players == 3:
        print("============================================")
        print("\t" + colors.FAIL + colors.BOLD + "Enemy Defeated You" + colors.ENDC)
        running = False
    #Enemy Attacks
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            #Enemy Chose Attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print("\n\t" + enemy.name + "attacks " + players[target].name + " for ", enemy_dmg, "points of damage.")

        elif enemy_choice == 1:
            magic_dmg = enemy.enemy_magic()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(colors.HEADER + "\n\t" + spell.name + " heals " + enemy.name + "for " + str(magic_dmg) + " HP." + colors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(colors.OKBLUE + "\n\t" + enemy.name + "'s " + spell.name + " done " + str(magic_dmg),
                      " points of damage to " + players[target].name + colors.ENDC)
                if players[target].get_hp() == 0:
                    print("\n\t" + players[target].name + " has died")
                    del players[target]
            # print("Enemy chose", spell, "damage", magic_dmg)

    # # Check If Battle is Over
    # defeated_enemies = 0
    # defeated_players = 0
    #
    # for enemy in enemies:
    #     if enemy.get_hp() == 0:
    #         defeated_enemies += 1
    #
    # for player in players:
    #     if player.get_hp() == 0:
    #         defeated_players += 1
    #
    # # Check If Player won
    # if defeated_enemies == 3:
    #     print("============================================")
    #     print("\t" + colors.OKGREEN + colors.BOLD + "You Win" + colors.ENDC)
    #     running = False
    #
    # # Check If Enemy Won
    # elif defeated_players == 3:
    #     print("============================================")
    #     print("\t" + colors.FAIL + colors.BOLD + "Enemy Defeated You" + colors.ENDC)
    #     running = False
    #
    #
    #

