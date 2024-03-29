from DNA import *
import Nodes
from collections import Counter
import math
import GraphBuilder
import ModelLoader
import copy


class Population(object):
    def __init__(self, population_size=100, max_dna_height=6):
        self.population_size = population_size
        self.max_dna_height = max_dna_height
        self.silence = False
        self.population = []
        self.output_train_file = None

    def get_best_model(self):
        return self.population[len(self.population)-1]

    def create_random_population(self):
        for _ in range(self.population_size):
            self.population.append(
                [DNA(get_rand_base_function(), self.max_dna_height), -1])

    def create_population_from_file(self,file_name):
        first_dna = ModelLoader.load_dna(file_name)
        for _ in range(self.population_size):
            self.population.append([DNA(get_rand_base_function(), self.max_dna_height,optionalData=copy.deepcopy(first_dna)),-1])


    def evaluate_individual_in_range(self, Individual, func_range, ideal_check):
        try:
            error = 0
            for i in func_range:
                temp = abs(Individual.evaluate(i) - ideal_check(i))
                error += temp
            return error
        except ZeroDivisionError:
            return -1

    def normal_fitness(self, fitness, _max):
        if fitness > _max or fitness < 0:
            return 0
        return 1-(fitness/_max)

    def calculate_gen_fitness(self, func_range, ideal_check, fitness_tolerance):
        for child in self.population:
            child[1] = self.evaluate_individual_in_range(
                child[0], func_range, ideal_check)

        maximum = max(self.population, key=lambda child: child[1])[1]
        minimum = min(self.population, key=lambda child: child[1] if child[1]>=0 else maximum)[1]

        if maximum == minimum:
            for child in self.population:
                child[1] = 0.5
            return

        for child in self.population:
            child[1] = self.normal_fitness(
                child[1], min([maximum, fitness_tolerance]))

        self.population.sort(key=lambda child: child[1])

    def create_new_gen(self):

        for child in self.population:
            func_point = math.sqrt(child[1])

            if random.uniform(0, 1) >= func_point:
                self.population.remove(child)

        temp = []
        for _ in range(self.population_size):
            if max(list(map(lambda child: child[1], self.population))) == 0:
                self.create_random_population()
                return
            father_index = random.randint(0, len(self.population)-1)
            mother_index = random.randint(0, len(self.population)-1)

            while father_index == mother_index:
                father_index = random.randint(0, len(self.population)-1)
                mother_index = random.randint(0, len(self.population)-1)

            father = self.population[father_index][0]
            mother = self.population[mother_index][0]
            opt = [father, mother]
            child = createChild(father, mother)
            while not checkTreeHeight(child.data, self.max_dna_height):
                child = createChild(father, mother)
            while not Nodes.checkTreeHeight(child.data, self.max_dna_height):
                child = createChild(father, mother)
            temp.append(child)

        self.population = list(
            map(lambda child: [child, -1, Nodes.getTreeHeight(child.data)], temp))

    def print_gen_to_file(self, gen_index, best_fitness):
        if self.output_train_file is not None:
            f = open(self.output_train_file, "a")
            f.write(str(gen_index) + "," + str(best_fitness)+"\n")
            f.close()

    def format_output_file(self):
        if self.output_train_file is not None:
            open(self.output_train_file, 'w').close()

    def show_train_graph(self):
        GraphBuilder.show_graph(self.output_train_file)

    def train_population(self, train_function, train_range, fitness_threshold=0.95, generation_limit=-1, fitness_tolerance=1000,train_dna_file=None):
        gen_indx = 0
        self.format_output_file()
        
        if train_dna_file is not None:
            self.create_population_from_file(train_dna_file)
        else:
            self.create_random_population()

        self.calculate_gen_fitness(
            train_range, train_function, fitness_tolerance)

        best_model = self.get_best_model()
        best_model_dna = best_model[0]
        best_model_fitness = best_model[1]

        self.print_gen_to_file(gen_indx, best_model_fitness)

        if not self.silence:
            print("generation " + str(gen_indx) +
                  " fitness " + str(best_model_fitness))

        while best_model_fitness < fitness_threshold:
            if generation_limit >= gen_indx:
                break
            self.create_new_gen()
            self.calculate_gen_fitness(
                train_range, train_function, fitness_tolerance)
            best_model = self.get_best_model()
            best_model_dna = best_model[0]
            best_model_fitness = best_model[1]

            gen_indx += 1

            self.print_gen_to_file(gen_indx, best_model_fitness)

            if not self.silence:
                print("generation " + str(gen_indx) +
                      " fitness " + str(best_model_fitness))

        return [best_model_dna, best_model_fitness, gen_indx]