import time
from capacity_checker import get_total_capacity

time.sleep(5)

gold_cap = get_total_capacity("gold")
elixir_cap = get_total_capacity("elixir")
print(f"Вместимость золота: {gold_cap}, эликсира: {elixir_cap}")
