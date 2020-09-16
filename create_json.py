import json
import os

def create_json_list(png_file_dir, json_save_path):
    path_dict = {}
    for _,_,files in os.walk(png_file_dir):
        for png_file in files:
            if '.png' in png_file:
                path_dict[os.path.join("negative_back", png_file)] = 'negative'

    with open(json_save_path, 'w') as json_file:
        json.dump(path_dict, json_file)

create_json_list("/Users/jxiang/Desktop/negative_back", "/Users/jxiang/Desktop/negative_back.json")