import json


class EnhancedNestedNode:
    def __init__(self, title, data=None):
        self.title = title
        self.children = []
        self.data = [] if data is None else [data]

    def add_child(self, node):
        self.children.append(node)

    def to_dict(self):
        """ Convert the node and its children to a dictionary format suitable for JSON serialization. """
        node_dict = {
            'title': self.title,
            'data': self.data,
            'children': [child.to_dict() for child in self.children]
        }
        return node_dict


def revised_parse_to_nested_json_fixed(elements,
                                       hierarchy={'H1': 1, 'H2': 2, 'H3': 3, 'H4': 4, 'H5': 5, 'H6': 6}):
    root = EnhancedNestedNode("Document")
    node_stack = [root]
    #TODO: use part3 in simple.py to get the H types.
    index_count = -1
    for element in elements:
        index_count +=1
        path = element.get('path', "")
        text = element.get("text")
        current_level = 0

        # Identify if the element is a title, subtitle, or part of a table, and its level
        for tag, level in hierarchy.items():
            if f'{tag}' in path:
                current_level = level
                break

        if current_level > 0:
            # Adjust the stack based on the current level
            while len(node_stack) > current_level:
                node_stack.pop()
            while len(node_stack) < current_level:
                # Placeholder node for missing levels
                placeholder = EnhancedNestedNode(path)
                node_stack[-1].add_child(placeholder)
                node_stack.append(placeholder)

            new_node = EnhancedNestedNode(text)
            node_stack[-1].add_child(new_node)
            node_stack.append(new_node)
        elif node_stack and text is not None:  # Ensure there's at least one node in the stack and text is not None
            if node_stack[-1].data:
                if type(text) is list:
                    # not required to write this condn explicitly but for better readability.
                    node_stack[-1].data.append(text)
                else:
                    node_stack[-1].data.append(text)
            else:
                node_stack[-1].data = [text]

    return root.to_dict()





def compute_simple(file_path='/Users/hit/Downloads/adobeStructuredData.json'):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        elements = json_data.get('elements', [])
        nested_json_structure = revised_parse_to_nested_json_fixed(elements)

        # nested_json_output = json.dumps(correctly_nested_json_structure, indent=2)
        return nested_json_structure

# compute_simple()