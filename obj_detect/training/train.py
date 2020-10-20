from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import label_map_util
from object_detection.utils import ops as utils_ops
import os
import pathlib
import subprocess
import numpy as np
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import shutil
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from IPython.display import display
import stat

from collections import defaultdict
from io import StringIO


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def download_model(model_name, model_date):
    base_url = 'http://download.tensorflow.org/models/object_detection/tf2/'
    model_file = model_name + '.tar.gz'
    model_dir = tf.keras.utils.get_file(
        fname=model_name,
        origin=base_url +
        model_date +
        '/' +
        model_file,
        untar=True)
    return str(model_dir)


def train_model():
    os_name = get_platform()
    print(os_name)
    if not os.path.exists('./_my_model'):
        os.mkdir('_my_model')
    if not os.path.exists('./_exported-models'):
        os.mkdir('_exported-models')

    if "models" in pathlib.Path.cwd().parts:
        while "models" in pathlib.Path.cwd().parts:
            os.chdir('..')
    elif not pathlib.Path('models').exists():
        os.system('git clone --depth 1 https://github.com/tensorflow/models')
        os.chdir('models/research')
        if os_name is 'Windows':
            subprocess.call(["../../protoc/protoc-3.4.0-win32/bin/protoc.exe",
                            "object_detection/protos/*.proto", "--python_out=."])
        elif os_name is 'Linux':
            st = os.stat('../../protoc/protoc-3.13.0-linux-x86_64/bin/protoc')
            os.chmod(
                '../../protoc/protoc-3.13.0-linux-x86_64/bin/protoc',
                st.st_mode | stat.S_IEXEC)
            subprocess.call(["../../protoc/protoc-3.13.0-linux-x86_64/bin/protoc",
                            "object_detection/protos/*.proto", "--python_out=."])
        os.system('pip install .')
        os.chdir('../..')

    MODEL_DATE = '20200711'
    MODEL_NAME = 'ssd_resnet50_v1_fpn_640x640_coco17_tpu-8'
    PATH_TO_MODEL_DIR = download_model(MODEL_NAME, MODEL_DATE)
    print(PATH_TO_MODEL_DIR)

    if not os.path.exists('_pre-trained-models'):
        shutil.copytree(PATH_TO_MODEL_DIR, '_pre-trained-models')
    if not os.path.exists('./model_main_tf2.py'):
        shutil.copy('models/research/object_detection/model_main_tf2.py', '.')
    if not os.path.exists('./exporter_main_v2.py'):
        shutil.copy('models/research/object_detection/exporter_main_v2.py', '.')

    print("Start training")
    subprocess.call(["python",
                    "model_main_tf2.py",
                    "--model_dir=_my_model",
                    "--pipeline_config_path=./pipeline.config"])

    print("Start exporting model")
    subprocess.call(["python",
                    "exporter_main_v2.py",
                    "--input_type", "image_tensor",
                    "--pipeline_config_path=./pipeline.config",
                    "--trained_checkpoint_dir", "./_my_model/",
                    "--output_directory", "./_exported-models/"])

    print("Done")
