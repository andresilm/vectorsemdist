__author__ = 'aluna'
from numpy import add
from scipy.spatial.distance import cosine

arg1w = 0.5
arg2w = 0.5
predw = 0.0

def vector_to_string(v):
        ret = ''

        if v is not None and len(v) > 0:
            for i in range(0,len(v)-2):
                ret = ret + str(v[i]) + ','
            #sys.stderr.write(str(v)+'\n')
            ret = ret + str(v[len(v)-1])


        return ret #','.join([str(e) for e in v])

def string_to_vector(strvec):

        strvec = strvec.replace(' ','')
        strvec = strvec.replace('\n','')

        return [float(e) for e in strvec.split(',') if e is not '\n']


def vector_mean(vector_set):
    vec_sum = [0 for x in vector_set[0]]
    for vec in vector_set:
        vec_sum = add(vec_sum,vec)

    vec_mean = [x/len(vector_set) for x in vec_sum]

    return vec_mean

def distance(e1, e2):
        #print ('Distance between ' + str(e1) + ' and ' + str(e2))
        #print('Dim(e1)='+str(len(e1)))
        #print('Dim(e2)='+str(len(e2)))
        return arg1w * cosine(e1[0], e2[0]) + predw * cosine(e1[1], e2[1]) + arg2w * cosine(e1[2], e2[2])


