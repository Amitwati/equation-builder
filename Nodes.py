import random

max_depth = 6



def organize(tree, height=0, depth_to_orgenaize=5):
    if height <= depth_to_orgenaize and not tree.isTerminal:
        tree.height = height
        for child in tree.children:
            organize(child, height+1, depth_to_orgenaize)
    else:
        tree.height = height


class Node(object):
    def __init__(self):
        self.height = 0
        self.isTerminal = False
        self.numOfChildren = -1
        self.infChildren = False
        self.mark = "?"
        self.isFunction = False

    def setHeight(self, height):
        self.height = height

    def evaluate(self, param):
        pass


class Number(Node):
    def __init__(self, value):
        Node.__init__(self)
        self.numOfChildren = 0
        self.isTerminal = True
        self.infChildren = False
        self.value = value

    def get_str(self):
        return str(self.value)

    def evaluate(self, param):
        return self.value


class Input(Node):
    def __init__(self, get_input):
        Node.__init__(self)
        self.numOfChildren = 0
        self.isTerminal = True
        self.infChildren = False
        self.get_input = get_input

    def get_str(self):
        return self.get_input[1]

    def evaluate(self, param):
        if self.get_input is not None:
            return self.get_input[0](param)
        return 0


class Plus(Node):
    def __init__(self):
        Node.__init__(self)
        self.mark = "+"
        self.numOfChildren = 2
        self.infChildren = True
        self.children = []

    def setHeight(self, height):
        self.height = height
        for child in self.children:
            child.setHeight(self.height + 1)

    def addChild(self, child):
        child.setHeight(self.height + 1)
        self.children += [child]

    def get_str(self):
        return "(" + self.children[0].get_str() + " + " + self.children[1].get_str() + ")"

    def evaluate(self, param):
        retVal = 0
        for child in self.children:
            retVal += child.evaluate(param)
        return retVal


class Minus(Node):
    def __init__(self):
        Node.__init__(self)
        self.numOfChildren = 2
        self.infChildren = False
        self.mark = "-"
        self.children = []

    def setHeight(self, height):
        self.height = height
        for child in self.children:
            child.setHeight(self.height + 1)

    def addChild(self, child):
        child.setHeight(self.height + 1)
        self.children += [child]

    def get_str(self):
        return "(" + self.children[0].get_str() + " - " + self.children[1].get_str() + ")"

    def evaluate(self, param):

        return (self.children[0].evaluate(param)) - (self.children[1].evaluate(param))


class Multiply(Node):
    def __init__(self):
        Node.__init__(self)
        self.numOfChildren = 2
        self.infChildren = True
        self.mark = "*"
        self.children = []

    def setHeight(self, height):
        self.height = height
        for child in self.children:
            child.setHeight(self.height + 1)

    def addChild(self, child):
        child.height = self.height + 1
        self.children += [child]

    def get_str(self):
        return "(" + self.children[0].get_str() + " * " + self.children[1].get_str() + ")"

    def evaluate(self, param):
        retVal = 1
        for child in self.children:
            retVal *= child.evaluate(param)
        return retVal


class Divide(Node):
    def __init__(self):
        Node.__init__(self)
        self.numOfChildren = 2
        self.infChildren = False
        self.mark = "/"
        self.children = []

    def setHeight(self, height):
        self.height = height
        for child in self.children:
            child.setHeight(self.height + 1)

    def addChild(self, child):
        child.height = self.height + 1
        self.children += [child]

    def get_str(self):
        return "(" + self.children[0].get_str() + " / " + self.children[1].get_str() + ")"

    def evaluate(self, param):
        try:
            return (self.children[0].evaluate(param))/(self.children[1].evaluate(param))
        except ZeroDivisionError:
            return 1


class Power(Node):
    def __init__(self):
        Node.__init__(self)
        self.numOfChildren = 2
        self.infChildren = False
        self.mark = "^"
        self.children = []

    def setHeight(self, height):
        self.height = height
        for child in self.children:
            child.setHeight(self.height + 1)

    def addChild(self, child):
        child.height = self.height + 1
        self.children += [child]

    def get_str(self):
        return "(" + self.children[0].get_str() + "^" + self.children[1].get_str() + ")"

    def evaluate(self, param):
        return (self.children[0].evaluate(param))**(self.children[1].evaluate(param))


class Max(Node):
    def __init__(self):
        Node.__init__(self)
        self.numOfChildren = 2
        self.infChildren = True
        self.isFunction = True
        self.mark = "max"
        self.children = []

    def setHeight(self, height):
        self.height = height
        for child in self.children:
            child.setHeight(self.height + 1)

    def addChild(self, child):
        child.height = self.height + 1
        self.children += [child]

    def get_str(self):
        return "max(" + self.children[0].get_str() + "," + self.children[1].get_str() + ")"

    def evaluate(self, param):
        eval_list = []
        for child in self.children:
            eval_list.append(child.evaluate(param))
        return max(eval_list)


class Min(Node):
    def __init__(self):
        Node.__init__(self)
        self.numOfChildren = 2
        self.infChildren = True
        self.isFunction = True
        self.mark = "max"
        self.children = []

    def setHeight(self, height):
        self.height = height
        for child in self.children:
            child.setHeight(self.height + 1)

    def get_str(self):
        return "max(" + self.children[0].get_str() + "," + self.children[1].get_str() + ")"

    def addChild(self, child):
        child.height = self.height + 1
        self.children += [child]

    def evaluate(self, param):
        eval_list = []
        for child in self.children:
            eval_list.append(child.evaluate(param))
        return min(eval_list)


def getNode(node):
    if node == "Plus":
        return Plus()
    elif node == "Minus":
        return Minus()
    elif node == "Multiply":
        return Multiply()
    elif node == "Divide":
        return Divide()
    elif node == "Power":
        return Power()
    elif node == "MAX":
        return Max()
    elif node == "MIN":
        return Min()


def getTreeHeight(tree):
    # if tree.height > max_depth:
    #     return tree.height

    if tree.isTerminal:
        return tree.height

    maximum = 0
    for child in tree.children:
        temp = getTreeHeight(child)
        maximum = max([temp, maximum])
    return maximum


def checkTreeHeight(tree, max_height):
    if tree.isTerminal or tree.height > max_height:
        return tree.height <= max_height
    return max(list(map(lambda child: checkTreeHeight(child, max_height), tree.children)))
