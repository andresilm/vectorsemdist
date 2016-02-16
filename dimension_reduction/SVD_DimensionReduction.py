__author__ = 'aluna'
from sklearn.decomposition import PCA, IncrementalPCA,TruncatedSVD
import VectorUtil
import sys

pred_root_col = 2

class DimensionReducer:
    def __init__(self):

        self.data = []


    def set_data(self,vector_set):
        self.data = vector_set


    def train(self):
        self.dimred.transform(self.data)


    def reduce_dimensions_of_vector(self,vector):
        return self.dimred(vector)

    def print_vector(self,v):
        ret = ''

        if len(ret) > 0:
            for i in range(0,len(v)-2):
                ret = ret + str(v[i]) + ','
            #sys.stderr.write(str(v)+'\n')
            ret = ret + str(v[len(v)-1])

        return ret



    def reduce_vectors_of_file_column(self,vectors_file,rel_list_filename,col,n_dim=100,n_samples=100,step=1):
        self.labels = []
        self.data = []

        self.preds = []
        incomplete_vector_set_relation_list = []

        fin= open(vectors_file,'r+')
        #fout= open(filename+'_reduced','a+')
        rel_list_file = open(rel_list_filename,'r')
        sys.stderr.write('Loading most frequent relations list.\n')

        most_frequent_relations_list = []
        sample_count = 0
        for line in rel_list_file:
            most_frequent_relations_list.append(line.split('\t')[0])
            sample_count = sample_count + 1
            if sample_count == n_samples:
                break

        #print(str(most_frequent_relations_list))

        sys.stderr.write('Done.' + str(len(most_frequent_relations_list)) + '\n')


        sample_count = 0
        for line in fin:
            line = line.split('|')
            vec = line[col].replace(' ','')
            rel = line[0].replace(' ','')
            if rel in most_frequent_relations_list:
                #print('Loading data of relation ' + rel + '\n')
                vec = VectorUtil.string_to_vector(vec)
                predvec = line[pred_root_col].replace(' ','')
                if step == 1 and predvec is not '':
                   # print('pred col = ' + str(line[pred_root_col]))
                    predvec = VectorUtil.string_to_vector(predvec)
                    self.preds.append(predvec)

                if predvec is not '':
                    self.labels.append(rel)
                    self.data.append(vec)
                    sample_count = sample_count + 1
                else:
                    sys.stderr.write('WARNING: relation "' + rel + '" skipped due to the absence of predicate root vector.\n')
                    incomplete_vector_set_relation_list.append(rel)


        sys.stderr.write(str(len(self.data))+' relations loaded.\n')


        if step == 1:
            sys.stderr.write('Creating new file..\n')
            fout = self.create_empty_output_file(vectors_file+'_reduced_step1.csv',n_samples,self.labels)
            fin.seek(0)
        elif step >= 2:
            fin.close()
            fin = open(vectors_file+'_reduced_step'+str(step-1)+'.csv','r')
            fout = open(vectors_file+'_reduced_step'+str(step)+'.csv','w')

        sys.stderr.write('Reducing, please wait...\n')
        dimred = TruncatedSVD(n_components=n_dim)
        dimred.fit(self.data)
        sys.stderr.write('Reduction finished.\n')

        sample_count = 0

        for line in fin:
            if line == '\n':
                continue

            sline = line.split('|')
            rel = sline[0].replace(' ','')

            if rel in most_frequent_relations_list:
                if rel in incomplete_vector_set_relation_list:
                    continue

                if len(sline)-1 < col:
                    sys.stderr.write('WARNING: not enough columns in line\n')
                  #  sys.stderr.write(str(len(sline)) + '\n')

                rel_pos = self.labels.index(rel)
                if step == 1:
                    sline[pred_root_col] = VectorUtil.vector_to_string(self.preds[rel_pos])

                vecred = dimred.transform(self.data[rel_pos])
                #sys.stderr.write('Transformed vector size is ' + str(len(vecred))+ ' x ' + str(len(vecred[0])) + '\n')


                if len(vecred) == 1:
                    vec_write = vecred[0]

                #self.data[sample_count] = vec
                sline[col] = VectorUtil.vector_to_string(vec_write) #vector reduced is put in the right column

                rvstr = '|'.join(sline)

                #sline[0] = rel
                #print(sline[col])


               # sys.stderr.write(rvstr)
                fout.write(rvstr+'\n')
                fout.flush()

                sample_count = sample_count + 1



        fout.close()

    def get_reduced_data(self):
        return self.data,self.labels

    def create_empty_output_file(self,filename,nr_lines,labels):

        f = open(filename,'w')
        #c = ['|' for j in range(0,nr_cols-1)]
        for i in range(0,len(self.data)):
            #sys.stderr.write('writing line...')
            f.write(labels[i] + '|S|PR|O\n')
            #f.flush()

        f.seek(0)
        return f











