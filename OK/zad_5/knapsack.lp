% define list of items, with their sizes
items(item_1;item_2;item_3;item_4;item_5;item_6).
size(item_1,215).
size(item_2,275).
size(item_3,335).
size(item_4,355).
size(item_5,420).
size(item_6,580).
% Define max items count and knapsack total size
#const total = 1505.
#const max_count = 10.
% Generate numbers between 0 and max count
num(0..max_count).
% Pack some amount of each type of items
1 { packed(Item, Number) : num(Number) } 1 :- items(Item).
% Sum size so its equal to the total
#sum{(Size*N),F : packed(F,N) : size(F,Size), num(N)} == total.