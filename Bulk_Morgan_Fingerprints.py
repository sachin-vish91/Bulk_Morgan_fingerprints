#Author: Sachin Vishwakarma

import glob
import pandas as pd
import numpy as np
from rdkit import Chem
import concurrent.futures
import time
from itertools import chain
from rdkit.Chem import AllChem
import glob, argparse


parser = argparse.ArgumentParser(description='Morgan_fingerprints using multitask')
parser.add_argument('--file_path', type=str, default='', help='path for the Fingerprints files')
parser.add_argument('--o', type=str, default='', help='output folder for saving file')
args = parser.parse_args()

def load_file():
	dataset = pd.read_csv(args.file_path, header=0)
	smiles = dataset.SMILES
	return smiles

def File_generator(file,smiles):
    
    Morgan_fingerprint_df = pd.DataFrame(file)
    Morgan_fingerprint_df['SMILES'] = smiles
    Morgan_fingerprint_df.to_csv(args.o + '/Fingerprints.csv', header=False, index=False)
    
    print('File saved')

def Morgan_fingerprints(smile):
    try:
        mol = Chem.MolFromSmiles(smile)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
        figerprints = list(fp)
    except:
        figerprints = ''
        
    return figerprints

def Multi_process(smiles):
    start = time.time()
    Morgan_fingerprint = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.map(Morgan_fingerprints, smiles)
        for result in future:
            Morgan_fingerprint.append(result)
    print('Total time taken for ', len(smiles), 'molecules', int(time.time() - start), 'seconds' )
    
    File_generator(Morgan_fingerprint, smiles)

def main():
    smiles = load_file()
    Multi_process(smiles)

if __name__ == '__main__':
    main()
