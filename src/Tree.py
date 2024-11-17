import json

class Node:
    def __init__(self, label, value=None, type=0, islist=False):
        # type 1：terminal node
        # type 0：non-terminal node 
        self.type = type
        self.islist = islist
        self.label = label
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def to_dict(self):
        node_dict = {
            "Type": "Terminal" if self.type == 1 else "Non-Terminal",
            "Label": self.label
        }
        if self.value is not None:
            node_dict["Value"] = self.value
        if self.children:
            node_dict["Children"] = [child.to_dict() for child in self.children]
        return node_dict

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.label) + ": " + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)