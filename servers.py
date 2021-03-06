#hejka
#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from re import fullmatch
from typing import Optional, List
from copy import deepcopy

class Product:

    def __hash__(self):
        return hash((self.name, self.price))

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i
    #  jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

# FIXME: Każada z poniższych klas serwerów powinna posiadać: (1) metodę inicjalizacyjną przyjmującą listę obiektów typu
#  `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze, (2) możliwość
#  odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę
#  wyników wyszukiwania, (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów
#  spełniających kryterium wyszukiwania


class Server(ABC):
    n_max_returned_entries = 3

    @abstractmethod
    def get_entries(self, n_letters: int = 1) -> List[Product]:
        raise NotImplemented


class ListServer(Server):
    def __init__(self, list_of_products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = deepcopy(list_of_products)

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        regex_string = r'^[a-zA-z]{' + str(n_letters) + r'}\d{2,3}'
        products_found = []
        for product in self.products:
            product_found = fullmatch(regex_string, product.name)
            if product_found is not None:
                products_found.append(product)
        if len(products_found) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            products_found.sort(key=lambda product: product.price)
            return products_found


class MapServer(Server):
    def __init__(self, list_of_products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = {product.name: product for product in list_of_products}

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        products_found = []
        # regex sprawdzajacy nazwe
        regex_string = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}'
        for product in self.products.keys():
            product_found = fullmatch(regex_string, product)

            # jesli znaleziono produkty to je dodaj do listy produktow
            if product_found is not None:
                products_found.append(self.products[product])

        # rzuc wyjatek jesli liczba produkow przekracza zalozona wartosc
        if len(products_found) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            products_found.sort(key=lambda product: product.price)
            return products_found


class Client:
    def __init__(self, server: Server):
        self.server = server

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        # jesli liczba produktow nie przekracza z gory zalozonej wartosci to sumujemy
        try:
            products_found = self.server.get_entries(n_letters)
            #POPRAWA żeby zwracało None
            if len(products_found)==0:
                return None
            total_price = sum(product.price for product in products_found)
            return total_price
        except TooManyProductsFoundError:
            return None
