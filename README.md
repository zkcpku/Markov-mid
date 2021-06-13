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



#### 代码逻辑

基本原理即从概率论的角度，将音乐看作一个随机过程，通过对给定的midi文件进行解析，得到音符与时值的序列，并综合考虑其构成的序列的变化过程中的概率，得到转移矩阵，最后通过采样的方法得到新的音乐

- 首先对midi文件进行解析，midi文件中包含多个instrument，需要确定一个主要的instrument进行后续操作。一个简单的想法是根据其中含有的音符序列的长度进行确定，如：

  ```
  乐器信息：                                                
  index    name    note length                         
  105      105Banjo                   班卓琴（美洲）          
           1435                                        
  25       25 Acoustic Guitar(steel)       钢弦吉他        
           1435                                        
  64       64 SopranoSax               高音萨克斯风          
           424                                         
  22       22Harmonica                         口琴      
           205                                         
  22       22Harmonica                         口琴      
           201                                         
  77       77Shakuhachi                    日本尺八        
           122                                         
  75       75 PanFlute                         排箫      
           122                                         
  115      115Woodblock                        木鱼      
           99                                          
  110      110Fiddle                       民族提琴        
           91                                          
  48       48 String Ensemble1        弦乐合奏音色1          
           80                                          
  40       40Violin                          小提琴       
           69                                          
  43       43Contrabass                  低音大提琴         
  ```

  其中，105号乐器——班卓琴（美洲）出现了1435个音符信息，可以选择该乐器作为主要的instrument

- midi中的原始信息为：

  ```
  [Note(start=1.463414, end=1.499999, pitch=69, velocity=51), Note(start=1.506097, end=1.542682, pitch=69, velocity=51), Note(start=1.554877, end=1.591463, pitch=69, velocity=51), ...
  ```

  我们提取音符信息pitch，并对duration进行离散化，得到新的序列：

  ```
  [{'pitch': 69, 'duration': 1}, {'pitch': 69, 'duration': 1}, {'pitch': 69, 'duration': 1}, {'pitch': 69, 'duration': 1}, {'pitch': 69, 'duration': 1}, {'pitch': 69, 'duration': 1}, ...
  ```

- 依据该序列，得到词表表示：

  ```
  {(72, 2): 0, (-1, -16): 1, (74, 1): 2, (-1, -8): 3, (77, 1): 4, (-1, 1): 5, (69, 16): 6, (74, 16): 7, (67, 1): 8, (62, 8): 9, (60, 8): 10, (67, 8): 11,...
  ```

  依据词表得到新的序列：

  ```
  [1, 6, 36, 27, 3, 12, 20, 32, 29, 37, 33, 13, 3, 12, 20, 17, 1, 35, 36, 25, 3, 10, 20, 32, 29, 37, 33, 12, 3, 27, 20, 6, 1, 34, 36,...
  ```


- 计算马尔可夫转移矩阵，采样生成新的音乐序列

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

