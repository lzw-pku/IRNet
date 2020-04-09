# coding: utf-8

import random
import copy
from typing import List


def random_select(l):
    if isinstance(l, str):
        return l
    else:
        assert isinstance(l, List)
        return random.choice(l)


class Node:
    STATEMENT_TYPE = 0
    ROOT_TYPE = 1
    SELECT_TYPE = 2
    FILTER_TYPE = 3
    ORDER_TYPE = 4
    A_TYPE = 5

    N_TYPE = 6 # !!!!!!!!!!!!!
    SUP_TYPE = 7 # !!!!!!!!!!!!!!!!!!!

    COLUMN_TYPE = 11
    TABLE_TYPE = 12
    KEYWORD_TYPE = 13

    VALUE_TYPE = '3'

    TYPE_DICT = {'SQL': None, 'Statement': STATEMENT_TYPE, 'Root': ROOT_TYPE, 'Select': SELECT_TYPE, 'Filter': FILTER_TYPE,
                 'Order': ORDER_TYPE, 'A': A_TYPE, 'C': COLUMN_TYPE, 'T': TABLE_TYPE, 'Value': VALUE_TYPE,
                 'N': N_TYPE, 'Sup': SUP_TYPE} # !!!!!!!!!!!!!!!!!!!
    KEYWORD_LIST = [
        'intersect', 'union', 'except',  # Statement
        'asc', 'des', 'limit',  # Order
        'and', 'or', '>', '<', '>=', '<=', '=', '!=', 'between', 'like', 'not_like', 'in', 'not_in',  # Filter
        'max', 'min', 'count', 'sum', 'avg', 'none'  # A
    ]
    '''
    Root1: Statement
    Root -> Sel Sup Filter | Sel Sup ????
    
    '''
    RULE_TEMPLATES = {
        # SQL
        'Statement': ['Find out {0}', 'Show {0}'],
        # Statement
        'intersect Root Root': ['the common part of the set of {0} and the set of {1}', 'the common part of {0} and {1}'],
        'union Root Root': ['everyone in the set of {0} or the set of {1}', 'each one in either {0} or {1}'],
        'except Root Root': ['everyone in the set of {0} but not in the set of {1}', 'each one in {0} but not in {1}'],
        'Root': '{0}',
        # Root
        'Select Filter Order': '{0}, {1}, {2}',
        'Select Filter': '{0}, {1}',
        'Select Order': '{0}, {1}',
        'Select': '{0}',
        'Select Sup Filter': '{0}, {1}, {2}', # !!!!!!!!!!!!!!!!!!!
        'Select Sup': '{0}, {1}', # !!!!!!!!!!!!!!!!!!!
        # Select
        'N': '{0}', # !!!!!!!!!!!

        'A': '{0}',
        'A A': '{0} and {1}',
        'A A A': '{0} , {1} and {2}',
        'A A A A': '{0} , {1} , {2} and {3}',
        'A A A A A': '{0} , {1} , {2} , {3} and {4}',
        'A A A A A A': '{0} , {1} , {2} , {3} , {4} and {5}',
        # A
        'none C T': ['the {0} of {1}', 'the {1} \'s {0}'],
        'max C T': ['the maximum {0} of {1}', 'the largest {0} of {1}', 'the biggest {0} of {1}', 'the maximum {1} \'s {0}'],
        'min C T': ['the minimum {0} of {1}', 'the smallest {0} of {1}', 'the minimum {1} \'s {0}'],
        'count C T': ['the number of {0} of {1}', 'the number of {1} \'s {0}'],
        'sum C T': ['the sum of {0} of {1}', 'the summation of {1} \'s {0}'],
        'avg C T': ['the average {0} of {1}', 'the mean value of {1} \'s {0}', 'the average of {1} \'s {0}'],
        # Filter
        'and Filter Filter': ['{0} and {1}', '{0} and {1}'], #!!!!!!!!!!!!!!!!!!!!
        'or Filter Filter': ['{0} or {1}', '{1} or {0}'], #!!!!!!!!!!!!!!!!!!
        '= A': ['where {0} equals to {1}'.format('{0}', VALUE_TYPE), 'where {0} is {1}'.format('{0}', VALUE_TYPE)],
        '> A': 'where {0} greater than {1}'.format('{0}', VALUE_TYPE),
        '< A': 'where {0} less than {1}'.format('{0}', VALUE_TYPE),
        '>= A': ['where {0} greater than or equals to {1}'.format('{0}', VALUE_TYPE), 'where {0} no less than or equals to {1}'.format('{0}', VALUE_TYPE)],
        '<= A': ['where {0} less than or equals to {1}'.format('{0}', VALUE_TYPE), 'where {0} no greater than or equals to {1}'.format('{0}', VALUE_TYPE)],
        '!= A': ['where {0} not equals to {1}'.format('{0}', VALUE_TYPE), 'where {0} is not to {1}'.format('{0}', VALUE_TYPE)],
        'between A': 'where {0} between {1} and {2}'.format('{0}', VALUE_TYPE, VALUE_TYPE),
        'like A': 'where {0} like {1}'.format('{0}', VALUE_TYPE),
        'not_like A': 'where {0} not like {1}'.format('{0}', VALUE_TYPE),
        '= A Root': ['where {0} equals to {1}', 'where {0} is {1}'],
        '> A Root': 'where {0} greater than {1}',
        '< A Root': 'where {0} less than {1}',
        '>= A Root': 'where {0} greater than or equals to {1}',
        '<= A Root': 'where {0} less than or equals to {1}',
        '!= A Root': ['where {0} not equals to {1}', 'where {0} is not to {1}'],
        'between A Root': 'where {0} is between {1}',  # todo: useless
        'in A Root': 'where {0} is in the set of {1}',
        'not_in A Root': 'where {0} is not in the set of {1}',
        # Order
        'asc A': 'in ascending order of {0}',
        'des A': 'in descending order of {0}',
        'asc A limit': 'in ascending order of {0}' + 'with maximum {0} item(s)'.format(VALUE_TYPE),
        'des A limit': 'in descending order of {0}' + 'with maximum {0} item(s)'.format(VALUE_TYPE),
    }
    RULE_TEMPLATES_WITHOUT_TABLE = copy.copy(RULE_TEMPLATES)
    RULE_TEMPLATES_WITHOUT_TABLE.update({
        'none C T': 'the {0}',
        'max C T': 'the maximum {0}',
        'min C T': 'the minimum {0}',
        'count C T': 'the number of {0}',
        'sum C T': 'the sum of {0}',
        'avg C T': 'the average {0}',
    })

    def __init__(self, node_id: int,
                 text: str,
                 statement: str,
                 children_tokens: List[str],
                 father=None,
                 depth=0):
        self.node_id = node_id
        self.text = text
        self.statement = statement.split(' -> ')[1].strip()  # align with irnet.context.grammar
        if text in Node.TYPE_DICT:
            self.type = Node.TYPE_DICT.get(text)
        elif text in Node.KEYWORD_LIST:
            self.type = Node.KEYWORD_TYPE
        else:
            raise Exception('Node type error')
        self._children_tokens = children_tokens
        self.children = []
        self.father = father
        self.depth = depth
        # father_text = 'None' if father is None else father.text
        # print(f'Created node: text={text}, children_tokens={children_tokens}, father={father_text}')
        self.checked: bool = True
        self.more_info = {}  # data container for outside operations

    def bfs(self, process_f=lambda x: x, node_only=True):
        ret_list = []
        queue = [self]
        while queue:
            node = queue[0]
            del queue[0]
            if isinstance(node, Node):
                ret_list.append(process_f(node))
            elif isinstance(node, str) and not node_only:
                ret_list.append(process_f(node))
            if isinstance(node, Node) and node.children:
                queue += node.children
        return ret_list

    def restatement(self, with_table=True):
        # 1. Find if Root node exists in subtree, if unchecked leaved, raise error  # todo: may be eliminated
        subtree_nodes = self.bfs()
        if False in [node.checked for node in subtree_nodes if not isinstance(node, str) and node.type == Node.ROOT_TYPE]:
            raise Exception('Unchecked Root node exists, check it first')

        # 2. Restate each child
        return self._restate_node(self, with_table=with_table)

    def restatement_with_tag(self):
        # 1. Find if Root node exists in subtree, if unchecked leaved, raise error  # todo: may be eliminated
        subtree_nodes = self.bfs()
        if False in [node.checked for node in subtree_nodes if
                     not isinstance(node, str) and node.type == Node.ROOT_TYPE]:
            raise Exception('Unchecked Root node exists, check it first')

        # 2. Restate each child
        return self._restate_node_with_tag(self)

    @staticmethod
    def _restate_node(node, with_table=True):
        if isinstance(node, str) and node not in Node.KEYWORD_LIST:
            raise Exception('Node should be str or keyword')
        node_statement = node.statement
        templates = Node.RULE_TEMPLATES if with_table else Node.RULE_TEMPLATES_WITHOUT_TABLE
        if node_statement in templates:
            rule_template = random_select(templates.get(node_statement))
            format_strings = []
            for child in node.children:
                if isinstance(child, str) and child in Node.KEYWORD_LIST:
                    continue
                format_strings.append(Node._restate_node(child, with_table=with_table))
            return rule_template.format(*format_strings)
        else:
            return ' '.join(node_statement.split('_')) if node_statement is not '*' else 'items'  # select *

    @staticmethod
    def _restate_node_with_tag(node, with_table=True):
        if isinstance(node, str) and node not in Node.KEYWORD_LIST:
            raise Exception('WA!!!')
        node_statement = node.statement
        templates = Node.RULE_TEMPLATES if with_table else Node.RULE_TEMPLATES_WITHOUT_TABLE
        if node_statement in templates:
            rule_template = templates.get(node_statement)
            if isinstance(rule_template, List):
                rule_template = random.sample(rule_template, 1)[0]
            sub_strings = []
            sub_string_tags = []
            for child in node.children:
                if isinstance(child, str) and child in Node.KEYWORD_LIST:
                    continue
                node_restatement_string, node_restatement_tag = Node._restate_node_with_tag(child)
                sub_strings.append(node_restatement_string)
                sub_string_tags.append(node_restatement_tag)
            restatement_string = rule_template.format(*sub_strings)
            restatement_tag = []
            nonterminal_children = [_ for _ in node.children if isinstance(_, Node)]
            for word in rule_template.split():
                if word.startswith('{') and word.endswith('}'):
                    placeholder_idx = int(word[1:-1])
                    if sub_string_tags[placeholder_idx] is not None:
                        restatement_tag += sub_string_tags[placeholder_idx]
                    else:
                        restatement_tag += nonterminal_children[placeholder_idx].text * len(sub_strings[placeholder_idx].split())
                else:
                    restatement_tag.append(node.text)
            return restatement_string, restatement_tag
        else:
            return ' '.join(node_statement.split('_')) if node_statement is not '*' else 'items', None#[node_statement]
        # todo: tag of table and column with split char

    @staticmethod
    def print_subtree(node):
        def _print_subtree(node):
            print('   ' * node.depth + node.text)
            for child in node.children:
                if isinstance(child, Node):
                    _print_subtree(child)
                else:
                    print('   ' * (node.depth + 1) + child)

        _print_subtree(node)

    def clear_more_info_recursively(self, keys=None):
        if keys is None:
            def clear_more_info(node):
                node.more_info.clear()
        else:
            def clear_more_info(node):
                for key in keys:
                    if key in node.more_info:
                        del node.more_info[key]

        self.bfs(process_f=clear_more_info)

    def compare_node(self, node) -> bool:
        if self.type == node.type and self.children == node.children:
            return True
        else:
            return False

    def compare_tree(self, node) -> bool:
        if self.type != node.type or self.statement != node.statement:
            self.more_info['subtree_equal'] = node.more_info['subtree_equal'] = False
            self.bfs(lambda x: x.more_info.update({'subtree_equal': False}))
            node.bfs(lambda x: x.more_info.update({'subtree_equal': False}))
            return False
        else:
            assert len(self.children) == len(node.children)
            status = True
            for child1, child2 in zip(self.children, node.children):
                if isinstance(child1, str) or isinstance(child2, str):
                    if child1 != child2:
                        status = False
                elif child1.compare_tree(child2) is False:
                    status = False
            self.more_info['subtree_equal'] = node.more_info['subtree_equal'] = status
            self.bfs(lambda x: x.more_info.update({'subtree_equal': status}))
            node.bfs(lambda x: x.more_info.update({'subtree_equal': status}))
            return status

    @staticmethod
    def from_statements(statements):
        root, _ = parse_sql_tree(statements)
        return root

    def get_action(self):
        state_map = ['intersect Root Root', 'union Root Root',
                     'except Root Root', 'Root']
        root_map = ['Select Sup Filter', 'Select Filter Order',
                    'Select Sup', 'Select Filter',
                    'Select Order', 'Select']
        filter_map = ['and Filter Filter', 'or Filter Filter',
                      '= A', '!= A', '< A', '> A', '<= A', '>= A',
                     'between A', 'like A', 'not_like A',
                      '= A Root', '< A Root', '> A Root', '!= A Root',
                      'between A Root', '>= A Root', '<= A Root',
                      'in A Root', 'not_in A Root']
        sup_map = order_map = ['des A', 'asc A']
        a_map = ['none C T', 'max C T', 'min C T', 'count C T',
                 'sum C T', 'avg C T']
        #if self.text == 'Statement':
        #    print([c.text if isinstance(c, Node) else c for c in self.children])
        childern_text = ' '.join([c.text if isinstance(c, Node) else c for c in self.children])
        if self.text == 'SQL':
            act = []
        elif self.text == 'Statement':
            act = [f'Root1({state_map.index(childern_text)})']
        elif self.text == 'Root':
            act = [f'Root({root_map.index(childern_text)})']
        elif self.text == 'N':
            act = [f'N({len(self.children) - 1})']
        elif self.text == 'Select':
            assert len(self.children) == 1 and self.children[0].text == 'N'
            act = [f'Sel(0)']
        elif self.text == 'Filter':
            act = [f'Filter({filter_map.index(childern_text)})']
        elif self.text == 'Sup':
            act = [f'Sup({sup_map.index(childern_text)})']
        elif self.text == 'Order':
            act = [f'Order({order_map.index(childern_text)})']
        elif self.text == 'A':
            act = [f'A({a_map.index(childern_text)})']
        else:
            #print(self.text)
            assert self.text == 'C' or self.text == 'T'
            if self.text == 'C':
                act = [f'Column {"_".join([c for c in self.children])}']
                #print([c for c in self.children], len(self.children))
                #print(act)
            else:
                act = [f'Table {"_".join([c for c in self.children])}']
                #print([c for c in self.children], len(self.children))
                #print(act)

        for child in self.children:
            if isinstance(child, Node):
                act += child.get_action()
        return act
def is_nonterminal(token):
    letter = token[0]
    if ord('A') <= ord(letter) <= ord('Z'):
        return True
    else:
        return False


def parse_sql_tree(tree_statements):
    #parse出一个tree。其中Node的children是由node和terminal组成的list。
    # print(tree_statements)
    max_depth = -1
    depth = 0
    stack = []
    root = Node(0, 'SQL', 'SQL -> Statement', ['Statement'], depth=0)
    stack.append(root)
    for state_id, statement in enumerate(tree_statements):
        assert statement.split(' -> ')[0] == stack[-1]._children_tokens[0]  # non-terminal match
        # print(f'statement = {statement}')
        nonterminal, children = statement.split('->')
        nonterminal = nonterminal.strip()
        children = [child.strip() for child in children.strip().split(' ')]
        node = Node(state_id, nonterminal, statement, children, father=stack[-1], depth=depth)
        stack[-1].children.append(node)
        del stack[-1]._children_tokens[0]
        stack.append(node)
        depth += 1
        max_depth = max(max_depth, depth)
        while stack:
            # move terminal tokens from children_tokens into children
            while stack[-1]._children_tokens and not is_nonterminal(stack[-1]._children_tokens[0]):
                stack[-1].children.append(stack[-1]._children_tokens[0])
                del stack[-1]._children_tokens[0]
            # layer up if no child waiting for process
            if len(stack[-1]._children_tokens) == 0:
                stack.pop()
                depth -= 1
                if len(stack) == 0:
                    return root, max_depth
            else:
                break
    return root, max_depth




from copy import deepcopy
import re
def refactor(node, mode):
    #print(node.text)
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
        for child in child_list[0]:
            ret += [[child] + c for c in tmp]
        return ret

    tmp = dfs(child_list)
    for child in tmp:
        new_node = deepcopy(node)
        new_node.children = deepcopy(child)
        sql_tree_list.append(new_node)

    if 'Filter' in mode and \
            (node.statement == 'and Filter Filter' or node.statement == 'or Filter Filter'):
        assert len(node.children) == 3 and (node.children[0] == 'and' or node.children[0] == 'or')
        assert len(child_list[0]) == 1 and (child_list[0][0] == 'and' or child_list[0][0] == 'or')
        for child1 in child_list[1]:
            for child2 in child_list[2]:
                new_node = deepcopy(node)
                new_node.children = deepcopy([child_list[0][0], child2, child1])
                sql_tree_list.append(new_node)

    if 'Intersect' in mode and node.statement == 'intersect Root Root':
        assert len(node.children) == 3 and node.children[0] == 'intersect'
        assert len(child_list[0]) == 1 and child_list[0][0] == 'intersect'
        for child1 in child_list[1]:
            for child2 in child_list[2]:
                new_node = deepcopy(node)
                new_node.children = deepcopy(['intersect', child2, child1])
                sql_tree_list.append(new_node)

    if 'Select' in mode and re.match('A( A)*', node.statement) != None:
        assert all([len(c) == 1 for c in child_list])
        for i in range(1, len(child_list)):
            new_node = deepcopy(node)
            new_node.children = deepcopy([c[0] for c in child_list[i:] + child_list[:i]])
            sql_tree_list.append(new_node)

    return sql_tree_list


def mutate_select(sql):
    state = sql.children[0]
    if len(state.children) > 1:
        return False
    root = state.children[0]
    sel = root.children[0]
    n = sel.children[0]
    if len(n.children) == 1:
        return False
    return True
    # schema link


def sem2nl(sql_tree, data):

    root, max_depth = parse_sql_tree(sql_tree)
    #sql_tree = [root]
    sql_tree = refactor(root, ['Filter', 'Select', 'Intersect'])

    restatement = [root.restatement_with_tag()[0] for root in sql_tree]
    #exit(0)
    def get_id(l):
        for i, s in enumerate(l):
            if s.startswith('Column'):
                column_name = s.split()[1].replace('_', ' ')
                s = f'C({data["col_set"].index(column_name)})'
            elif s.startswith('Table'):
                table_name = s.split()[1].replace('_', ' ')
                s = f'T({data["table_names"].index(table_name)})'
            l[i] = s
        return l

    rule_action = [get_id(root.get_action()) for root in sql_tree]

    return restatement, rule_action
    #print(restatement[0])


if __name__ == '__main__':
    from src.rule.semQL import *
    # sql_tree = ['Statement -> Root', 'Root -> Select Filter',
    #             'Select -> A', 'A -> count C T', 'C -> budget_in_billions', 'T -> department',
    #             'Filter -> > A', 'A -> none C T', 'C -> age', 'T -> head']
    sql_tree = ['Statement -> Root', 'Root -> Select Filter',
                    'Select -> A', 'A -> sum C T', 'C -> enr', 'T -> college',
                    'Filter -> not_in A Root', 'A -> none C T', 'C -> cname', 'T -> college',
                        'Root -> Select Filter',
                            'Select -> A', 'A -> none C T', 'C -> cname', 'T -> tryout',
                            'Filter -> = A', 'A -> none C T', 'C -> ppos', 'T -> tryout']




    import json
    nt_map = {
        'Root1': 'Statement', 'Root': 'Root', 'Sel': 'Select', 'N': 'N', 'A': 'A',
        'C': 'C', 'T': 'T', 'Filter': 'Filter', 'Sup': 'Sup', 'Order': 'Order',
    }
    reversed_map = {v: k for k, v in nt_map.items()}
    #with open('./data/train_spider.json') as f:
    #    data = json.load(f)
    with open('./data/dev.json') as f:
        data = json.load(f)
    with open('./data/tables.json') as f:
        table = json.load(f)
    table = {t['db_id']: t for t in table}
    total = 0
    new_data = []
    for i, d in enumerate(data):
        print(i)
        if 'JOIN' in d['query']:continue
        #total += 1
        #print(i, total)
        #continue
        rules = d['rule_label']
        question = d['question']
        db_id = d['db_id']
        db = table[db_id]
        #print(rules)
        actions = []
        flag = False
        for rule in rules.split():
            nt = rule.split('(')[0]
            try:
                obj = eval(rule)
            except:
                #print(rules)
                flag = True
                break
            prod = obj.production
            prod = [nt_map[p] if p in nt_map.keys() else p for p in prod.split()[1:]]
            prod = f'{nt_map[nt]} -> {" ".join(prod)}'
            if nt == 'A':
                prod += ' T'
            elif nt == 'C':
                prod = f'{nt} -> {d["col_set"][obj.id_c]}'
            elif nt == 'T':
                prod = f'{nt} -> {d["table_names"][obj.id_c]}'
            actions.append(prod)
        if flag:
            continue
        #print(rules)
        #print(d['col_set'])
        #print(d['table_names'])
        #print(d['query'], d['question'])
        #if sem2nl(actions, d):
        #    print(d['question'], d['query'])
        #    total += 1
        tmp = sem2nl(actions, d)
        d['mutate'] = (tmp[0], [' '.join(t) for t in tmp[1]])
        #print( d['mutate'][1])
        new_data.append(d)
        #exit(0)
        '''
        r1 = rules
        r2 = ' '.join(sem2nl(actions, d)[1][0])
        if r1 != r2:
            print(i)
            print(r1, r2)
            exit(0)
        '''
    with open('generate_data.json', 'w') as f:
        import json
        json.dump(new_data, f)
    #print(total)

    exit(0)
    data = list(filter(lambda x: 'generate' in x.keys(), data))
    import pickle
    with open('generate_data.pkl', 'wb') as f:
        pickle.dump(data, f)
    print(total, len(data))



# total:4731   Filter: 404    Select: 1253   Intersect: 103     1702