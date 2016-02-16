__author__ = 'aluna'

from scipy.spatial.distance import cosine
from numpy import add, mean
from random import randrange
import sys
from VectorUtil import string_to_vector,vector_to_string,vector_mean,distance

# custom kmeans clustering for relation similarity measure, represented by 3 vectors
class CustomKmeansClustering:
    def __init__(self, nr_clusters):
        self.data = []  # [(r,a1,a2)]
        #self.labels = dict()  # [{rel_name : index in self.data}]
        self.centroids = [] # [(rel_vec_mean,arg1_vec_mean,arg2_vec_mean)]
        self.clusters = []  # [ [rel] ]
        self.nr_clusters = nr_clusters

    def set_data(self, labels, data):
        self.data = data
        self.labels = labels

    def calculate_centroids(self):
        self.curr_centroids = []
        for cluster in self.clusters:

            a1=[self.arg1_vector(rel_name) for rel_name in cluster]
            p = [self.predroot_vector(rel_name) for rel_name in cluster]
            a2 = [self.arg2_vector(rel_name) for rel_name in cluster]

            vm_a1 = vector_mean(a1) # (v1[a1] + ... + vn[a1]) / n
            vm_p = vector_mean(p)
            vm_a2 = vector_mean(a2)

            self.centroids.append((vm_a1,vm_p,vm_a2))

    def reassign_clusters(self):
        self.clusters = [[] for i in range(0, self.nr_clusters)]

        for rel in self.labels:
            cluster_index = self.nearest_centroid(rel)  # index of centroid
            self.clusters[cluster_index].append(rel)

    def choose_initial_centroids(self):
        added = 0
        while added != self.nr_clusters:
            j = randrange(0,len(self.data))
            if self.data[j] not in self.centroids:
                self.centroids.append(self.data[j])
                added = added + 1

        #sys.stderr.write('Initial centroids:\n' + str(self.centroids) + '\n')

    def vectors_of_relation(self,rel_name):
        return self.data[self.labels.index(rel_name)]

    def arg1_vector(self,rel_name):
        v = self.vectors_of_relation(rel_name)
        return v[0]

    def predroot_vector(self,rel_name):
        v = self.vectors_of_relation(rel_name)
        return v[1]

    def arg2_vector(self,rel_name):
        v = self.vectors_of_relation(rel_name)
        return v[2]

    def nearest_centroid(self, rel_name):
        mindist, minindex = 9999, -1

        for i in range(0,len(self.centroids)):
            dist = distance(self.vectors_of_relation(rel_name), self.centroids[i])
            if dist < mindist:
                mindist = dist
                minindex = i

        return minindex

    def do_kmeans(self):
        sys.stderr.write('Choosing centroids.'+'\n')
        self.choose_initial_centroids()
        self.prev_centroids = []
        self.clusters = []  # list of lists of relations name
        sys.stderr.write('Starting kmeans loop...'+'\n')
        while self.centroids != self.prev_centroids:
            self.reassign_clusters()
            self.prev_centroids = self.centroids
            self.calculate_centroids()
            
        sys.stderr.write('Kmeans ended.'+'\n')

    def set_weights(self,arg1w=0.33,predw=0.33,arg2w=0.33):
        self.arg1w = arg1w
        self.arg2w = arg2w
        self.predw = predw



    def save_clusters_to_file(self, filename):
        fout = open(filename, 'w')

        for i in range(0,len(self.clusters)):
            for r in self.clusters[i]:
                fout.write(r + '@' + str(i) + '\n')
                fout.flush()

        fout.close()


    def load_data_from_csv_file(self,filename):
        fin = open(filename,'r')
        self.labels = []
        self.data = []

        for line in fin:
            rel_name,vec1,predvec,vec2 = line.split('|')
            self.labels.append(rel_name) #will not find any repetition
            self.data.append((string_to_vector(vec1),string_to_vector(predvec),string_to_vector(vec2.replace('\n',''))))

        fin.close()
