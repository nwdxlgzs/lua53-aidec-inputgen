import struct

TOKEN_SET = set()


class OpMode:
    iNone = -1
    iABC = 0
    iABx = 1
    iAsBx = 2
    iAx = 3

    @staticmethod
    def tostr(mode):
        if mode == OpMode.iABC:
            return "iABC"
        elif mode == OpMode.iABx:
            return "iABx"
        elif mode == OpMode.iAsBx:
            return "iAsBx"
        elif mode == OpMode.iAx:
            return "iAx"
        else:
            return "iNone"


class OpArgMask:
    OpArgNone = -1
    OpArgN = 0
    OpArgU = 1
    OpArgR = 2
    OpArgK = 3

    @staticmethod
    def tostr(mask):
        if mask == OpArgMask.OpArgN:
            return "OpArgN"
        elif mask == OpArgMask.OpArgU:
            return "OpArgU"
        elif mask == OpArgMask.OpArgR:
            return "OpArgR"
        elif mask == OpArgMask.OpArgK:
            return "OpArgK"
        else:
            return "OpArgNone"


OpDefines = [
    # op-code | op-name | T | A | B | C | mode | inline | jump
    (0, "OP_MOVE", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (1, "OP_LOADK", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgN, OpMode.iABx,
     lambda i: False, False),
    (2, "OP_LOADKX", 0, 1, OpArgMask.OpArgN, OpArgMask.OpArgN, OpMode.iABx,
     lambda i: True, False),
    (3, "OP_LOADBOOL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: i.C != 0, False),
    (4, "OP_LOADNIL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (5, "OP_GETUPVAL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (6, "OP_GETTABUP", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (7, "OP_GETTABLE", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (8, "OP_SETTABUP", 0, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (9, "OP_SETUPVAL", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (10, "OP_SETTABLE", 0, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (11, "OP_NEWTABLE", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: False, False),
    (12, "OP_SELF", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (13, "OP_ADD", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (14, "OP_SUB", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (15, "OP_MUL", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (16, "OP_MOD", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (17, "OP_POW", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (18, "OP_DIV", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (19, "OP_IDIV", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (20, "OP_BAND", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (21, "OP_BOR", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (22, "OP_BXOR", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (23, "OP_SHL", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (24, "OP_SHR", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False, False),
    (25, "OP_UNM", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (26, "OP_BNOT", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (27, "OP_NOT", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (28, "OP_LEN", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (29, "OP_CONCAT", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgR, OpMode.iABC,
     lambda i: False, False),
    (30, "OP_JMP", 0, 0, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False, True),
    (31, "OP_EQ", 1, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: True, False),
    (32, "OP_LT", 1, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: True, False),
    (33, "OP_LE", 1, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: True, False),
    (34, "OP_TEST", 1, 0, OpArgMask.OpArgN, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: True, False),
    (35, "OP_TESTSET", 1, 1, OpArgMask.OpArgR, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: True, False),
    (36, "OP_CALL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: False, False),
    (37, "OP_TAILCALL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: False, False),
    (38, "OP_RETURN", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (39, "OP_FORLOOP", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False, True),
    (40, "OP_FORPREP", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False, True),
    (41, "OP_TFORCALL", 0, 0, OpArgMask.OpArgN, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: True, False),
    (42, "OP_TFORLOOP", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False, True),
    (43, "OP_SETLIST", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: i.C == 0, False),
    (44, "OP_CLOSURE", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABx,
     lambda i: False, False),
    (45, "OP_VARARG", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False, False),
    (46, "OP_EXTRAARG", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iAx,
     lambda i: False, False),
    # 超长常规定义范围的指令
    (-1, "OP_UNKNOWN", 0, 0, OpArgMask.OpArgNone, OpArgMask.OpArgNone, OpMode.iNone,
     lambda i: False, False),
]
for opdef in OpDefines:
    TOKEN_SET.add(f"<|{opdef[1]}|>")
    TOKEN_SET.add(f"<|Instruction-T={opdef[2]}|>")
    TOKEN_SET.add(f"<|Instruction-A={opdef[3]}|>")
    TOKEN_SET.add(f"<|Instruction-B={OpArgMask.tostr(opdef[4])}|>")
    TOKEN_SET.add(f"<|Instruction-C={OpArgMask.tostr(opdef[5])}|>")
    TOKEN_SET.add(f"<|Instruction-MODE={OpMode.tostr(opdef[6])}|>")

TOKEN_SET.add("<|Instruction|>")
TOKEN_SET.add("<|Instruction-B-ISK=true|>")
TOKEN_SET.add("<|Instruction-B-ISK=false|>")
TOKEN_SET.add("<|Instruction-C-ISK=true|>")
TOKEN_SET.add("<|Instruction-C-ISK=false|>")
TOKEN_SET.add("<|Instruction-INLINE=true|>")
TOKEN_SET.add("<|Instruction-INLINE=false|>")
TOKEN_SET.add("<|Instruction-JUMP=true|>")
TOKEN_SET.add("<|Instruction-JUMP=false|>")
TOKEN_SET.add("<|Instruction-Bx|>")
TOKEN_SET.add("<|/Instruction-Bx|>")
TOKEN_SET.add("<|Instruction-sBx|>")
TOKEN_SET.add("<|/Instruction-sBx|>")
TOKEN_SET.add("<|Instruction-Ax|>")
TOKEN_SET.add("<|/Instruction-Ax|>")
TOKEN_SET.add("<|/Instruction|>")
TOKEN_SET.add("<|Constant|>")
# 存在：nil|true|false
TOKEN_SET.add("<|/Constant|>")
TOKEN_SET.add("<|Upvaldesc|>")
TOKEN_SET.add("<|/Upvaldesc|>")
TOKEN_SET.add("<|Upvaldesc-name|>")
TOKEN_SET.add("<|/Upvaldesc-name|>")
TOKEN_SET.add("<|NULL|>")
TOKEN_SET.add("<|LocVar|>")
TOKEN_SET.add("<|/LocVar|>")
TOKEN_SET.add("<|LocVar-varname|>")
TOKEN_SET.add("<|/LocVar-varname|>")
TOKEN_SET.add("<|LocVar-startpc|>")
TOKEN_SET.add("<|/LocVar-startpc|>")
TOKEN_SET.add("<|LocVar-endpc|>")
TOKEN_SET.add("<|/LocVar-endpc|>")
TOKEN_SET.add("<|LineInfo|>")
TOKEN_SET.add("<|LineInfo-pad|>")
TOKEN_SET.add("<|/LineInfo|>")
TOKEN_SET.add("<|Proto|>")
TOKEN_SET.add("<|/Proto|>")
TOKEN_SET.add("<|Proto-sizeupvalues|>")
TOKEN_SET.add("<|/Proto-sizeupvalues|>")
TOKEN_SET.add("<|Proto-sizek|>")
TOKEN_SET.add("<|/Proto-sizek|>")
TOKEN_SET.add("<|Proto-sizecode|>")
TOKEN_SET.add("<|/Proto-sizecode|>")
TOKEN_SET.add("<|Proto-sizelineinfo|>")
TOKEN_SET.add("<|/Proto-sizelineinfo|>")
TOKEN_SET.add("<|Proto-sizep|>")
TOKEN_SET.add("<|/Proto-sizep|>")
TOKEN_SET.add("<|Proto-sizelocvars|>")
TOKEN_SET.add("<|/Proto-sizelocvars|>")
TOKEN_SET.add("<|Proto-linedefined|>")
TOKEN_SET.add("<|/Proto-linedefined|>")
TOKEN_SET.add("<|Proto-lastlinedefined|>")
TOKEN_SET.add("<|/Proto-lastlinedefined|>")
TOKEN_SET.add("<|Proto-k|>")
TOKEN_SET.add("<|/Proto-k|>")
TOKEN_SET.add("<|Proto-k-idx|>")
TOKEN_SET.add("<|/Proto-k-idx|>")
TOKEN_SET.add("<|Proto-k-idx|>")
TOKEN_SET.add("<|/Proto-k-idx|>")
TOKEN_SET.add("<|Proto-code|>")
TOKEN_SET.add("<|/Proto-code|>")
TOKEN_SET.add("<|Proto-code-idx|>")
TOKEN_SET.add("<|/Proto-code-idx|>")
TOKEN_SET.add("<|Jump-Target|>")
TOKEN_SET.add("<|/Jump-Target|>")
TOKEN_SET.add("<|Proto-lineinfo|>")
TOKEN_SET.add("<|/Proto-lineinfo|>")
TOKEN_SET.add("<|Proto-locvars|>")
TOKEN_SET.add("<|/Proto-locvars|>")
TOKEN_SET.add("<|Proto-locvars-idx|>")
TOKEN_SET.add("<|/Proto-locvars-idx|>")
TOKEN_SET.add("<|Proto-upvalues|>")
TOKEN_SET.add("<|/Proto-upvalues|>")
TOKEN_SET.add("<|Proto-upvalues-idx|>")
TOKEN_SET.add("<|/Proto-upvalues-idx|>")
TOKEN_SET.add("<|Proto-source|>")
TOKEN_SET.add("<|/Proto-source|>")
TOKEN_SET.add("<|Proto-p|>")
TOKEN_SET.add("<|/Proto-p|>")
TOKEN_SET.add("<|Proto-p-idx|>")
TOKEN_SET.add("<|/Proto-p-idx|>")
for i in range(0, 256):
    TOKEN_SET.add(f"<|Instruction-B-K={i}|>")
    TOKEN_SET.add(f"<|Instruction-B-R={i}|>")
    TOKEN_SET.add(f"<|Instruction-C-K={i}|>")
    TOKEN_SET.add(f"<|Instruction-C-R={i}|>")
    TOKEN_SET.add(f"<|Instruction-A={i}|>")
    TOKEN_SET.add(f"\\x{i:02X}")
    TOKEN_SET.add(f"<|Upvaldesc-instack={i}|>")
    TOKEN_SET.add(f"<|Upvaldesc-idx={i}|>")
    TOKEN_SET.add(f"<|Proto-nupvalues={i}|>")
    TOKEN_SET.add(f"<|Proto-numparams={i}|>")
    TOKEN_SET.add(f"<|Proto-is_vararg={i}|>")
    TOKEN_SET.add(f"<|Proto-maxstacksize={i}|>")
for i in range(0, 512):
    TOKEN_SET.add(f"<|Instruction-B={i}|>")
    TOKEN_SET.add(f"<|Instruction-C={i}|>")

    

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("lua-bpe-32k")
with open("Atokens.txt", "w") as f:
    for token in sorted(TOKEN_SET):
        f.write(token + "\n")
special_tokens = {
    "additional_special_tokens": list(sorted(TOKEN_SET))+["<|im_start|>","<|im_end|>"]
}
tokenizer.add_special_tokens(special_tokens)
tokenizer.save_pretrained("lua-bpe-32k-Add")

# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("lua-bpe-32k-Add")
print(len(tokenizer))
print("DEMO:", tokenizer.tokenize("function A= <|NULL|>"))