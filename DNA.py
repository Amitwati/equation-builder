import random
from Nodes import *
import copy
import math

base_function = [
    [lambda param: param**2, "(x^2)"],
]


num_of_terminals = 3
# nodeList = ["Number",, "Plus", "Minus","Multiply", "Divide","SIN"]
nodeList = ["Number","PARAM", "Plus", "Minus","Multiply", "Divide","SIN"]


def mutateTree(tree):
    if random.randint(0, 100) != random.randint(0, 100):
        organize(tree)
        return tree

    rand_node_depth = random.randint(
        0, getTreeHeight(tree))
    temp = tree
    if temp.isTerminal or rand_node_depth == 0:
        temp = DNA(get_rand_base_function(), 5).data
        organize(temp)
        return temp

    for _ in range(0, rand_node_depth):
        num_of_children = len(temp.children)
        rand_indx = random.randint(0, num_of_children-1)

        if temp.children[rand_indx].isTerminal:
            temp = DNA(get_rand_base_function(), 4).data
            organize(temp)
            return temp

        temp = temp.children[rand_indx]

    num_of_children = len(temp.children)
    rand_indx = random.randint(0, num_of_children-1)

    temp.children[rand_indx] = DNA(get_rand_base_function(), 4).data
    organize(tree)
    return tree


def createChild(father, mother):

    dna_options = [copy.deepcopy(father), copy.deepcopy(mother)]
    rand_indx = -1

    child_max_height = max([father.max_height, mother.max_height])

    bottom_tree_index = random.randint(0, 1)
    upper_tree_index = 1-bottom_tree_index

    bottom_tree = dna_options[bottom_tree_index].data
    upper_tree = dna_options[upper_tree_index].data

    # ------------ started get middle_node

    middle_node = upper_tree

    if middle_node.isTerminal:
        child = dna_options[random.randint(0, 1)]
        child.data = mutateTree(child.data)
        return child

    rand_node_depth = random.randint(0, getTreeHeight(upper_tree))

    # if middle_node.mark == "sin":
    #     print("here!")
    

    for _ in range(rand_node_depth-1):
        num_of_children = len(middle_node.children)
        middle_rand_indx = random.randint(0, num_of_children-1)

        if middle_node.children[middle_rand_indx].isTerminal:
            break

        middle_node = middle_node.children[middle_rand_indx]

    middle_rand_indx = random.randint(0, middle_node.numOfChildren-1)

    # ------------ finished get middle_node

    # ------------ start get bottom_tree
    rand_node_depth = random.randint(0, getTreeHeight(bottom_tree))

    if not bottom_tree.isTerminal:
        # while getTreeHeight(bottom_tree) >
        for _ in range(0, rand_node_depth):
            if bottom_tree.isTerminal:
                break

            num_of_children = len(bottom_tree.children)
            rand_indx = random.randint(0, num_of_children-1)
            bottom_tree = bottom_tree.children[rand_indx]

    # ------------ start get bottom_tree

    # if middle_node and rand_indx >= 0:
    middle_node.children[middle_rand_indx] = bottom_tree

    organize(upper_tree)

    upper_tree = mutateTree(upper_tree)

    child = DNA(dna_options[random.randint(0, 1)].input_func,
                getTreeHeight(upper_tree), upper_tree)
    return child


def get_rand_base_function():
    return base_function[random.randint(0, len(base_function)-1)]


def print_eval_function(tree):
    print(tree.get_str())


class DNA(object):

    def __init__(self, inputFunction, max_height, optionalData=None):
        self.max_height = max_height
        self.input_func = inputFunction
        if optionalData is None:
            if inputFunction is None:
                self.data = self.buildRandomTree(
                    get_rand_base_function(), max_height)
            else:
                self.data = self.buildRandomTree(inputFunction, max_height)
        else:
            self.data = optionalData

    def pickRandomNodeType(self):
        indx = random.randint(0, len(nodeList)-1)
        return nodeList[indx]

    def buildRandomTree(self, inputFunction, max_height):
        global num_of_terminals
        if max_height == 1:
            head_type = nodeList[random.randint(0, num_of_terminals)]
            if head_type == "Number":
                head = Number(random.randint(0, 100))
            elif head_type == "Input":
                head = Input(inputFunction)
                return head
            else:
                head = Param()
                return head
        else:
            head_type = self.pickRandomNodeType()
            if head_type == "Number":
                head = Number(random.randint(0, 100))
                return head
            elif head_type == "Input":
                head = Input(inputFunction)
                return head
            elif head_type == "PARAM":
                head = Param()
                return head
            

            head = getNode(head_type)
            self._buildRandomTree(head, inputFunction, max_height-1)
            return head

    def _buildRandomTree(self, head, inputFunction, max_height):
        global num_of_terminals
        if max_height == 2:
            for _ in range(0, head.numOfChildren):
                temp = random.randint(0, num_of_terminals)
                if nodeList[temp] == "Number":
                    head.addChild(Number(random.randint(0, 100)))
                elif nodeList[temp] == "Input":
                    head.addChild(Input(inputFunction))
                else:
                    head.addChild(Param())
            return head

        for i in range(0, head.numOfChildren):
            childType = self.pickRandomNodeType()
            if childType == "Number":
                head.addChild(Number(random.randint(0, 100)))
                continue
            elif childType == "Input":
                head.addChild(Input(inputFunction))
                continue
            else:
                head.addChild(Param())
                continue
            head.addChild(getNode(childType))
            self._buildRandomTree(
                head.children[i], inputFunction, max_height-1)

    def evaluate(self, param):
        return self.data.evaluate(param)
