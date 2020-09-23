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

NUM_REFERENCES = 5

full_dataset_dir = '/data/rsg/mammogram/covid_data'

positive_back_dir = '/data/rsg/mammogram/covid_data/positive_back'
negative_back_dir = '/data/rsg/mammogram/covid_data/negative_back'

positive_metadata = json.load(open("/data/rsg/mammogram/covid_data/positive_back.json"))
negative_metadata = json.load(open("/data/rsg/mammogram/covid_data/negative_back.json"))

shuffled_positive_metadata_list = list(positive_metadata.keys())

shuffled_negative_metadata_list = list(negative_metadata.keys())

shuffled_metadata_list = shuffled_positive_metadata_list + shuffled_negative_metadata_list

random.shuffle(shuffled_metadata_list)

index = 0


positive_reference = np.random.choice([i for i in positive_metadata.keys()], size=NUM_REFERENCES, replace=False)
for path in positive_reference:
    del positive_metadata[path]

negative_reference = np.random.choice([i for i in negative_metadata.keys()], size=NUM_REFERENCES, replace=False)
for path in negative_reference:
    del negative_metadata[path]


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

    global index

    print(index)

    test_image = shuffled_metadata_list[index]

    label = 'positive' if test_image in positive_metadata else 'negative'
    if label == 'positive':
        mols.append({
            'image_paths': positive_reference,
            'label': "positive",
            'test_image': test_image
        })
        mols.append({
            'image_paths': negative_reference,
            'label': "positive",
            'test_image': negative_reference[0]
        })
        test_index = 0
    else:
        mols.append({
            'image_paths': positive_reference,
            'label': "positive",
            'test_image': positive_reference[0]
        })
        mols.append({
            'image_paths': negative_reference,
            'label': "negative",
            'test_image': test_image
        })
        test_index = 1

    last = request.args.get('last', 'NA')

    index += 1

    return render_template("main.html", mols=mols, test_index=test_index, num_channels=NUM_CHANNELS, last=last)

@app.route('/image/<path:path>')
def image(path):

    img_io = io.BytesIO()
    image_path = os.path.join(full_dataset_dir, path)

    img = Image.open(image_path)
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/PNG')

