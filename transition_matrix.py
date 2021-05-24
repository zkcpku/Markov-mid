import random
import numpy as np
import random

def transition_matrix(transitions,n = None):
    if not n:
        n = 1+ max(transitions) #number of states

    M = [[0]*n for _ in range(n)]
    

    for (i,j) in zip(transitions,transitions[1:]):
        M[i][j] += 1

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M

# t = [1,1,2,6,8,5,5,7,8,8,1,1,4,5,5,0,0,0,1,1,4,4,5,1,3,3,4,5,4,1,1]
# m = transition_matrix(t)
# for row in m: print(' '.join('{0:.2f}'.format(x) for x in row))

def generate_seq(m, vocab_size, max_len = 1000):
    states = list(range(vocab_size))
    now_len = 0
    rst_seq = []
    start = random.choice(states)
    rst_seq.append(start)
    while now_len < max_len:
        if sum(m[rst_seq[-1]]) == 0:
            break
        change = np.random.choice(states, p=m[rst_seq[-1]])
        rst_seq.append(change)
    return rst_seq