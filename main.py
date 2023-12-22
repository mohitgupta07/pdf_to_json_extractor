import json

class EnhancedNestedNode:
    def __init__(self, title, data=None):
        self.title = title
        self.children = []
        self.data = data

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

# Modified function with added check to prevent IndexError
def enhanced_parse_to_nested_json(elements):
    root = EnhancedNestedNode("Document")
    node_stack = [root]
    hierarchy = {'Figure': 0, 'H1': 1, 'H2': 2, 'H3': 3, 'H4': 4, 'H5': 5, 'H6': 6, 'Table': 7,  'TR': 8, 'TD': 9}

    for element in elements:
        path = element.get('Path', "")
        text = element.get("Text", None)
        current_level = -1

        for tag, level in hierarchy.items():
            if f'/{tag}' in path:
                current_level = level
                break

        if current_level > -1:
            # Adjust the stack based on the current level
            while len(node_stack) > current_level:
                node_stack.pop()
            new_node = EnhancedNestedNode(text)
            if node_stack:  # Check if there is still an element in the stack
                node_stack[-1].add_child(new_node)
                node_stack.append(new_node)
        elif node_stack and text:  # Ensure there's at least one node in the stack
            if node_stack[-1].data:
                node_stack[-1].data += " " + text
            else:
                node_stack[-1].data = text

    return root.to_dict()

# Function to read JSON file and extract the elements for parsing
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data.get('elements', [])


# Read the file and parse to nested JSON structure


# # Convert the nested structure to JSON format and print
# enhanced_nested_json_output = json.dumps(enhanced_nested_json_structure, indent=2)
# print(enhanced_nested_json_output)

def compute_code(file_path='/Users/hit/Downloads/adobeStructuredData.json'):
    with open(file_path, 'r') as file:
        text_elements = read_json_file(file_path)
        enhanced_nested_json_structure = enhanced_parse_to_nested_json(text_elements)

        # nested_json_output = json.dumps(correctly_nested_json_structure, indent=2)
        return enhanced_nested_json_structure

compute_code()