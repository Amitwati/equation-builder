from Population import Population
import random
from collections import Counter
from DNA import *
from Nodes import *
import math



def test_model(model, test):
    for i in range(0, 10):
        print("model("+str(i)+") = " + str(model.evaluate(i)) +
              " | " + str(test(i)) + " = test("+str(i)+")")
    print("----------")

def test_func(x): return (x*x/2)*5

pop_size = 500

p = Population(population_size=pop_size,max_dna_height=10)
model_stats = p.train_population(test_func, range(0, 10), fitness_threshold=0.98, fitness_tolerance=1000)
print("********* RESULTS *********")
print("generations : " + str(model_stats[2]))
print("fitness : " + str(model_stats[1]))
print("model : ")
print_eval_function(model_stats[0].data)
print("------------")
test_model(model_stats[0],test_func)
