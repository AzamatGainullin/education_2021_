from __future__ import annotations
from typing import Tuple, List
from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm
from random import shuffle, sample
from copy import deepcopy


class SendMoreMoney2(Chromosome):
    def __init__(self, letters: List[str]) -> None:
        self.letters: List[str] = letters
        self.slovar = {'SE':5, 'SN':2, 'SD':4, 'EN':1, 'ND':3, 'ES':5, 'NS':2, 'DS':4, 'NE':1, 'DN':3, 'ED':5, 'DE':5}

    def fitness(self) -> float:
        dist1 = self.slovar[self.letters[0] + self.letters[1]]
        dist2 = self.slovar[self.letters[1] + self.letters[2]]
        dist3 = self.slovar[self.letters[2] + self.letters[3]]
        dist = dist1 + dist2 + dist3

        return dist

    @classmethod
    def random_instance(cls) -> SendMoreMoney2:
        letters = ["S", "E", "N", "D"]
        shuffle(letters)
        return SendMoreMoney2(letters)

    def crossover(self, other: SendMoreMoney2) -> Tuple[SendMoreMoney2, SendMoreMoney2]:
        child1: SendMoreMoney2 = deepcopy(self)
        child2: SendMoreMoney2 = deepcopy(other)
        idx1, idx2 = sample(range(len(self.letters)), k=2)
        l1, l2 = child1.letters[idx1], child2.letters[idx2]
        child1.letters[child1.letters.index(l2)], child1.letters[idx2] = child1.letters[idx2], l2
        child2.letters[child2.letters.index(l1)], child2.letters[idx1] = child2.letters[idx1], l1
        return child1, child2

    def mutate(self) -> None: # swap two letters' locations
        idx1, idx2 = sample(range(len(self.letters)), k=2)
        self.letters[idx1], self.letters[idx2] = self.letters[idx2], self.letters[idx1]

    def __str__(self) -> str:

        return f" letters: {self.letters}"


if __name__ == "__main__":
    initial_population: List[SendMoreMoney2] = [SendMoreMoney2.random_instance() for _ in range(3)]
    ga: GeneticAlgorithm[SendMoreMoney2] = GeneticAlgorithm(initial_population=initial_population, threshold=50, max_generations = 20, mutation_chance = 0.2, crossover_chance = 0.7, selection_type=GeneticAlgorithm.SelectionType.ROULETTE)
    result: SendMoreMoney2 = ga.run()
    print(result)
