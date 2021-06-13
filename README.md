## 马尔科夫链生成音乐

对midi文件进行解析，依靠马尔科夫链生成新的midi音乐

### Requirements

pretty_midi==0.2.9



### 运行

基本执行过程在`main.py`文件中详细阐述，以提供的`茉莉花.mid`为例

`python main.py`

命令行中会输出该mid文件所有的音轨信息

所得到的`inst.mid`为提取的105号乐器的单轨音乐（105定义在代码中的`inst_id`变量）

所得到的`generated.mid`为生成的音乐



### 模块功能

#### midi2seq.py

midi文件格式处理模块，函数包括：

- print_inst：打印包含的所有音轨乐器信息
- read_all_notes：读取midi文件并提取所需要的音符内容
- note_list2pitch_list：将音符序列转化为规范的音高序列，该过程将duration信息离散化
- pitch_list2note_list：上一个函数的反过程
- save_note_list：将音符序列保存为新的midi文件



#### vocab_utils.py

词表预处理模块，该模块仿照了计算机领域的自然语言处理NLP的构建过程，将mid中出现的音高和时值信息重新编码，方便后续马尔科夫链生成操作，函数包括：

- pitch_list2pair_list：将规范的音高序列转化为`（pitch，duration）`的pair结构
- pair_list2pitch_list：上一个函数的反过程
- creat_dict：创建转换词典



#### transition_matrix.py

马尔科夫链技术生成模块，函数包括：

- transition_matrix：依据序列计算转移矩阵
- generate_seq：依据转移矩阵计算新的生成序列



#### inst_info.txt

midi文件中的乐器信息与其对应的id

