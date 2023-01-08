from mknapsack import solve_unbounded_knapsack

# Given ten item types with the following profits and weights:
profits = [100, 200, 60, 150, 250]
weights = [3, 5, 2, 4, 6]

# ...and a knapsack with the following capacity:
capacity = 50

# Assign items repeatedly into the knapsack while maximizing profits
res = solve_unbounded_knapsack(profits, weights, capacity)
for weight, count in zip(weights,res):
    print(f"Przedmiot o wadze {weight} zapakowany {count} razy")
print(f"Wartosc: {sum([count*weight for count,weight in zip(profits,res)])}")
print(f"Waga calkowita: {sum([count*weight for count,weight in zip(weights,res)])}")