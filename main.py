import numpy as np

import midi2seq
import transition_matrix
import vocab_utils

midi_file = '茉莉花.mid'
inst_file = 'inst.mid'
output_file = 'generated.mid'

inst_id = 105

print("乐器信息：")
midi2seq.print_inst(midi_file)



all_notes_dict = midi2seq.read_all_notes(midi_file)
all_pitch_list, min_duration,start_time,vel = midi2seq.note_list2pitch_list(all_notes_dict[inst_id])

midi2seq.save_note_list(all_notes_dict[inst_id],inst_file)


pair_list = vocab_utils.pitch_list2pair_list(all_pitch_list)
seq2idx, idx2seq = vocab_utils.creat_dict(pair_list)


# print(pair_list[:20])

input_seq = [seq2idx[e] for e in pair_list]

m = transition_matrix.transition_matrix(input_seq)

# print(np.array(m).shape)

output_seq = transition_matrix.generate_seq(m, len(seq2idx))
output_seq = [idx2seq[e] for e in output_seq]
output_pitch_list = vocab_utils.pair_list2pitch_list(output_seq)
output_note_list = midi2seq.pitch_list2note_list(output_pitch_list, min_duration,start_time,vel)


midi2seq.save_note_list(output_note_list,output_file)