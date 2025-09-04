# lua53-aidec-inputgen
一种Lua53字节码解析工具，输出非常具有格式化，可以在加入特定token的AI模型里做数据集

基础词典来自2.7GB的Lua代码文件进行的32K的BPE

然后再加上本工具的自定义特殊token以及对话用的3个token（EOS在32K里）

一共37010个token

> `LuaCopilot_bbpe_48k.zip`是我后来重新基于更大规模（4.2G的lua+8105常用汉字）训练的新的原始的分词器，能把Lua代码转换为1/5甚至1/6量（bytes->int）tokens的新分词器。这样一般来说4mb以内的lua文件都可以一次喂进1m的模型里

> `LuaCopilot_bbpe_64k.zip`是新一代BBPE分词器，基于`20.1GB`的超大Lua样本，因为样本上来之后分词器学到很多词语，虽然转换比例降低到1/2到1/3左右，基本上断绝了3mb的lua（3MB的Lua大部份是批量生成出来的数据，如果是人工写的转换率可能会好一些）

# 建议的SFT-ChatML
源码：
```lua
a=1
```
用于AIDEC实际的训练内容（建议加入随机strip保证模型可以在不依赖Upvaldesc-name等可能不存在的内容也可以正常瞎猜）：
```chatml
<|im_start|>user
<|Proto|><|Proto-nupvalues=1|><|Proto-numparams=0|><|Proto-is_vararg=1|><|Proto-maxstacksize=2|><|Proto-sizeupvalues|>1<|/Proto-sizeupvalues|><|Proto-sizek|>2<|/Proto-sizek|><|Proto-sizecode|>0<|/Proto-sizecode|><|Proto-sizelineinfo|>2<|/Proto-sizelineinfo|><|Proto-sizep|>0<|/Proto-sizep|><|Proto-sizelocvars|>0<|/Proto-sizelocvars|><|Proto-linedefined|>0<|/Proto-linedefined|><|Proto-lastlinedefined|>0<|/Proto-lastlinedefined|><|Proto-k|><|Proto-k-idx|>0<|/Proto-k-idx|><|Constant|>"a"<|/Constant|><|Proto-k-idx|>1<|/Proto-k-idx|><|Constant|>5e-324<|/Constant|><|/Proto-k|><|Proto-code|><|Proto-code-idx|>0<|/Proto-code-idx|><|Instruction|><|OP_SETTABUP|><|Instruction-T=0|><|Instruction-A=0|><|Instruction-B=OpArgK|><|Instruction-B-ISK=true|><|Instruction-B-K=0|><|Instruction-B-R=256|><|Instruction-C=OpArgK|><|Instruction-C-ISK=true|><|Instruction-C-K=1|><|Instruction-C-R=257|><|Instruction-MODE=iABC|><|Instruction-INLINE=false|><|Instruction-JUMP=false|><|Instruction-A=0|><|Instruction-B=256|><|Instruction-C=257|><|Instruction-Bx|>131329<|/Instruction-Bx|><|Instruction-sBx|>258<|/Instruction-sBx|><|Instruction-Ax|>33620224<|/Instruction-Ax|><|/Instruction|><|Proto-code-idx|>1<|/Proto-code-idx|><|Instruction|><|OP_RETURN|><|Instruction-T=0|><|Instruction-A=0|><|Instruction-B=OpArgU|><|Instruction-B-ISK=false|><|Instruction-B-K=1|><|Instruction-B-R=1|><|Instruction-C=OpArgN|><|Instruction-C-ISK=false|><|Instruction-C-K=0|><|Instruction-C-R=0|><|Instruction-MODE=iABC|><|Instruction-INLINE=false|><|Instruction-JUMP=false|><|Instruction-A=0|><|Instruction-B=1|><|Instruction-C=0|><|Instruction-Bx|>512<|/Instruction-Bx|><|Instruction-sBx|>-130559<|/Instruction-sBx|><|Instruction-Ax|>131072<|/Instruction-Ax|><|/Instruction|><|/Proto-code|><|Proto-lineinfo|><|LineInfo|>1<|LineInfo-pad|>1<|LineInfo-pad|><|/LineInfo|><|/Proto-lineinfo|><|Proto-locvars|><|/Proto-locvars|><|Proto-upvalues|><|Proto-upvalues-idx|>0<|/Proto-upvalues-idx|><|Upvaldesc|><|Upvaldesc-name|>_ENV<|/Upvaldesc-name|><|Upvaldesc-instack=1|><|Upvaldesc-idx=0|><|/Upvaldesc|><|/Proto-upvalues|><|Proto-source|>@demo.lua<|/Proto-source|><|Proto-p|><|/Proto-p|><|/Proto|><|im_end|>
<|im_start|>assistant
a=1<|im_end|>
```

> 想要让LLM理解语义还不如提前帮他处理好语义……这样就能把一段描述转化为具体的令牌值，这会对具体任务执行有巨大帮助……无论模型大小，就都能相对敏感的认识到任务……至少理论是这样的。值得注意的是，这个工具输出的汇编信息相对于原Lua文件是上百倍的体积膨胀，绝对不适合人类汇编分析使用……

> 原生支持把内容解析为strip后内容（抹除debug信息），这样可以同时生产处正常字节码和精简字节码的解析

> 当前的设计不支持大文件，因为几KB的带有debug信息的Lua加上其解析汇编的结果，Token就会碰到超过1M……经验上讲，文本字节长度50MB差不多就是1M的Token容量，所以这个工具天然不支持大文件，但是简单的小文件应该有希望。
