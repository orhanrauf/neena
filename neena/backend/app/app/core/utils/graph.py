from app import schemas


class Graph:
    def __init__(self, num_vertices):
        self.graph = {i: [] for i in range(num_vertices)}
        self.num_vertices = num_vertices

    def add_edge(self, start_node, end_node):
        self.graph[start_node].append(end_node)
        
    def is_cyclic_util(self, node, visited, rec_stack):
        visited[node] = True
        rec_stack[node] = True

        # Visit all the neighbors
        for neighbor in self.graph[node]:
            if not visited[neighbor]:
                if self.is_cyclic_util(neighbor, visited, rec_stack):
                    return True
            elif rec_stack[neighbor]:  # If the node is in the recursion stack, then graph has a cycle
                return True

        # Node needs to be popped from recursion stack before function ends
        rec_stack[node] = False
        return False

    def is_cyclic(self):
        visited = [False] * self.num_vertices
        rec_stack = [False] * self.num_vertices
        for node in range(self.num_vertices):
            if not visited[node]:
                if self.is_cyclic_util(node, visited, rec_stack):
                    return True
        return False
    
    def topological_sort_util(self, node, visited, stack):
        visited[node] = True

        # Visit all the neighbors
        for neighbor in self.graph[node]:
            if not visited[neighbor]:
                self.topological_sort_util(neighbor, visited, stack)

        # Push current node to stack which stores the result
        stack.insert(0, node)

    def topological_sort(self):
        # Return None for a cyclic graph
        if self.is_cyclic():
            return None

        visited = [False] * self.num_vertices
        stack = []

        for node in range(self.num_vertices):
            if not visited[node]:
                self.topological_sort_util(node, visited, stack)

        return stack

def flow_to_graph(flow: schemas.FlowBase) -> Graph:
    num_vertices = len(flow.task_operations)
    graph = Graph(num_vertices)
    task_to_node = {task.name: i for i, task in enumerate(flow.task_operations)}
    node_to_task = {i: task for task, i in task_to_node.items()}

    for task in flow.task_operations:
        for arg in task.arguments:
            if arg.source == "@tasks()":
                source_task_name = arg.value.split('.')[0]
                graph.add_edge(task_to_node[source_task_name], task_to_node[task.name])

    return graph, node_to_task
