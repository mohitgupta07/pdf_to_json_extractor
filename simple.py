import json
from main2 import revised_parse_to_nested_json_fixed

'''
stack = [root]
class node:
    title
    child -> node.
    path

hierarchy = {'H1': 1, 'H2': 2, 'H3': 3, 'H4': 4, 'H5': 5, 'H6': 6, 'TR': 7, 'TD': 8, 'L': 1, 'LI': 2}

H1. 
root -> title , child -> [new_node_h1]

new_node.
stack = [root, new_node_h1]

H2 
new_node.
stack = [root, new_node_h1, new_node_h2]

H3
new_node.
stack = [root, new_node_h1, new_node_h2, new_node_h3]

H2
new_node
stack.pop(new_node_h3)
stack.pop(new_node_h2)
stack = [root, new_node_h1]
add h2
stack = [root, new_node_h1, new_node_h2]

table

'''


import re
def main_code(elements):
    root = []
    current = []
    stack = None
    output = []
    final_dict = []
    for element in elements:
        path = element.get('Path', "")
        text = element.get("Text", "")
        kids = element.get("Kids", None)
        substring_to_remove = "//Document"
        # Removing the substring
        path = path.replace(substring_to_remove, "")
        pattern = r'\[\d+\]'

        # Removing the pattern from the string
        path = re.sub(pattern, "", path)

        tags_to_ignore = ('Table/', 'Figure')

        flag = True
        for tag in tags_to_ignore:
            if f'{tag}' in path:
                flag = False
                break

        # if flag true then use stack.
        if flag:
            matching_path = False
            if stack is None:
                stack = [path]
            else:
                if path.__eq__(stack[-1]):
                    matching_path = True


        if flag and path.__contains__("Table"):
            # print(path, element.get("filePaths"))
            final_dict.append({"path":path, "text":element.get("filePaths")})
        elif flag and kids is None:
            # print(path, text)# bounds, text)
            final_dict.append({"path": path, "text": text})
        elif flag and kids:
            kid_txt = ""
            for kid in kids:
                kid_txt += " " + kid.get("Text", "")
            # print(path, kid_txt)
            final_dict.append({"path": path, "text": kid_txt})
    part2_data = part2(final_dict)
    hierarchy_dict = part3(part2_data)
    part4_data = revised_parse_to_nested_json_fixed(part2_data[1:], hierarchy_dict)
    return root


def part2(elements):
    data = []
    type_set = ["L", "P", "Aside", "TOC"]
    ls_size = len(elements)
    i = 0
    while i < ls_size:
        element = elements[i]
        is_type_found = False
        for selected_type in type_set:
            if element['path'].__contains__(selected_type):
                is_type_found = True
                # print(element['path'], element['text'])
                club_txt = element['text']
                child_j = i + 1
                while True:
                    if child_j >= len(elements):
                        break
                    celement = elements[child_j]
                    if celement['path'].__contains__(selected_type):
                        club_txt = club_txt + " " + celement['text']
                        child_j += 1
                    else:
                        break
                i = child_j
                ans = {"path": selected_type, "text": club_txt}
                data.append(ans)
                # print(f'{ans["path"]}', ans['text'])
                break
        if is_type_found:
            continue
        #main condn
        i += 1
        data.append(element)
        # print(element['path'], element['text'])
    return data

def part3(elements):
    unique_types = set()
    for element in elements:
        if element['path'].__contains__("H"):
            unique_types.add(element['path'])
    return dict(zip(sorted(unique_types), range(1, len(unique_types)+ 1)))

def part4(elements):
    order = {'H': 0, 'H1': 1, 'H2': 2, 'H3': 3, 'H4': 4, 'H5': 5, 'H6': 6}
    root = []
    node_stack = [root]
    for element in elements:
        path = element.get('Path', "")
        text = element.get("Text")
        current_level = -1


def compute_code(file_path='structuredData_filepath.json'):
    with open(file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
        elements = json_data.get('elements', [])
        nested_json_structure = main_code(elements)

        # nested_json_output = json.dumps(correctly_nested_json_structure, indent=2)
        return nested_json_structure

compute_code()
