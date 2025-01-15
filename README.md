# plm-nlp-book

本仓库是对《[自然语言处理：基于预训练模型的方法](https://github.com/HIT-SCIR/plm-nlp-code)》（作者：车万翔、郭江、崔一鸣）一书github仓库代码的一些修正和增加，全文格式按照[git commit-message规范书写](https://github.com/loveleaves/git/blob/main/git-message.md)。

## 本仓库代码测试环境

* Python: 3.8.13
* PyTorch: 1.11.0
* Transformers: 4.9.0
* cuda：11.3
* NLTK: 3.5
* LTP: 4.0

## 修改

### chp2

- fix(chp2/svd.py): 按照书上和所给样例，对画图范围更改

### chp4

- fix(chp4/lstm_sent_polarity.py; lstm_polarity.py): 新版本pack_padded_sequence中lengths参数要求放在cpu上，更改了放置位置
- fix(chp4/transformer_sent_polarity; transformer_polarity; utils.py):  修复使用GPU时“数据不在同一device”的错误

## 增加

### chp6

- feat(chp6/raw_data.txt): 增加用于测试的爬取得到的真实数据集，每行是一个独立的语段。
- feat(chp6/train.txt): 增加用于train_elmo.py测试的raw_data.txt单词分割后的数据集，每行是一个独立的语段，每个单词用空格分隔。
- feat(chp6/word_segment.py): 增加用于对爬取得到的真实数据集进行单词分割函数代码

## 报错汇总

运行代码可能出现的问题汇总于[这里](./error.md)

### 勘误
* 2.1.2节（词的分布式表示），pmi计算函数代码中，以下语句注释中的“分子”应改为“分母”
```
expected = np.outer(row_totals, col_totals) / total # 获得每个元素的分母
```

* 【数学符号】一节中，【线性代数】部分【矩阵A与矩阵B的Hardamard乘积】中，Hardamard的拼写应该为Hadamard。

* 书中2.1.2节：3.奇异值分解小节（17页）中，矩阵**V**的维度应为|C| x r，即$\bm{V} \in \mathbb{R}^{|\mathbb{C}| \times r}$。

* 书中3.4.3节`convert_t2s.py`：
```python
f_in = open(sys.argv[0], "r")
```
修正为
```python
f_in = open(sys.argv[1], "r")
```

* 书中3.4.3节`wikidata_cleaning.py`：
```python
f_in = open(sys.argv[0], 'r')
```
修正为
```python
f_in = open(sys.argv[1], 'r')
```
此外，为了兼容Python 3.7以上版本，将`remove_control_chars`函数修改为：
```python
def remove_control_chars(in_str):
    control_chars = ''.join(map(chr, list(range(0, 32)) + list(range(127, 160))))
    control_chars = re.compile('[%s]' % re.escape(control_chars))
    return control_chars.sub('', in_str)
```

* 书中4.6.1节`Vocab`类的`__init__`与`build`方法有误，修正为：
```python
class Vocab:
    def __init__(self, tokens=None):
        self.idx_to_token = list()
        self.token_to_idx = dict()

        if tokens is not None:
            if "<unk>" not in tokens:
                tokens = tokens + ["<unk>"]
            for token in tokens:
                self.idx_to_token.append(token)
                self.token_to_idx[token] = len(self.idx_to_token) - 1
            self.unk = self.token_to_idx['<unk>']

    @classmethod
    def build(cls, text, min_freq=1, reserved_tokens=None):
        token_freqs = defaultdict(int)
        for sentence in text:
            for token in sentence:
                token_freqs[token] += 1
        uniq_tokens = ["<unk>"] + (reserved_tokens if reserved_tokens else [])
        uniq_tokens += [token for token, freq in token_freqs.items() \
                        if freq >= min_freq and token != "<unk>"]
        return cls(uniq_tokens)
```

* 书中4.6.5节使用的`MLP`模型类是基于`EmbeddingBag`的`MLP`实现，与4.6.3节的`MLP`实现有所区别，具体如下：
```python
class MLP(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_class):
        super(MLP, self).__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(embedding_dim, hidden_dim)
        self.activate = F.relu
        self.linear2 = nn.Linear(hidden_dim, num_class)

    def forward(self, inputs, offsets):
        embedding = self.embedding(inputs, offsets)
        hidden = self.activate(self.linear1(embedding))
        outputs = self.linear2(hidden)
        log_probs = F.log_softmax(outputs, dim=1)
        return log_probs
```

* 书中6.2.3节`ELMoLstmEncoder`类的`forward`函数实现有误，修正为：
```python
def forward(self, inputs, lengths):
    batch_size, seq_len, input_dim = inputs.shape
    rev_idx = torch.arange(seq_len).unsqueeze(0).repeat(batch_size, 1)
    for i in range(lengths.shape[0]):
        rev_idx[i,:lengths[i]] = torch.arange(lengths[i]-1, -1, -1)
    rev_idx = rev_idx.unsqueeze(2).expand_as(inputs)
    rev_idx = rev_idx.to(inputs.device)
    rev_inputs = inputs.gather(1, rev_idx)

    forward_inputs, backward_inputs = inputs, rev_inputs
    stacked_forward_states, stacked_backward_states = [], []

    for layer_index in range(self.num_layers):
        # Transfer `lengths` to CPU to be compatible with latest PyTorch versions.
        packed_forward_inputs = pack_padded_sequence(
            forward_inputs, lengths.cpu(), batch_first=True, enforce_sorted=False)
        packed_backward_inputs = pack_padded_sequence(
            backward_inputs, lengths.cpu(), batch_first=True, enforce_sorted=False)

        # forward
        forward_layer = self.forward_layers[layer_index]
        packed_forward, _ = forward_layer(packed_forward_inputs)
        forward = pad_packed_sequence(packed_forward, batch_first=True)[0]
        forward = self.forward_projections[layer_index](forward)
        stacked_forward_states.append(forward)

        # backward
        backward_layer = self.backward_layers[layer_index]
        packed_backward, _ = backward_layer(packed_backward_inputs)
        backward = pad_packed_sequence(packed_backward, batch_first=True)[0]
        backward = self.backward_projections[layer_index](backward)
        # convert back to original sequence order using rev_idx
        stacked_backward_states.append(backward.gather(1, rev_idx))

        forward_inputs, backward_inputs = forward, backward

    # stacked_forward_states: [batch_size, seq_len, projection_dim] * num_layers
    # stacked_backward_states: [batch_size, seq_len, projection_dim] * num_layers
    return stacked_forward_states, stacked_backward_states
```

* 书中7.4.3节（199页）"句对文本分类"→"代码实现"中的`tokenize()`函数存在问题，请按如下进行修正。
```python
def tokenize(examples):
    return tokenizer(examples['hypothesis'], examples['premise'], truncation=True, padding='max_length')
```
修正为
```python
def tokenize(examples):
    return tokenizer(examples['sentence1'], examples['sentence2'], truncation=True, padding='max_length')
```

* 书中5.3.4节（143页）GloVe词向量训练部分代码在计算L2损失时存在问题，请按如下进行修正。
```python
loss = (torch.sum(word_embeds * context_embeds, dim=1) + word_biases + context_biases - log_counts) ** 2
```
修正为
```python
loss = (torch.sum(word_embeds * context_embeds, dim=1, keepdim=True) + word_biases + context_biases - log_counts) ** 2
```

## 篇末语

如果本仓库对你有帮助的话，欢迎Fork和star，后续将持续更新