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
parser.add_argument('--nBits', type=int, default=1024, help='Number of bits for Morgan fingerprints')
parser.add_argument('--radius', type=int, default=2, help='radius for Morgan fingerprints')
parser.add_argument('--format', type=str, default='bits',choices=['count','bits'], help='Select Morgan fingerprints type')
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
        if args.format == 'count':
            fp = AllChem.GetHashedMorganFingerprint(mol, radius=args.radius, nBits=args.nBits)
        elif args.format == 'bits':
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=args.radius, nBits=args.nBits)
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
