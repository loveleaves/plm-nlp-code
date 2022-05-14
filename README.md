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

- fix(chp4/lstm_sent_polarity.py): 新版本pack_padded_sequence中lengths参数需放在cpu上，更改放置位置
- fix(chp4/transformer_sent_polarity; utils.py):  修复使用GPU时“数据不在同一device”的错误

## 增加

### chp6

- feat(chp6/raw_data.txt): 增加用于测试的爬取得到的真实数据集，每行是一个独立的语段。
- feat(chp6/train.txt): 增加用于train_elmo.py测试的raw_data.txt单词分割后的数据集，每行是一个独立的语段，每个单词用空格分隔。
- feat(chp6/word_segment.py): 增加用于对爬取得到的真实数据集进行单词分割函数代码

## 篇末语

如果本仓库对你有帮助的话，欢迎Fork和star，后续将持续更新