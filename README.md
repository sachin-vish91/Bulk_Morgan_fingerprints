# Bulk_Morgan_fingerprints
Bulk_morgan_fingerprints is able to generate the Morgan fingerprints for 50,000 molecules in 20 seconds using 20 core CPU. This script is written using multiprocessing technique that is able to generate the Morgan fingerprints faster than compared to normal method.<br />
sample file is available in the folder name input.csv.

**To run this script download the code and run the following command** <br />
python Bulk_Morgan_Fingerprints.py --file_path input.csv --o path_output_file
<br />
for all the option see below:
--file_path = full path file contains smiles with header name is 'SMILES'<br />
--o = full path for the output file <br />
--nBits = number of bits default:1024 <br />
--radius = select radious default:2 <br />
--format = bits or count format default:bits <br />
