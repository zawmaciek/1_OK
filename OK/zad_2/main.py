from mknapsack import solve_unbounded_knapsack
import time

t = time.time()
value = [100, 200, 60, 150, 250]
weights = [3, 5, 2, 4, 6]
capacity = 50
res = solve_unbounded_knapsack(value, weights, capacity)
for weight, count in zip(weights, res):
    print(f"Przedmiot o wadze {weight} zapakowany {count} razy")
print(f"Wartosc: {sum([count * weight for count, weight in zip(value, res)])}")
print(f"Waga calkowita: {sum([count * weight for count, weight in zip(weights, res)])}")
print(f'Czas Rozwiazywania:{time.time() - t} s')
