

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):
        associations = []
        for d in self.declarations:
            if isinstance(d.relation, Association):
                associations.append(d.relation.name)
        return list(set(associations))

    def list_objects(self):
        objects = []
        for d in self.declarations:
            if isinstance(d.relation, Member):
                objects.append(d.relation.entity1)
        return list(set(objects))

    def list_users(self):
        users = []
        for d in self.declarations:
            if isinstance(d, Declaration):
                users.append(d.user)
        return list(set(users))

    def list_types(self):
        types = []
        for d in self.declarations:
            if isinstance(d.relation, Member) or isinstance(d.relation, Subtype):
                types.append(d.relation.entity2)
        return list(set(types))

    def list_local_associations(self, entity):
        query = self.query_local(e1 = entity)
        associations = []
        for d in query:
            if isinstance(d.relation, Association):
                associations.append(d.relation.name)
        return list(set(associations))

    def list_relations_by_user(self, user):
        query = self.query_local(user = user)
        relations = []
        for d in query:
            relations.append(d.relation.name)
            
        return list(set(relations))
    
    def associations_by_user(self, user):
        query = self.query_local(user = user)
        associations = []
        for d in query:
            if isinstance(d.relation, Association):
                if d.relation.name not in associations:
                    associations.append(d.relation.name)
        return len(associations)

    def list_local_associations_by_user(self, entity):
        query = self.query_local(e1 = entity)
        associations = []
        for d in query:
            if isinstance(d.relation, Association):
                associations.append((d.relation.name, d.user))
        return list(set(associations))

    def predecessor(self, entity_predecessor, entity):
        query = self.query_local(e2 = entity_predecessor)
        for d in query:
            if isinstance(d.relation, Subtype) or isinstance(d.relation, Member):
                if d.relation.entity1 == entity:
                    return True
                else:
                    return self.predecessor(d.relation.entity1, entity)
        return False
    
    def predecessor_path(self, entity_predecessor, entity):
        query = self.query_local(e2 = entity_predecessor)
        for d in query:
            if d.relation.entity1 == entity:
                return [entity_predecessor, entity]
            else:
                predecessors = self.predecessor_path(d.relation.entity1, entity)
                if predecessors:
                    return [entity_predecessor] + predecessors
        return None

    def query(self, entity, association = None):
        parents = []
        declarations = []

        query = self.query_local(e1 = entity)
        for d in query:
            if not isinstance(d.relation, Association):
                parents.append(d.relation.entity2)
            else:
                if association is None or d.relation.name == association:
                    declarations.append(d)

        for parent in parents:
            declarations += self.query(parent, association)

        return declarations

    def query2(self, entity, relation = None):
        query = self.query(entity)
        query2 = self.query_local(e1 = entity)
        for d in query2:
            if not isinstance(d.relation, Association) and\
            (relation is None or d.relation.name == relation):
                query.append(d)
        return query
