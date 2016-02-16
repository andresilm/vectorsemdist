__author__ = 'aluna'
import RelationVectorSpace
import IncrPCA_DimensionReduction

import CustomClustering

import sys

def main(args):
    if len(args) == 2:

        k = int(args[1])

        sys.stderr.write('Starting clustering process'+'\n')
        CC = CustomClustering.CustomKmeansClustering(k)
        CC.load_data_from_csv_file('/home/aluna/ParGen_resources/relation_vspace.csv_reduced_step2.csv')
        CC.set_weights(arg1w=0.5,predw=0,arg2w=0.5)
        CC.do_kmeans()
        sys.stderr.write('Saving clusters to file'+'\n')
        CC.save_clusters_to_file('/home/aluna/ParGen_resources/relation_clustering_'+ str(k) + '.dat')
    else:
        print('Usage: [this].py n_clusters\n')


main(sys.argv)