import random
import time
nodes = [
    {
        "id": "4",
        "type": "log",
        "data": {
            "value": 1
        },
        "position": {
            "x": 850,
            "y": 52
        },
        "measured": {
            "width": 160,
            "height": 80
        }
    },
    {
        "id": "5",
        "type": "onRun",
        "data": {
            "value": 1
        },
        "position": {
            "x": 251.3069647463456,
            "y": 202.5232602723795
        },
        "measured": {
            "width": 203,
            "height": 80
        },
        "selected": False,
        "dragging": False
    },
    {
        "id": "6",
        "type": "string",
        "data": {},
        "position": {
            "x": 468.68013757523636,
            "y": -86.21410146173687
        },
        "measured": {
            "width": 202,
            "height": 83
        },
        "selected": False,
        "dragging": False
    },
    {
        "id": "7",
        "type": "onRun",
        "data": {},
        "position": {
            "x": -247.81965862445003,
            "y": -1.5157165665103978
        },
        "measured": {
            "width": 203,
            "height": 80
        },
        "selected": False,
        "dragging": False
    },
    {
        "id": "8",
        "type": "log",
        "data": {},
        "position": {
            "x": 44,
            "y": -31
        },
        "measured": {
            "width": 160,
            "height": 80
        },
        "selected": False,
        "dragging": False
    },
    {
        "id": "9",
        "type": "number",
        "data": {
            "value": "1"
        },
        "position": {
            "x": -245.2964055732096,
            "y": -87.42739404057696
        },
        "measured": {
            "width": 202,
            "height": 74
        },
        "selected": False,
        "dragging": False
    }
]
edges = [
    {
        "id": "e5-4",
        "source": "5",
        "target": "4",
        "sourceHandle": "trigger1",
        "targetHandle": "trigger1",
        "type": "",
        "data": {
            "type": "number"
        }
    },
    {
        "source": "6",
        "sourceHandle": "source1",
        "target": "4",
        "targetHandle": "target1",
        "id": "xy-edge__6source1-4target1"
    },
    {
        "source": "7",
        "sourceHandle": "trigger1",
        "target": "8",
        "targetHandle": "trigger1",
        "id": "xy-edge__7trigger1-8trigger1"
    },
    {
        "source": "9",
        "sourceHandle": "source1",
        "target": "8",
        "targetHandle": "target1",
        "id": "xy-edge__9source1-8target1"
    }
]



"""
how to handle node parsing.

ok first we go through all nodes, look for on run nodes then look for edges that connect to them. 
then if the node is taking inputs we go back over that input node and check what node it is if its input we just pipe in the value and run the function. if its a function with more inputs we do the same thing until we reach a node that has no inputs.
then we run that node and return the value. if its a function we run the function with the inputs we have collected and return the value. if its a log node we just log the value.
when we reach the end we return to the node we started at

"""


# ---- Main Graph Class ----

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = {node["id"]: NodeFactory.create(node) for node in nodes}
        self.edges = edges
        self.edge_map = self.build_edge_map()

    def build_edge_map(self):
        # Map of target_id -> [incoming edges]
        edge_map = {}
        for edge in self.edges:
            edge_map.setdefault(edge["target"], []).append(edge)
        return edge_map

    def run(self):
        for node in self.nodes.values():
            if isinstance(node, OnRunNode):
                node.run(self)
                





# ---- Node Factory and Base Node Class ----


class NodeFactory:
    @staticmethod
    def create(raw_node):
        node_type = raw_node["type"]
        if node_type == "number":
            return NumberNode(raw_node)
        elif node_type == "math":
            return MathNode(raw_node)
        elif node_type == "log":
            return LogNode(raw_node)
        elif node_type == "onRun":
            return OnRunNode(raw_node)
        elif node_type == "string":
            return StringNode(raw_node)
        elif node_type == "joinText":
            return JoinTextNode(raw_node)
        elif node_type == "random":
            return RandomNode(raw_node)
        else:
            raise ValueError(f"Unknown node type: {node_type}")

class BaseNode:
    def __init__(self, raw_node):
        self.id = raw_node["id"]
        self.data = raw_node["data"]
        self.type = raw_node["type"]

    def evaluate(self, graph):
        
        if self.type == "onRun":
            return None
        raise NotImplementedError


# ---- Node types ----

class NumberNode(BaseNode):
    def evaluate(self, graph):
        return self.data["value"]
    
    
class StringNode(BaseNode):
    def evaluate(self, graph):
        return self.data.get("value", "")

class MathNode(BaseNode):
    def evaluate(self, graph):
        input_values = []
        for edge in graph.edge_map.get(self.id, []):
            source_node = graph.nodes[edge["source"]]
            input_values.append(source_node.evaluate(graph))
        op = self.data["op"]
        if op == "add":
            return sum(input_values)


class LogNode(BaseNode):
    def evaluate(self, graph):
        for edge in graph.edge_map.get(self.id, []):
            source_node = graph.nodes[edge["source"]]
            val = source_node.evaluate(graph)
            if val is not None:
                print(f"[LOG] {val}")
        return None

class OnRunNode(BaseNode):
    def run(self, graph):
        for edge in graph.edges:
            if edge["source"] == self.id:
                target_node = graph.nodes[edge["target"]]
                target_node.evaluate(graph)
                
class JoinTextNode(BaseNode):
    def evaluate(self, graph):
        input_values = []
        for edge in graph.edge_map.get(self.id, []):
            source_node = graph.nodes[edge["source"]]
            input_values.append(source_node.evaluate(graph))
        return "".join(input_values)
    
class RandomNode(BaseNode):
    def evaluate(self, graph):
        input_values = []
        for edge in graph.edge_map.get(self.id, []):
            source_node = graph.nodes[edge["source"]]
            input_values.append(source_node.evaluate(graph))
        return random.choice(input_values) if input_values else None




start_time = time.time()
print("Starting graph evaluation...")
if __name__ == "__main__":
    graph = Graph(nodes, edges)
    graph.run()

    print("Graph evaluation completed.")
    print(f"Execution time: {time.time() - start_time} ms")