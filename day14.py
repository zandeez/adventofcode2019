#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, field
from itertools import count
from sys import stderr
from typing import List, Dict, Tuple


@dataclass
class Ingredient:
    name: str
    amount: int = 0

    @staticmethod
    def parse(ingredient: str):
        a, i = ingredient.strip().split(" ")
        return Ingredient(name=i, amount=int(a))


@dataclass()
class Recipe:
    result: Ingredient = field(default_factory=Ingredient)
    ingredients: List[Ingredient] = field(default_factory=list)

    @staticmethod
    def parse(recipe: str) -> Recipe:
        ingredient_string, result_string = recipe.split("=>")
        result = Ingredient.parse(result_string)
        ingredients_array = ingredient_string.split(",")
        ingredients = [
            Ingredient.parse(s) for s in ingredients_array
        ]
        return Recipe(result=result, ingredients=ingredients)

    def ore_required(self, reactor: Reactor, qty: int = 1) -> int:
        if self.result.name == "ORE":
            return qty

        # Check reactor stock for spare
        stock_used: int = 0
        if self.result.name in reactor.stock and reactor.stock[self.result.name]:
            if reactor.stock[self.result.name] > qty:
                reactor.stock[self.result.name] -= qty
                stock_used = qty
            else:
                stock_used = reactor.stock[self.result.name]
                reactor.stock[self.result.name] = 0

        react_qty = qty - stock_used

        runs: int = (react_qty // self.result.amount) + ((react_qty % self.result.amount) > 0)
        excess: int = (self.result.amount * runs) - react_qty
        ore = sum([
            reactor.recipes[ingredient.name].ore_required(reactor, runs * ingredient.amount) for ingredient in
            self.ingredients
        ])
        # print(qty, self.result.name, "required, using", stock_used, "units of", self.result.name, "from stock",
        #       react_qty, "more units required from", runs, "runs, using", ore, "ORE (total).", excess,
        #       "units produced and stored in stock.")
        if excess:
            if self.result.name not in reactor.stock:
                reactor.stock[self.result.name] = 0
            reactor.stock[self.result.name] += excess
        return ore


class Reactor:
    recipes: Dict[str, Recipe] = field(default_factory=dict)
    stock: Dict[str, int] = field(default_factory=dict)
    FUEL = "FUEL"
    ORE = "ORE"

    def __init__(self):
        with open("day14.txt", "r") as file:
            self.recipes = dict([
                (recipe.result.name, recipe) for recipe in
                [Recipe.parse(line) for line in file.readlines()]
            ])
            self.recipes[Reactor.ORE] = Recipe(result=Ingredient(name=Reactor.ORE, amount=1))

    def make_fuel_target(self, qty=1):
        self.stock: Dict[str, int] = {}
        return self.recipes[Reactor.FUEL].ore_required(self, qty)

    def make_fuel_available(self, ore_qty=1000000000000):
        ore = ore_qty
        for i in count():
            required = self.recipes[Reactor.FUEL].ore_required(self, 1)
            if ore < required:
                return i - 1
            ore -= required

            print(ore, "remaining after producing", i+1, "fuel")

        return 0


reactor = Reactor()
pt1 = reactor.make_fuel_target()
print("Part 1:", pt1)

target = 1000000000000
current = target // pt1
ore_used = 0
while ore_used < 1000000000000:
    ore_used = reactor.make_fuel_target(current)
    remaining_ore = target - ore_used
    extra = remaining_ore // pt1
    current += extra
    if extra == 0:
        break

print("Part 2:", current)