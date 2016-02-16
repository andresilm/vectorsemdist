__author__ = 'aluna'
import RelationVectorSpace
import IncrPCA_DimensionReduction
import CustomClustering
import SVD_DimensionReduction

import sys

vectors_source = '/home/aluna/ParGen_resources/relation_vspace.csv'
rel_to_reduce = '/home/aluna/ParGen_resources/relations_sorted_by_frequency.txt'
rel_freq_src = '/home/aluna/ParGen_resources/frame_extraction.dat'
maxrel = 20



def main(args):
    if len(args) == 3:
        maxrel = int(args[2])
        target_dimension = int(args[1])
        print('Looking for the ' + str(maxrel) + ' most frequent relations.')

        sys.stderr.write('Reducing vectors of argument 1' + '\n')
        DR1 = SVD_DimensionReduction.DimensionReducer()
        DR1.reduce_vectors_of_file_column(vectors_source, rel_to_reduce, 1, n_dim=target_dimension, n_samples=maxrel, step=1)  # arg 1 =  subject
        sys.stderr.write('Reducing vectors of argument 2\n')
        DR1 = None
        DR2 = SVD_DimensionReduction.DimensionReducer()
        DR2.reduce_vectors_of_file_column(vectors_source, rel_to_reduce, 3, n_dim=target_dimension, n_samples=maxrel,step=2)  # arg2  = object
        DR2 = None
        # DR3 = IncrPCA_DimensionReduction.DimensionReducer()
        # DR3.reduce_vectors_of_file_column(filename,3,n_dim=target_dimension,n_samples=n_samples,step=3) # arg2  = object
        # DR3=None

    else:
        print('Usage: [this].py target_dimension\n')


main(sys.argv)
