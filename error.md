# 报错解决

## 通用报错

**out of memory**

```docs
#报错info
RuntimeError: CUDA out of memory. Tried to allocate...
#原因
无法为当前程序分配需要的GPU显存
#解决办法
1.减小batch_size
2.linux下nvidia-smi（使用服务器虚拟显卡此命令不一定可用）查看占用GPU的进程，kill掉没用的进程（有运行进程占用一部分显存）
3.使用更大显存的显卡（当使用显卡显存确实无法满足需求）
```

**ConnectionError**

```docs
#报错info
ConnectionError: Couldn't reach https://...
#原因
无法连接到指定网站，被墙或当前网络动荡
#解决办法
1.多次运行看是否成功
2.使用能连接到该网站的代理，并开启系统代理或使当前进程或软件能使用代理
3.在其他网站找到需要的文件下载到本地，并放至指定文件夹内（实在无法连接且无代理）
```



## 各章节报错

### chp4

**lstm_sent_polarity.py; lstm_polarity.py**

```docs
#报错info
TypeError: length_to_mask() missing 1 required positional argument: 'device'
#原因
length_to_mask()新版本改动，使用需额外传入device参数
#解决办法
使用时额外添加device参数
```

**transformer_sent_polarity; transformer_polarity; utils.py**

```docs
#报错info
RuntimeError: 'lengths' argument should be a 1D CPU int64 tensor, but got 1D cuda:0 Long tensor
#原因
pack_padded_sequence()新版本改动，使用lengths参数需放置在cpu上不能放置在GPU上
#解决办法
使用pack_padded_sequence()时保证lengths参数在cpu上
```



