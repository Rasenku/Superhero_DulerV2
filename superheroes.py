import random
import os

class Ability:
    def __init__(self, name, max_damage):
        '''
       Initialize the values passed into this
       method as instance variables.
        '''

        # Assign the "name" and "max_damage"
        # for a specific instance of the Ability class
        self.name = name
        self.max_damage = max_damage


    def attack(self):
      ''' Return a value between 0 and the value set by self.max_damage.'''

      random_value = random.randint(0,self.max_damage)
      return random_value


class Armor:
    def __init__(self, name, max_block):
        '''Instantiate instance properties.
            name: String
            max_block: Integer
        '''

        self.name = name
        self.max_block = max_block

    def block(self):
        '''
        Return a random value between 0 and the
        initialized max_block strength.
        '''
        random_value = random.randint(0, self.max_block)
        return random_value

class Hero:
    # We want our hero to have a default "starting_health",
    # so we can set that in the function header.
    def __init__(self, name, starting_health=100):
        '''Instance properties:
          abilities: List
          armors: List
          name: String
          starting_health: Integer
          current_health: Integer
        '''

        self.abilities = list()
        self.armors = list()
        self.name = name
        self.starting_health = starting_health
        self.current_health = starting_health
        self.deaths = 0
        self.kills = 0

    def add_ability(self, ability):
        ''' Add ability to abilities list '''
        self.abilities.append(ability)

    def add_armor(self, armor):
        '''Add armor to self.armors
            Armor: Armor Object
        '''
        self.armors.append(armor)

    def add_weapon(self, weapon):
        '''Add weapon to self.abilities'''
        self.abilities.append(weapon)

    def attack(self):
        '''Calculate the total damage from all ability attacks.
          return: total_damage:Int
        '''
        total_damage = 0
        for ability in self.abilities:
            total_damage += ability.attack()
        return total_damage

    def defend(self):  #, damage_amt
        '''Calculate the total block amount from all armor blocks.
            return: total_block:Int
        '''
        total_block = 0
        for armor in self.armors:
            total_block += armor.block()
        return total_block

    def take_damage(self, damage):
        '''Updates self.current_health to reflect the damage minus the defense.
        '''
        defense = self.defend()
        self.current_health -= damage - defense

    def is_alive(self):
        '''Return True or False depending on whether the hero is alive or not.
        '''
        if self.current_health <= 0:
            return False
        return True

    def fight(self, opponent):
        if self.abilities == [] and opponent.abilities == []:
            print("Draw")
        else:
            while self.is_alive() and opponent.is_alive():
                my_dmg = self.attack()
                opponent.take_damage(my_dmg)

                if opponent.is_alive():
                    opponent_dmg = opponent.attack()
                    self.take_damage(opponent_dmg)

                    if self.is_alive():
                        continue
                    else:
                        opponent.kills += 1
                        self.deaths += 1
                        print(f"{opponent.name} wins!")
                else:
                    self.kills += 1
                    opponent.deaths += 1
                    print(f"{self.name} wins!")

    def add_kill(self, num_kills):
        ''' Update self.kills by num_kills amount'''
        self.kills += num_kills

    def add_death(self, num_deaths):
        ''' Update deaths with num_deaths'''
        self.kills += num_deaths



class Weapon(Ability):
    def attack(self):
        """  This method returns a random value
        between one half to the full attack power of the weapon.
        """
        random_value = random.randint(self.max_damage//2, self.max_damage)
        return random_value



class Team:
    def __init__(self, name):
        ''' Initialize your team with its team name and an empty list of heroes
        '''
        self.name = name
        self.heroes = list()

    def remove_hero(self, name):
        '''Remove hero from heroes list.
        If Hero isn't found return 0.
        '''
        foundHero = False
        for hero in self.heroes:
            if hero.name == name:
                self.heroes.remove(hero)
                foundHero = True
        if not foundHero:
            return 0

    def view_all_heroes(self):
            '''Prints out all heroes to the console.'''
            for hero in self.heroes:
                print(hero.name)

    def add_hero(self, hero):
        '''Add Hero object to self.heroes.'''
        self.heroes.append(hero)

    def stats(self):
        '''Print team statistics'''
        for hero in self.heroes:
            kd = hero.kills / hero.deaths
            print("{} Kill/Deaths:{}".format(hero.name,kd))

    def revive_heroes(self):
        ''' Reset all heroes health to starting_health'''
        for hero in self.heroes:
            hero.current_health = hero.starting_health

    def attack(self, other_team):
        ''' Battle each team against each other.'''

        living_heroes = list()
        living_opponents = list()

        for hero in self.heroes:
            living_heroes.append(hero)

        for hero in other_team.heroes:
            living_opponents.append(hero)

        while len(living_heroes) > 0 and len(living_opponents) > 0:
            my_hero = random.choice(living_heroes)
            opponent = random.choice(living_opponents)

            my_hero.fight(opponent)

            if my_hero.is_alive():
                living_opponents.remove(opponent)
            else:
                living_heroes.remove(my_hero)




class Arena:
    def __init__(self):
        self.team_one = None
        self.team_two = None

    def create_ability(self):
        ability_name = input("Ability Name:")
        ability_damage = int(input("Ability Damage:"))
        return Ability (ability_name, ability_damage)

    def create_weapon(self):
        weapon_name = input("Weapon Name:")
        weapon_damage = int(input("Weapon Damage:"))
        return Weapon(weapon_name, weapon_damage)

    def create_armor(self):
        armor_name = input("Armor name:")
        armor_amount = int(input("Armor block amount:"))
        return Armor(armor_name, armor_amount)

    def create_hero(self):
        name = input("Enter a Hero name: ")
        new_Hero = Hero(name, starting_health = 100)
        equip_ability = input("Do you want a random ability? y or no: ")
        equip_weapon = input("Do you want a random weapon? y or no: ")
        equip_armor = input("Do you want random armor? y or no: ")
        if equip_ability == "y":
            new_Hero.add_ability(self.create_ability())
        if equip_weapon == "y":
            new_Hero.add_weapon(self.create_weapon())
        if equip_armor == "y":
            new_Hero.add_armor(self.create_armor())
        return new_Hero

    def build_team_one(self):
        team_name = input("Enter a Team 1 name:")
        team_one = Team(team_name)
        num_of_heroes = int(input("Enter a number of heroes:"))
        for i in range(num_of_heroes):
             hero = self.create_hero()
             team_one.add_hero(hero)
        self.team_one = team_one
    def build_team_two(self):
        team_name = input("Enter a Team 2 name:")
        team_two = Team(team_name)
        num_of_heroes = int(input("Enter a number of heroes:"))
        for i in range(num_of_heroes):
             hero = self.create_hero()
             team_two.add_hero(hero)
        self.team_two = team_two

    def team_battle(self):
            self.team_one.attack(self.team_two)


    def if_team_dead(self, TeamAlive):
        TeamDeaths = 0
        for hero in TeamAlive:
            if hero.current_health == 0:
                TeamDeaths += 1
        if TeamDeaths == len(TeamAlive):
            return True
        else:
            return False

    def show_stats(self):
        teamA = self.if_team_dead(self.team_one.heroes)
        teamB = self.if_team_dead(self.team_two.heroes)

        if teamA == False:
            print(f"Victor is Team {self.team_two.name}")
            print("The Survivors are: ")
            for hero in self.team_one.heroes:
                if hero.is_alive():
                    print(hero.name)
        elif teamB == False:
            print(f"Victor is Team {self.team_one.name}")
            print("The Survivors are: ")
            for hero in self.team_two.heroes:
                if hero.is_alive():
                    print({hero.name})
                else:
                    print("None bro, all my friends are dead")
        elif teamA == False and teamB == False:
            print("DRAW!")

        print(f'Team One KDR: {self.team_one.stats()}')
        print(f'Team Two KDR: {self.team_two.stats()}')



if __name__ == "__main__":
    game_is_running = True

    arena = Arena()

    arena.build_team_one()
    arena.build_team_two()

    while game_is_running:

        arena.team_battle()
        arena.show_stats()
        play_again = input("Do you want to play again? Y or N: ")

        if play_again.lower() == "n":
            game_is_running = False
        else:
            arena.team_one.revive_heroes()
            arena.team_two.revive_heroes()
