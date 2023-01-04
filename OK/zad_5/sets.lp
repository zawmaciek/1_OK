
% Define the set L = {1, 2, ... , 44}
L = 1..44.

% Define the four subsets B1, B2, B3, and B4
B1 = {X : L(X)}.
B2 = {X : L(X)}.
B3 = {X : L(X)}.
B4 = {X : L(X)}.

% Each element of L must be in exactly one of the four subsets
1{in(X,B): B1; B2; B3; B4}1 :- L(X).

% If x, y ∈ B then x + y ∉ B for each of the four subsets
:- in(X, B), in(Y, B), in(X+Y, B).


% Output the four subsets
#show B1/1.
#show B2/1.
#show B3/1.
#show B4/1.