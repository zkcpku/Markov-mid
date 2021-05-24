def pitch_list2pair_list(pitch_list):
    return [(e['pitch'],e['duration']) for e in pitch_list]
def pair_list2pitch_list(pair_list):
    return [{'pitch':e[0],'duration':e[1]} for e in pair_list]

def creat_dict(all_seq):
    all_set = list(set(all_seq))
    seq2idx = {all_set[i]:i for i in range(len(all_set))}
    idx2seq = {seq2idx[k]:k for k in seq2idx}
    return seq2idx, idx2seq