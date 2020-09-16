from flask import Flask, send_file, render_template, request
from PIL import Image
import flask
import numpy as np
import os
import json
from collections import defaultdict
import random
import io
from shutil import copyfileobj
from string import ascii_uppercase
from tempfile import NamedTemporaryFile

app = Flask(__name__)

NUM_CLASSES = 2
NUM_IMAGES = 5
NUM_CHANNELS = 5

METADATA_DIR = '/data/rsg/mammogram/CellPainter'
metadata_file = "images_for_puma_and_morpho_assay_metadata_aug18_2020.json"
full_dataset_dir = '/Users/jxiang/Desktop'

positive_back_dir = '/Users/jxiang/Desktop/positive_back'
negative_back_dir = '/Users/jxiang/Desktop/negative_back'

positive_metadata = json.load(open("/Users/jxiang/Desktop/positive_back.json"))
negative_metadata = json.load(open("/Users/jxiang/Desktop/negative_back.json"))

# metadata = json.load(open(os.path.join(METADATA_DIR, metadata_file)))

def get_random_positive_image_paths(k=3):
    image_paths = [i for i in positive_metadata.keys()]
    chosen_paths = np.random.choice(image_paths, size = min(k, len(image_paths)), replace=False)

    return chosen_paths

def get_random_negative_image_paths(k=3):
    image_paths = [i for i in negative_metadata.keys()]
    chosen_paths = np.random.choice(image_paths, size = min(k, len(image_paths)), replace=False)

    return chosen_paths

# def get_random_image_basenames(smile, k=3):
#     images = metadata[smile]['images']
#     plate2images = defaultdict(list)
#     for x in images:
#         plate2images[x['plate_id']].append(os.path.basename(x['path']))

#     plates = plate2images.keys()
#     chosen_plates = np.random.choice(list(plates), size=min(k, len(plates)), replace=False)

#     return [np.random.choice(plate2images[p], size=1)[0] for p in chosen_plates]

@app.route('/')
def main():
    mols = []

    pos_image_paths = get_random_positive_image_paths(NUM_IMAGES + 1)
    neg_image_paths = get_random_negative_image_paths(NUM_IMAGES + 1)

    for i in range(NUM_CLASSES):
        if i == 0:
            mols.append({
                'image_paths': pos_image_paths[:-1],
                'label': "positive",
                'test_image': pos_image_paths[-1]
            })
        else:
            mols.append({
                'image_paths': neg_image_paths[:-1],
                'label': "negative",
                'test_image': neg_image_paths[-1]
            })

    test_index = random.choices(range(NUM_CLASSES))[0]

    last = request.args.get('last', 'NA')

    print("MOLS: ", mols)

    return render_template("main.html", mols=mols, test_index=test_index, num_channels=NUM_CHANNELS, last=last)

@app.route('/image/<path:path>')
def image(path):

    img_io = io.BytesIO()
    image_path = os.path.join(full_dataset_dir, path)

    img = Image.open(image_path)
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/PNG')

