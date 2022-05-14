from ltp import LTP
import codecs
from tqdm.auto import tqdm

def preprocess_corpus(source_path, target_path):
    ltp = LTP()
    print("starting word segment")
    with codecs.open(source_path, "r", encoding="utf-8") as f:  # codecs好处：不会因为编码问题出错
        for line in tqdm(f):
            line = line.rstrip()
            segment, hidden = ltp.seg([line])
            sentence = ""
            with codecs.open(target_path, "a+", encoding="utf-8") as fp:
                for i in segment:
                    for j in i:
                        sentence += j + ' '
                fp.write(sentence)
                fp.write('\n')
preprocess_corpus('raw_data.txt','train.txt')
