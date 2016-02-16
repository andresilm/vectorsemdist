__author__ = 'aluna'
import VectorUtil

import sys
import random
import os

def load_vectorspace(filename):
    f = open(filename,'r')

    vectors = dict()

    for line in f:
        data = line.split('|')
        if len(data) == 4 and '' not in data:
            a1 = VectorUtil.string_to_vector(data[1].replace(' ',''))
            p = VectorUtil.string_to_vector(data[2].replace(' ',''))
            a2 = VectorUtil.string_to_vector(data[3].replace(' ',''))
            vectors.update({data[0]: (a1,p,a2)})


    return vectors


def main(args):
    msg = 'COMMANDS: lr [word] | cmp [rel1] [rel2] | pv [rel_name] | quit | ls | help\n'
    vectors = load_vectorspace(args[1])
    line = input(msg)

    while line != 'quit':
        cmds = line.split(' ')

        if cmds[0] == 'lr' and len(cmds) <= 3:

            if len(cmds) == 1:
                for v in vectors:
                    sys.stderr.write(v+' | ')
                sys.stderr.write('\n\n')
            else:
                for v in vectors:
                    w = v.split('_')
                    if cmds[1] in w:
                        sys.stderr.write(v + ' , ')
                sys.stderr.write('\n\n')

        elif cmds[0] == 'cmp' and len(cmds) == 3:
            names = cmds
            names[2].replace('\n','')
            if names[1] in vectors and names[2] in vectors:
                #print('Distance between ' + names[1] + ' and ' + names[2] + ' is ')
                print('DISTANCE: ')
                print(str(VectorUtil.distance(vectors[names[1]], vectors[names[2]])) + '\n')


        elif cmds[0] == 'pv' and len(cmds) == 2:
            if cmds[1] in vectors:
                print(vectors[cmds[1]])

        elif cmds[0] == 'fs' and len(cmds) == 2:
            print('Not implemented.')

        elif cmds[0] == 'ls' and len(cmds) == 1:
            print('Loaded '+str(len(vectors)) + ' vectors.')

        elif cmds[0] == 'help' and len(cmds) == 1:
            print('COMMANDS explained:')
            print('lr: find relation containing the word [word]. List all relations loaded if no word is provided.')
            print('ls: display amount of relations loaded.')


        line = input('Type other command.\n' + msg)





main(sys.argv)