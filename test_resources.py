import time
from resources import get_resources, get_townhall_level

time.sleep(5)

gold, elixir, gems = get_resources()
print(f"Золото: {gold}, Эликсир: {elixir}, Гемы: {gems}")

level = get_townhall_level()
print(f"Уровень ратуши: {level}")
