from Population import *
from DNA import *
import ModelLoader
import GraphBuilder
from numpy import *

# we want to create new population in size of 1000 models
populationSize = 1000
checkRange = range(-10,10)

# the ideal function we want to copy


def trainFunction(x): return (x*5)/2


# initialize the pupulation
p = Population(population_size=populationSize, max_dna_height=10)

# uncomment the following line to silent the train process
# p.silence = True

# uncomment the following line to save the train progress to 'train_info.txt' file
# p.output_train_file = 'train_info.txt'

# train the population on the train function in range of 0 to 30,
# stop trainning when found model with fitness higher then 0.98
# if the function error is higher then 100 in some point -> model fitness is 0
# return : [ <BEST_MODEL_DNA_OBJ> , <BEST_MODEL_FITNESS_FLOAT> , <BEST_MODEL_GENERATION> ]
best_model_stats = p.train_population(
    trainFunction, checkRange, fitness_threshold=0.98,fitness_tolerance=1000)

# print the best model evaluation function
print_eval_function(best_model_stats[0].data)

# uncomment the following line to show the train graph from the output file
# p.show_train_graph()

# GraphBuilder.compare_graph(
#     best_model_stats[0].evaluate, 
#     trainFunction, 
#     checkRange)

# save the best model to 'best_model_cos.dna' file
# ModelLoader.save_dna('best_model.dna', best_model_stats[0].data)

# uncomment the following line to load the best model to 'best_model_cos.dna' file
# dna = ModelLoader.load_dna('best_model_cos.dna')
# print_eval_function(dna)
