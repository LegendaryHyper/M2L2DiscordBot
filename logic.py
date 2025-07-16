import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
from datetime import timedelta
from datetime import datetime
class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.pokemon_strength = random.randint(1, 199)
        self.pokemon_health_max = random.randint(1, 999)
        self.pokemon_health_cur = self.pokemon_health_max
        self.last_feed_time = datetime.now()
        self.name = None
        self.image = None
        self.level = 1
        self.exp = 0
        self.exp_max = 200
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]
    async def show_lvl(self):
        return f"Pokemon'un seviyesi: {self.level}\n{self.exp}/{self.exp_max}"
    async def feed_pokemon(self, feed_cooldown = 20, heal_perdec = 3):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_cooldown)
        if current_time.timestamp() - self.last_feed_time.timestamp() >= feed_cooldown: # !
            output = f"LVL {self.level} - {self.exp}/{self.exp_max} --> "
            lvl_up_string = ""
            increase = random.randint(20,100)
            self.exp += increase
            if self.exp >= self.exp_max:
                self.exp -= self.exp_max
                self.level += 1
                self.exp_max *= 1.5
                self.exp_max = int(round(self.exp_max))
                self.pokemon_strength *= 1.2
                self.pokemon_strength = int(round(self.pokemon_strength))
                self.pokemon_health_max *= 1.2
                self.pokemon_strength = int(round(self.pokemon_health_max))
                self.pokemon_health_cur = self.pokemon_health_max
                if self.pokemon_health_cur + round(self.pokemon_health_max * heal_perdec / 10) > self.pokemon_health_max:
                    self.pokemon_health_cur = self.pokemon_health_max
                else:
                    self.pokemon_health_cur += round(self.pokemon_health_max * heal_perdec / 10)
                lvl_up_string = f"Leveled up to level {self.level}!"
            if lvl_up_string:
                output = output + f"LVL {self.level} - {self.exp}/{self.exp_max}\n\n+{increase} EXP\n" + lvl_up_string
            else:
                output = output + f"LVL {self.level} - {self.exp}/{self.exp_max}\n\n+{increase} EXP\n"
            return output
        else:
            return f"Pokemonunuzu {feed_cooldown - round(current_time.timestamp() - self.last_feed_time.timestamp())} saniye içinde besleyebilirsiniz." # !
    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name}\nPokemon'un Canı: {self.pokemon_health_cur}/{self.pokemon_health_max}\nPokemon'un Seviyesi: LVL {self.level} - {self.exp}/{self.exp_max}"  # Pokémon adını içeren dizeyi döndürür
    async def pokemon_str(self):
        if not self.pokemon_strength:
            self.name = await self.get_name()
        return f"Gücü: {self.pokemon_strength}"
    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data["sprites"]["front_default"]
                    return img_url
                else:
                    return None
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"
        if enemy.pokemon_health_cur > self.pokemon_strength:
            enemy.pokemon_health_cur -= self.pokemon_strength
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.pokemon_strength}"
        else:
            enemy.pokemon_health_cur = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
        self.pokemon_health_cur = self.pokemon_health_max
    
    async def show_total(self):
        return len(Pokemon.pokemons.keys)


class Wizard (Pokemon):
    async def feed_pokemon(self, feed_cooldown=10):
        return await super().feed_pokemon(feed_cooldown)

class Fighter (Pokemon):
    async def feed_pokemon(self, feed_cooldown = 20, heal_perdec = 5):
        return await super().feed_pokemon(feed_cooldown, heal_perdec)
    async def attack(self, enemy):
        super_strength = random.randint(5, 15)  
        self.pokemon_strength += super_strength
        sonuc = await super().attack(enemy)  
        self.pokemon_strength -= super_strength
        return sonuc + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_strength}"