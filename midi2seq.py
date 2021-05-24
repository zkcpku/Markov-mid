import pretty_midi

def simplify_midi(midi_file,out_path):
    # 取音符最长的乐器单独提取出来作为新的midi
    mid = pretty_midi.PrettyMIDI(midi_file=midi_file)
    long_midi_notes = []
    for inst in mid.instruments:
        print(inst.program)
        inst_notes = inst.notes
        if len(long_midi_notes) < len(inst_notes):
            long_midi_notes = inst_notes
            print("change to:",inst.program)
    
    mid = pretty_midi.PrettyMIDI()
    # if want to change instument, see https://www.midi.org/specifications/item/gm-level-1-sound-set
    instument = pretty_midi.Instrument(1, False, "Developed By zkc")
    instument.notes = long_midi_notes

    mid.instruments.append(instument)
    if out_path is not None:
        mid.write(out_path)
    return long_midi_notes

def print_inst(midi_file):
    INST_INFO_PATH = 'inst_info.txt'
    with open(INST_INFO_PATH,'r',encoding='utf8') as f:
        inst_info = f.readlines()
    mid = pretty_midi.PrettyMIDI(midi_file=midi_file)
    print("index",'\t','name','\t','note length')
    this_inst_info = [[inst.program, inst_info[inst.program],len(inst.notes)] for inst in mid.instruments]
    this_inst_info.sort(key = lambda x:-x[-1])
    for e in this_inst_info:
        print(e[0],'\t',e[1],'\t',e[2])

def read_all_notes(midi_file):
    mid = pretty_midi.PrettyMIDI(midi_file = midi_file)
    rst_dict = {}
    for inst in mid.instruments:
        rst_dict[inst.program] = inst.notes
    return rst_dict


def get_duration(min_duration,this_duration):
    return round(this_duration / min_duration)
def note_list2pitch_list(note_list):
    note_list = [e for e in note_list if e.start < e.end]
    all_duration = [e.end - e.start for e in note_list]
    min_duration = min(all_duration)
    all_duration_time = [get_duration(min_duration,e) for e in all_duration]
    all_pitch_list = []
    for i in range(len(note_list)):
        if i!=0:
            pause_duration = get_duration(min_duration, note_list[i].start - note_list[i-1].end)
            if pause_duration != 0:
                all_pitch_list.append({'pitch':-1, 'duration':pause_duration})
        all_pitch_list.append({'pitch':note_list[i].pitch,'duration':all_duration_time[i]})
#     all_pitch_list = [{'pitch':note_list[i].pitch,'duration':all_duration_time[i]} for i in range(len(note_list))]
    return all_pitch_list, min_duration, note_list[0].start, note_list[0].velocity


def pitch_list2note_list(all_pitch, min_duration, start, vel):
    rst = []
    start_time = start
    for e in all_pitch:
        if e['pitch'] != -1:
            this_note = pretty_midi.Note(vel, e['pitch'], start_time, (start_time + min_duration * e['duration']) )
            start_time = start_time + min_duration * e['duration']
            rst.append(this_note)
        else:
            start_time = start_time + min_duration * e['duration']
    return rst




def save_note_list(note_list,out_path):
    mid = pretty_midi.PrettyMIDI()
    # if want to change instument, see https://www.midi.org/specifications/item/gm-level-1-sound-set
    instument = pretty_midi.Instrument(1, False, "Developed By zkc")
    instument.notes = note_list

    mid.instruments.append(instument)
    if out_path is not None:
        mid.write(out_path)
