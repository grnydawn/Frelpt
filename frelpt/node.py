# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

class ConcreteSyntaxNode(object):

    wrap_map = {}

    def __init__(self, parent, nodetypes, wrapped):
        self.parent = parent
        self.nodetypes = nodetypes
        self.wrapped = wrapped

        if isinstance(wrapped, (tuple, list)):
            self.wrap_map[id(wrapped)] = self
        elif self.wrapped is not None:
            self.wrapped.pair = self

        self.subnodes = []
        #self.ids = {} # namespace {id: [defined obj, [declared objs], intent]}
        self.lines = None # origina source code

    #def __getattr__(self, attr):
    #    return getattr(self.wrapped, attr)

    def topnode(self):
        top = self
        while hasattr(top,"parent") and top.parent:
            top = top.parent
        return top

    def __str__(self):
        return str(self.wrapped)

    def __repr__(self):
        return repr(self.wrapped)

    def showcode(self):
        lines = []
        lines.append(str(self))
        lines.extend([str(n) for n in self.subnodes])

        return "\n".join(lines)

    def showtree(self, depth=0):
        lines = []
        lines.append("    "*depth + repr(self))
        lines.extend([n.showtree(depth=depth+1) for n in self.subnodes
                      if hasattr(n, "showtree")])

        return "\n".join(lines)

    def traverse(self, bag, node=None, func=None, prerun=True, depth=0):

        if node is None and depth==0:
            node = self

        if prerun and callable(func):
            if func(node, bag, depth): return

        if not callable(func):
            if isinstance(bag, dict):
                if "__nodes__" in bag:
                    bagnodes = []
                    bag["__nodes__"] = bagnodes
                else:
                    bagnodes = bag["__nodes__"]
                bagnodes.append(node)
            elif isinstance(bag, list):
                bag.append(node)
            elif isinstance(bag, set):
                bag.add(node)

        if node and hasattr(node, "subnodes") and node.subnodes is not None:
            for child in node.subnodes:
                self.traverse(bag, node=child, func=func, prerun=prerun, depth=depth+1)

        if not prerun and callable(func):
            if func(node, bag, depth): return

class BlockNode(ConcreteSyntaxNode):

    def resolve(self):

        for subnode in self.subnodes:
                subnode.resolve()

class Tuple(BlockNode):

    def __getitem__(self, index):
        return self.subnodes[index]

nodeclass_template = '''\
class {clsname}({parentcls}):
    pass
'''

#    def collect_identifiers(self, ids):
#        self.resolver.search_{clsname}(self, ids)
#
#    def locate_declaration(self, name, node):
#        self.resolver.declare_{clsname}(self, name, node)
#
#    def locate_definition(self, name, node):
#        self.resolver.define_{clsname}(self, name, node)
#
#    def find_intent(self, name, node):
#        self.resolver.intent_{clsname}(self, name, node)
#

# node_classes : any
# node_types : all
def walk_ast(node, node_classes=None, node_types=None):

    if node_classes:
        if isinstance(node, node_classes):
            if node_types:
                if hasattr(node, "nodetypes"):
                    if all(t in node.nodetypes for t in node_types):
                        yield node
            else:
                yield node
    elif node_types:
        if hasattr(node, "nodetypes"):
            if all(t in node.nodetypes for t in node_types):
                yield node
    else:
        yield node

    if hasattr(node, "subnodes"):
        for subnode in node.subnodes:
            for _n in walk_ast(subnode, node_classes=node_classes, node_types=node_types):
                yield _n
