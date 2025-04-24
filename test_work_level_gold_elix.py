# test_resources.py
from resources import get_resources
import time
time.sleep(3)
gold, elixir, gems = get_resources()

print(f"Золото: {gold}")
print(f"Эликсир: {elixir}")
print(f"Гемы: {gems}")
