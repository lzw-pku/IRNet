from sql2nl import Node
from copy import deepcopy
import re
#def exchange_filter(node):


def refactor(node, mode):
    #print(node)
    sql_tree_list = []
    child_list = []
    for child in node.children:
        if isinstance(child, Node):
            child_list.append(refactor(child, mode))
        else:
            child_list.append([child])

    def dfs(child_list):
        if len(child_list) == 1:
            return [[c] for c in child_list[0]]
        ret = []
        tmp = dfs(child_list[1:])
        #print(tmp)
        for child in child_list[0]:
            ret += [[child] + c for c in tmp]
        return ret

    #print(child_list)
    #print(dfs(child_list))
    tmp = dfs(child_list)
    for child in tmp:
        new_node = deepcopy(node)
        new_node.children = deepcopy(child)
        sql_tree_list.append(new_node)


    if 'Filter' in mode and \
            (node.statement == 'and Filter Filter' or node.statement == 'or Filter Filter'):
        assert len(node.children) == 3 and (node.children[0] == 'and' or node.children[0] == 'or')
        for child1 in child_list[1]:
            for child2 in child_list[2]:
                new_node = deepcopy(node)
                new_node.children = deepcopy([child2, child1])
                sql_tree_list.append(new_node)

        #node.children = [node.children[1], node.children[0]]
    if 'Intersect' in mode and node.statement == 'intersect Root Root':
        assert len(node.children) == 3 and node.children[0] == 'intersect'
        for child1 in child_list[1]:
            for child2 in child_list[2]:
                new_node = deepcopy(node)
                new_node.children = deepcopy([child2, child1])
                sql_tree_list.append(new_node)

    if 'Select' in mode and re.match('A( A)*', node.statement) != None:
        assert all([len(c) == 1 for c in child_list])
        for i in range(1, len(child_list)):
            new_node = deepcopy(node)
            new_node.children = deepcopy([c[0] for c in child_list[i:] + child_list[:i]])
            sql_tree_list.append(new_node)

    return sql_tree_list
