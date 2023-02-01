# Pedro Duarte Soares Ferreira
# NMEC: 98620
# IA 2022/23

from tree_search import *
from cidades import *
from blocksworld import *


def func_branching(connections,coordinates):
    """Returns an estimate of the branching factor of the problem."""

    number_of_neighbors = []
    for coordinate in coordinates:
        counter = 0
        for connection in connections:
            if coordinate in connection:
                counter += 1
        number_of_neighbors.append(counter)

    return sum(number_of_neighbors)/len(number_of_neighbors)-1


class MyCities(Cidades):
    def __init__(self,connections,coordinates):
        super().__init__(connections,coordinates)
        self.branching_estimate = func_branching(self.connections, self.coordinates)

class MySTRIPS(STRIPS):
    def __init__(self,optimize=False):
        super().__init__(optimize)

    def simulate_plan(self,state,plan):
        # Break condition
        if not plan:
            return set(state)

        action = plan.pop(0)
        
        for i in action.pc:
            if i not in state:
                return None
        
        [state.remove(i) for i in action.neg]
        [state.append(i) for i in action.pos]

        # Recursive call
        return self.simulate_plan(state,plan)
 
class MyNode(SearchNode):
    def __init__(self,state,parent,cost=0,heuristic=0,depth=0):
        super().__init__(state,parent)
        self.cost = cost
        self.heuristic = heuristic
        self.depth = depth

class MyTree(SearchTree):

    def __init__(self,problem,strategy='breadth',optimize=0,keep=0.25): 
        super().__init__(problem,strategy)
        self.optimize = optimize
        self.keep = keep

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)

        if self.strategy == 'A*':
            if self.optimize == 0:
                nodes = [(i, self.all_nodes[i]) for i in self.open_nodes]
                # sort by f(n) = g(n) + h(n)
                nodes.sort(key=lambda x: x[1].cost + x[1].heuristic)
                self.open_nodes = [i[0] for i in nodes]
            else:
                nodes = [(i, self.all_nodes[i]) for i in self.open_nodes]
                # sort by f(n) = g(n) + h(n)
                nodes.sort(key=lambda x: x[1][2] + x[1][3])
                self.open_nodes = [i[0] for i in nodes]
        else:
            # IBA*
            self.forget_worst_terminals()


    # remove a fraction of open (terminal) nodes
    # with lowest evaluation function
    # (used in Incrementally Bounded A*)
    def forget_worst_terminals(self):
        if self.optimize == 0:
            # Get nodes with index in open_nodes
            nodes = [(i, self.all_nodes[i]) for i in self.open_nodes]

            # Get average depth from nodes
            avg_depth = sum([node[1].depth for node in nodes])/len(nodes)

            max_nodes_given_depth = self.problem.domain.branching_estimate**avg_depth

            num_keep = int(self.keep*max_nodes_given_depth)+1

            # sort by f(n) = g(n) + h(n)
            nodes.sort(key=lambda x: x[1].cost + x[1].heuristic)
            # remove nodes with worst f(n)
            self.open_nodes = [i[0] for i in nodes[:num_keep]]

        elif self.optimize == 1:
            # Get nodes with index in open_nodes
            nodes = [(i, self.all_nodes[i]) for i in self.open_nodes]

            # Get average depth from nodes
            avg_depth = sum([node[1][4] for node in nodes])/len(nodes)

            max_nodes_given_depth = self.problem.domain.branching_estimate**avg_depth

            num_keep = int(self.keep*max_nodes_given_depth)+1

            # sort by f(n) = g(n) + h(n)
            nodes.sort(key=lambda x: x[1][2] + x[1][3])

            # remove nodes with worst f(n)
            self.open_nodes = [i[0] for i in nodes[:num_keep]]
            
        else:
            # Get nodes with index in open_nodes
            nodes = [(i, self.all_nodes[i]) for i in self.open_nodes]

            # Get average depth from nodes
            avg_depth = sum([node[1][4] for node in nodes])/len(nodes)

            max_nodes_given_depth = self.problem[0][5]**avg_depth

            num_keep = int(self.keep*max_nodes_given_depth)+1

            # sort by f(n) = g(n) + h(n)
            nodes.sort(key=lambda x: x[1][2] + x[1][3])

            # remove nodes with worst f(n)
            self.open_nodes = [i[0] for i in nodes[:num_keep]]


    # procurar a solucao
    def search2(self):
        opt = self.optimize
        if opt == 0:
            return self.search_opt_0()
        elif opt == 1:
            return self.search_opt_1()
        elif opt == 2:
            return self.search_opt_2()
        elif opt == 4:
            return self.search_opt_4()

    def get_path_tuple(self,node):
        if node[1] == None:
            return [node[0]]
        path = self.get_path_tuple(self.all_nodes[node[1]])
        path += [node[0]]
        return(path)

    def goal_test_tuple(self, state):
        return self.problem[0][4](state,self.problem[2])

    def search_opt_0(self):
        root = MyNode(self.problem.initial, None, heuristic=self.problem.domain.heuristic(self.problem.initial,self.problem.goal))
        self.all_nodes = [root]
        self.open_nodes = [0]

        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]

            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path(node)
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):

                newstate = self.problem.domain.result(node.state,a)

                if newstate not in self.get_path(node):

                    cost = node.cost + self.problem.domain.cost(node.state, (node.state, newstate))
                    heuristic = self.problem.domain.heuristic(newstate,self.problem.goal)
                    depth = node.depth + 1

                    newnode = MyNode(newstate, nodeID, cost, heuristic, depth)

                    lnewnodes.append(len(self.all_nodes))
                    self.all_nodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    def search_opt_1(self):
        root = (self.problem.initial, None, 0, self.problem.domain.heuristic(self.problem.initial,self.problem.goal), 0)
        self.all_nodes = [root]
        self.open_nodes = [0]

        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]

            if self.problem.goal_test(node[0]):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path_tuple(node)
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node[0]):

                newstate = self.problem.domain.result(node[0],a)

                if newstate not in self.get_path_tuple(node):

                    cost = node[2] + self.problem.domain.cost(node[0], (node[0], newstate))
                    heuristic = self.problem.domain.heuristic(newstate,self.problem.goal)
                    depth = node[4] + 1

                    newnode = (newstate, nodeID, cost, heuristic, depth)

                    lnewnodes.append(len(self.all_nodes))
                    self.all_nodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    def search_opt_2(self):
        root = (self.problem[1], None, 0, self.problem[0][3](self.problem[1],self.problem[2]), 0)
        self.all_nodes = [root]
        self.open_nodes = [0]

        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]

            if self.goal_test_tuple(node[0]):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path_tuple(node)
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem[0][0](node[0]):

                newstate = self.problem[0][1](node[0],a)

                if newstate not in self.get_path_tuple(node):

                    cost = node[2] + self.problem[0][2](node[0], (node[0], newstate))
                    heuristic = self.problem[0][3](newstate,self.problem[2])
                    depth = node[4] + 1

                    newnode = (newstate, nodeID, cost, heuristic, depth)

                    lnewnodes.append(len(self.all_nodes))
                    self.all_nodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    def search_opt_4(self):
        root = (self.problem[1], None, 0, self.problem[0][3](self.problem[1],self.problem[2]), 0)
        self.all_nodes = [root]
        self.open_nodes = [0]
        self.closed_nodes = []

        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            self.closed_nodes.append(nodeID)

            if self.goal_test_tuple(node[0]):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path_tuple(node)
            lnewnodes = []
            self.non_terminals += 1

            for a in self.problem[0][0](node[0]):

                newstate = self.problem[0][1](node[0],a)
                if newstate not in self.get_path_tuple(node):

                    cost = node[2] + self.problem[0][2](node[0], (node[0], newstate))
                    heuristic = self.problem[0][3](newstate,self.problem[2])
                    depth = node[4] + 1
                    newnode = (newstate, nodeID, cost, heuristic, depth)

                    if not self.is_in_closed(newstate) and not self.is_in_open(newstate):
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                    
                    else:
                        for _id, _node in enumerate(self.all_nodes):
                            if _node[0] == newstate:
                                if _node[2] > cost:
                                    self.all_nodes[_id] = newnode
    
            self.add_to_open(lnewnodes)
        return None


    def is_in_closed(self, state):
        for nodeID in self.closed_nodes:
            if self.all_nodes[nodeID][0] == state:
                return True
        return False
    
    def is_in_open(self, state):
        for nodeID in self.open_nodes:
            if self.all_nodes[nodeID][0] == state:
                return True
        return False