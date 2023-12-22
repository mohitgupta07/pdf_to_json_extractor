import json
import os.path
import re
import auto_pdf_try
import extract_txt_with_styling_info_from_pdf
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
def get_data_from_csv(file_list, root_dir="resources/ExtractTextInfoWithStylingInfoFromPDF3"):
    '''
    util for getting data from csv. Note that we will club single csv and the final output would be list of csvs data
    comma seprated.
    :param file_list:
    :return:
    '''
    data_list = []
    for file_path in file_list:
        if str(file_path).__contains__("csv"):
            try:
                with open(os.path.join(root_dir, file_path), 'r') as file:
                    csv_string = file.read()
                    data_list.append(csv_string)
            except:
                print("skipping. couldn't read csv.")
    return data_list if len(data_list) > 1 else data_list[0]


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
            #todo: change csv to data.
            text_data = get_data_from_csv(element.get("filePaths"))
            final_dict.append({"path": path, "text": text_data})
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
    part4_data = revised_parse_to_nested_json_fixed(part2_data, hierarchy_dict)
    return part4_data


def part2(elements):
    '''
    this portion clubs the unneccesary tags to one.
    :param elements:
    :return:
    '''
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
    '''
    cleansing part. reverse hierarchy.
    :param elements:
    :return:  hieracrhy provider with updated data.
    '''
    # find first H tag.
    # for element in elements:
    #     if not element['path'].__contains__("H"):
    #         elements = elements[1:]
    #     else:
    #         break
    # first ---
    for i in range(len(elements) - 1):
        element = elements[i]
        if element['path'].__contains__("H"):
            stop_ind = i + 1
            for cj in range(i + 1, len(elements)):
                next_element = elements[cj]
                if next_element['path'] == element['path']:
                    continue
                stop_ind = cj
                break
            for cj in range(i, stop_ind):
                updated_element = elements[cj]
                # str_val = updated_element['path'].("")
                regex = r"\/?H(\d+)"
                # Reapplying the regex to each test string
                match = re.search(regex, updated_element['path'])
                str_val = match.group(1) if match else ''
                if str_val != '':
                    val = int(str_val)
                    val = val - (stop_ind - (i + 1))
                    new_path = "/H" + str(val)
                    element['path'] = new_path

    # second ---
    unique_types = set()
    for element in elements:
        if element['path'].__contains__("H"):
            unique_types.add(element['path'])
    return dict(zip(sorted(unique_types), range(1, len(unique_types)+ 1)))


def compute_code(file_path='resources/ExtractTextInfoWithStylingInfoFromPDF3/structuredData.json', output_json_path="output_file.json"):
    with open(file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
        elements = json_data.get('elements', [])
        nested_json_structure = main_code(elements)

        nested_json_output = json.dumps(nested_json_structure, indent=2)
        # Write the dictionary to a file
        with open(output_json_path, 'w') as json_file:
            json.dump(nested_json_structure, json_file, indent=2)
        return nested_json_output

'''
1- first use auto_pdf_try.py and add more required tags in your current pdf.
2- then use extract_pdf api.
3- run compute_code here.
https://developer.adobe.com/document-services/docs/overview/pdf-extract-api/howtos/extract-api/
'''


compute_code()


def automated_run():
    #todo: add hyper-params.
    auto_pdf_try.run_autotag()
    extract_txt_with_styling_info_from_pdf.run_extract_pdf()
    compute_code()