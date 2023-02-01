#encoding: utf8

# YOUR NAME: PEDRO DUARTE SOARES FERREIRA
# YOUR NUMBER: 98620

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT:
# - ...
# - ...

from semantic_network import *
from bayes_net import *
from constraintsearch import *


class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def is_object(self,user,obj):
        declarations = self.query_local(user=user)
        for d in declarations:
            if isinstance(d.relation,Member) and d.relation.entity1 == obj or \
            isinstance(d.relation,Association) and d.relation.card == None and \
            (d.relation.entity2 == obj or d.relation.entity1 == obj):
                return True
        return False

    def is_type(self,user,type):
        """Checks if the type type exists in user declarations"""
        declarations = self.query_local(user=user)
        for d in declarations:
            if isinstance(d.relation,Member) and d.relation.entity2 == type or \
            isinstance(d.relation,Subtype) and (d.relation.entity2 == type or d.relation.entity1 == type) or \
            isinstance(d.relation,Association) and d.relation.card != None and \
            (d.relation.entity2 == type or d.relation.entity1 == type):
                return True
        return False

    def infer_type(self, user, obj):
        """Infers the type of an object based on the declarations of user"""
        if not self.is_object(user,obj):
            return None

        query = self.query_local(user=user)
        for d in query:
            if isinstance(d.relation,Member) and d.relation.entity1 == obj:
                return d.relation.entity2
            elif isinstance(d.relation, Subtype) and d.relation.entity1 == obj:
                return d.relation.entity2
            elif isinstance(d.relation, Subtype) and d.relation.entity2 == obj:
                return d.relation.entity1
            elif isinstance(d.relation,Association) and d.relation.card == None and \
            (d.relation.entity2 == obj or d.relation.entity1 == obj):
                # Go through though associations by user and check if entity2 was declared as a type
                for d2 in self.query_local(user=user, rel=d.relation.name):
                    if isinstance(d2.relation,Association) and d2.relation.card != None:
                        return d2.relation.entity2
        return "__unknown__"


    def infer_signature(self, user, assoc):
        """Infers the signature of the association based on the declarations of user"""
        declarations = self.query_local(user=user, rel=assoc)
        if declarations:
            for d in declarations:
                if self.is_type(user,d.relation.entity2):
                    return (d.relation.entity1, d.relation.entity2)
            return (self.infer_type(user,declarations[0].relation.entity1), self.infer_type(user,declarations[0].relation.entity2))
        else:
            return None

class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)

    def markov_blanket(self,var):
        """Returns the Markov blanket of var"""

        # Variables pointing to var
        parents = self.dependencies[var][0][0] + \
                    self.dependencies[var][0][1]


        # Variables pointed by var
        children = []
        # Variables pointing to children
        spouses = []
        for _var in self.dependencies:
            _var_dependencies = self.dependencies[_var][0][0] + \
                                self.dependencies[_var][0][1]
            # Get variables var is pointing to
            if var in _var_dependencies and _var not in children:
                children.append(_var)
                spouses.extend(_var_dependencies)

        spouses = list(set(spouses))
        spouses.remove(var)

        # Return the union of the three sets
        return list(set(parents + children + spouses))


class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def propagate(self, domains, var):
        """Propagates the constraints to the domains"""
        # Get edges containing var
        edges = [(v1,v2) for (v1,v2) in self.constraints if v2==var]
        while edges!=[]:
            (xj,xi) = edges.pop()

            constraint = self.constraints[xj,xi]

            # Create new domain without inconsistent values
            new_domain = []
            for x1 in domains[xj]:
                for x2 in domains[xi]:
                    if constraint(xj,x1,xi,x2):
                        new_domain += [x1]
                        break
                    
            # If the domain changed, update domain and add edges to the queue
            if len(new_domain)<len(domains[xj]):
               domains[xj] = new_domain
               edges += [(v1,v2) for (v1,v2) in self.constraints if v2==xj]
            
    def higherorder2binary(self,ho_c_vars,unary_c):
        # IMPLEMENT HERE
        pass


