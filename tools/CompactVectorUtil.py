__author__ = 'aluna'
import math
import sys

def vector_to_string(cvec):
    return ','.join(key+':'+str(cvec[key]) for key in cvec)

def string_to_vector(strvec):
    v = dict()
    pairs = strvec.split(',')
    for p in pairs:
        p = p.split(':')
       # print(str(p))
        if len(p)  == 2:
            v.update({p[0] : int(p[1])})
        #else:
         #   sys.stderr.write('WARNING: format error\n')
    return v

#def vector_mean(vector_set,dim):



def relation_similarity(r1,r2):
    return (cosine_sim(r1[0],r2[0]) + cosine_sim(r1[2],r2[2])) / 2.

def cosine_sim(cvec1=dict(),cvec2=dict()): #cvec are sets
    fk_inters = [key for key in cvec1 if key in cvec2]

    u = 0
    for feat_key in fk_inters:
        u = u + cvec1[feat_key] * cvec2[feat_key]

    d1 = 0
    for feat_key in cvec1:
        d1 = d1 + cvec1[feat_key] * cvec1[feat_key]
    #d1 = math.sqrt(d1)

    d2 = 0
    for feat_key in cvec2:
        d2 = d2 + cvec2[feat_key] * cvec2[feat_key]

    #d2 = math.sqrt(d2)

    d = math.sqrt(d1 * d2)

    return u/d

def max_value(collection):
    m = -1
    for e in collection:
        if collection[e]>m:
            m = collection[e]
    return m