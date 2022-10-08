## Instalacja pakietow
```pip install -r requirements.txt```
## Rozwiazanie 1:

Wykorzystanie wszystkich permutacji group (brute force) z uzyciem funkcji get_all_unconnected_groups()
Zuzycie pamieci dla grafow o liczbie wierzcholkow >10 jest nierealne, jednak dla mniejszych dziala.

## Rozwiazanie 2:

Wykorzystanie gotowego rozwiazania do znalezienia maksymalnych niezaleznych grup z uzyciem funkcji
get_all_maximal_independent_subsets()
Rozwiazanie opiera sie na tym ze maksimum klik dopełnienia grafu oryginalnego to maksimum zbiorów niezależnych grafu
oryginalnego.

Dla grafow o liczbie wierzcholkow ~200 wynosi okolo 5s.