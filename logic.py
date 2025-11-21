from random import randint, random
import requests

def get_pokemon(user_id):
    return Pokemon.pokemons.get(user_id)

class Pokemon:
    pokemons = {}

    def __init__(self, trainer_id):
        self.trainer_id = trainer_id

        self.pokemon_number = randint(1, 1000) #Больше 1300

        self.data = self.load_pokemon()

        # Характеристики
        self.level = 1
        self.xp = 0
        self.xp_to_next = 50
        self.hp = randint(100, 150)
        self.power = randint(25, 40)

        self.rarity_name = self.rarity_roll()
        self.bonus_factor = self.rarity_value(self.rarity_name)

        Pokemon.pokemons[trainer_id] = self

    # Загрузка данных
    def load_pokemon(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        r = requests.get(url)

        if r.status_code == 200:
            j = r.json()
            return {
                "name": j['forms'][0]['name'],
                "img": j['sprites']['front_default'],
                "type": j['types'][0]['type']['name']
            }

        return {"name": "Pikachu",
                "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                "type": "electric"}
    @staticmethod
    def rarity_roll():
        roll = random()
        if roll < 0.0005:
            return "mythical"
        elif roll < 0.01:
            return "ultra"
        elif roll < 0.10:
            return "rare"
        return "common"

    @staticmethod
    def rarity_value(rarity):
        values = {
            "common": 1.0,
            "rare": 1.2,
            "ultra": 1.5,
            "mythical": 2.0
        }
        return values[rarity]

    # Система опыта
    def add_xp(self, amount):
        self.xp += amount
        leveled = False

        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = 50 * (self.level ** 2)
            leveled = True

        return leveled

    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.trainer_id} с @{enemy.trainer_id}"
        else:
            enemy.hp = 0
            return f"Победа @{self.trainer_id} над @{enemy.trainer_id}! "

    # Информация
    def info(self):
        return (f"__Имя: {self.data['name']}\n__"
                f"__Тип: {self.data['type']}\n__"
                f"__Хп:{self.hp}\n__"
                f"__Сила:{self.power}\n__"
                f"__Редкость: {self.rarity_name}\n__"
                f"__Множитель бонусов: x{self.bonus_factor}\n__"
                f"__Уровень: {self.level}\n__"
                f"__Опыт: {round(self.xp, 1)}/{self.xp_to_next}__"
                )

    def show_img(self):
        return self.data['img']


class Wizard(Pokemon):
    def __init__(self, trainer_id):
        super().__init__(trainer_id)

        self.hp -= randint(10, 20)
        self.power += randint(5, 10)

    def info(self):
        print(super().info() + f"Волшебник")

    def attack(self, enemy):
        print(super().attack(enemy))

class Fighter(Pokemon):
    def __init__(self, trainer_id):
        super().__init__(trainer_id)

        self.hp += randint(15, 25)
        self.power -= randint(5, 15)

    def info(self):
        print(super().info() + f"Боец")

    def attack(self, enemy):
        print(super().attack(enemy))

if __name__ == "__main__":
    w = Wizard(1)
    f = Fighter(2)
    w.info()
    f.info()
    while True:
        if f.hp <= 0:
            print("Победа w")
            break
        f.attack(w)
        if w.hp <= 0:
            print("Победа f")
            break
        w.attack(f)


