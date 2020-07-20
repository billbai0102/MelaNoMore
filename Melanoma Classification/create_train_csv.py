"""
This script creates csvs for the train, validation, and test folders.
It allows PyTorch to easily read in the data.
"""

# imports
import pandas as pd
import os

# paths to train, val, and test directories
train_path = './data/DermMel/train'
val_path = './data/DermMel/valid'
test_path = './data/DermMel/test'

'''
:param path: path to look for files in
:param out_name: what to save the csv as
:param file_type: the filetype of files in the directory.
'''
def create_csv(path, out_name, file_type=['.jpeg', '.jpg']):
    df = pd.DataFrame(columns=['id', 'target'])
    malignant_path = path + '/Melanoma'
    benign_path = path + '/NotMelanoma'

    for filename in os.listdir(malignant_path):
        if filename.endswith(file_type[0]):
            data = {
                'id': filename.replace(file_type[0], ''),
                'target': 1
            }
            df = df.append(data, ignore_index=True)

    for filename in os.listdir(benign_path):
        if filename.endswith(file_type[1]):
            data = {
                'id': filename.replace(file_type[1], ''),
                'target': 0
            }
            df = df.append(data, ignore_index=True)

    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(f'./data/DermMel/{out_name}.csv')


# creates csvs for each of the three directories.
create_csv(train_path, 'train_labels')
create_csv(val_path, 'val_labels')
create_csv(test_path, 'test_labels')
