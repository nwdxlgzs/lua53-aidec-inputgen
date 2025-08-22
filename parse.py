import struct


class LuaTValueUtils:
    LUA_TNONE = -1
    LUA_TNIL = 0
    LUA_TBOOLEAN = 1
    LUA_TLIGHTUSERDATA = 2
    LUA_TNUMBER = 3
    LUA_TSTRING = 4
    LUA_TTABLE = 5
    LUA_TFUNCTION = 6
    LUA_TUSERDATA = 7
    LUA_TTHREAD = 8
    LUA_NUMTAGS = 9
    LUA_TPROTO = LUA_NUMTAGS
    LUA_TDEADKEY = LUA_NUMTAGS+1
    LUA_TOTALTAGS = LUA_NUMTAGS+2
    LUA_TLCL = LUA_TFUNCTION | (0 << 4)
    LUA_TLCF = LUA_TFUNCTION | (1 << 4)
    LUA_TCCL = LUA_TFUNCTION | (2 << 4)
    LUA_TSHRSTR = LUA_TSTRING | (0 << 4)
    LUA_TLNGSTR = LUA_TSTRING | (1 << 4)
    LUA_TNUMFLT = LUA_TNUMBER | (0 << 4)
    LUA_TNUMINT = LUA_TNUMBER | (1 << 4)
    BIT_ISCOLLECTABLE = 1 << 6
    LUAI_MAXSHORTLEN = 40

    @staticmethod
    def ctb(t):
        return t | LuaTValueUtils.BIT_ISCOLLECTABLE

    @staticmethod
    def novariant(x):
        return x & 0x0F

    @staticmethod
    def ttype(o):
        return o.rttype() & 0x3F

    @staticmethod
    def ttnov(o):
        return LuaTValueUtils.novariant(o.rttype())

    @staticmethod
    def checktag(o, t):
        return o.rttype() == t

    @staticmethod
    def checktype(o, t):
        return o.ttnov() == t

    @staticmethod
    def ttisnumber(o):
        return LuaTValueUtils.checktype(o, LuaTValueUtils.LUA_TNUMBER)

    @staticmethod
    def ttisfloat(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.LUA_TNUMFLT)

    @staticmethod
    def ttisinteger(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.LUA_TNUMINT)

    @staticmethod
    def ttisnil(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.LUA_TNIL)

    @staticmethod
    def ttisboolean(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.LUA_TBOOLEAN)

    @staticmethod
    def ttislightuserdata(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.LUA_TLIGHTUSERDATA)

    @staticmethod
    def ttisstring(o):
        return LuaTValueUtils.checktype(o, LuaTValueUtils.LUA_TSTRING)

    @staticmethod
    def ttisshrstring(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.ctb(LuaTValueUtils.LUA_TSHRSTR))

    @staticmethod
    def ttislngstring(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.ctb(LuaTValueUtils.LUA_TLNGSTR))

    @staticmethod
    def ttistable(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.ctb(LuaTValueUtils.LUA_TTABLE))

    @staticmethod
    def ttisfunction(o):
        return LuaTValueUtils.checktype(o, LuaTValueUtils.LUA_TFUNCTION)

    @staticmethod
    def ttisclosure(o):
        return (o.rttype() & 0x1F) == LuaTValueUtils.LUA_TFUNCTION

    @staticmethod
    def ttisCclosure(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.ctb(LuaTValueUtils.LUA_TCCL))

    @staticmethod
    def ttisLclosure(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.ctb(LuaTValueUtils.LUA_TLCL))

    @staticmethod
    def ttislcf(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.LUA_TLCF)

    @staticmethod
    def ttisfulluserdata(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.ctb(LuaTValueUtils.LUA_TUSERDATA))

    @staticmethod
    def ttisthread(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.ctb(LuaTValueUtils.LUA_TTHREAD))

    @staticmethod
    def ttisdeadkey(o):
        return LuaTValueUtils.checktag(o, LuaTValueUtils.LUA_TDEADKEY)

    @staticmethod
    def l_isfalse(o):
        return o.ttisnil() or (o.ttisboolean() and o.bvalue(asBool=False) == 0)

    @staticmethod
    def iscollectable(o):
        return o.rttype() & LuaTValueUtils.BIT_ISCOLLECTABLE

    @staticmethod
    def setfltvalue(obj, x):
        obj.val_(x)
        obj.settt_(LuaTValueUtils.LUA_TNUMFLT)

    @staticmethod
    def chgfltvalue(obj, x):
        if obj.ttisfloat():
            obj.val_(x)

    @staticmethod
    def setivalue(obj, x):
        obj.val_(x)
        obj.settt_(LuaTValueUtils.LUA_TNUMINT)

    @staticmethod
    def chgivalue(obj, x):
        if obj.ttisinteger():
            obj.val_(x)

    @staticmethod
    def setnilvalue(obj):
        obj.settt_(LuaTValueUtils.LUA_TNIL)

    @staticmethod
    def setbvalue(obj, x):
        obj.settt_(LuaTValueUtils.LUA_TBOOLEAN)
        if type(x) == bool:
            x = 1 if x else 0
        obj.val_(x)

    @staticmethod
    def setsvalue(obj, x):
        if len(x.encode('utf-8')) < LuaTValueUtils.LUAI_MAXSHORTLEN:
            string_type = LuaTValueUtils.LUA_TSHRSTR
        else:
            string_type = LuaTValueUtils.LUA_TLNGSTR
        obj.setval_(x)
        obj.settt_(LuaTValueUtils.ctb(string_type))

    @staticmethod
    def setdeadvalue(obj):
        obj.settt_(LuaTValueUtils.LUA_TDEADKEY)

    @staticmethod
    def ivalue(o, check=False):
        if check and not o.ttisinteger():
            raise Exception("<ivalue> ttisinteger => False")
        return o.val_()

    @staticmethod
    def fltvalue(o, check=False):
        if check and not o.ttisfloat():
            raise Exception("<fltvalue> ttisfloat => False")
        return o.val_()

    @staticmethod
    def nvalue(o, check=False):
        if check and not o.ttisnumber():
            raise Exception("<nvalue> ttisnumber => False")
        if o.ttisinteger():
            return o.ivalue()
        else:
            return o.fltvalue()

    @staticmethod
    def bvalue(o, check=False, asBool=True):
        if check and not o.ttisboolean():
            raise Exception("<bvalue> ttisboolean => False")
        val = o.val_()
        if asBool:
            return val != 0
        return val

    @staticmethod
    def svalue(o, check=False):
        if check and not o.ttisstring():
            raise Exception("<svalue> ttisstring => False")
        return o.val_()


class InstructionUtils:
    SIZE_C = 9
    SIZE_B = 9
    SIZE_Bx = (SIZE_C + SIZE_B)
    SIZE_A = 8
    SIZE_Ax = (SIZE_Bx + SIZE_A)
    SIZE_OP = 6
    POS_OP = 0
    POS_A = (POS_OP + SIZE_OP)
    POS_C = (POS_A + SIZE_A)
    POS_B = (POS_C + SIZE_C)
    POS_Bx = POS_C
    POS_Ax = POS_A
    MAXARG_Bx = (1 << SIZE_Bx)-1
    MAXARG_sBx = MAXARG_Bx >> 1
    MAXARG_Ax = (1 << SIZE_Ax)-1
    MAXARG_A = (1 << SIZE_A)-1
    MAXARG_B = (1 << SIZE_B)-1
    MAXARG_C = (1 << SIZE_C)-1
    BITRK = 1 << (SIZE_B - 1)
    NO_REG = MAXARG_A
    LFIELDS_PER_FLUSH = 50

    @staticmethod
    def ISK(x):
        return x & InstructionUtils.BITRK

    @staticmethod
    def INDEXK(r):
        return r & ~InstructionUtils.BITRK

    @staticmethod
    def RKASK(x):
        return x | InstructionUtils.BITRK

    @staticmethod
    def MASK1(n, p):
        return (~((~0) << n)) << p

    @staticmethod
    def MASK0(n, p):
        return ~InstructionUtils.MASK1(n, p)

    @staticmethod
    def GET_OPCODE(i):
        return (i >> InstructionUtils.POS_OP) & InstructionUtils.MASK1(InstructionUtils.SIZE_OP, 0)

    @staticmethod
    def SET_OPCODE(i, o):
        return (i & InstructionUtils.MASK0(InstructionUtils.SIZE_OP, InstructionUtils.POS_OP)) | ((o << InstructionUtils.POS_OP) & InstructionUtils.MASK1(InstructionUtils.SIZE_OP, InstructionUtils.POS_OP))

    @staticmethod
    def getarg(i, pos, size):
        return (i >> pos) & InstructionUtils.MASK1(size, pos)

    @staticmethod
    def setarg(i, v, pos, size):
        return (i & InstructionUtils.MASK0(size, pos)) | ((v << pos) & InstructionUtils.MASK1(size, pos))

    @staticmethod
    def GETARG_A(i):
        return InstructionUtils.getarg(i, InstructionUtils.POS_A, InstructionUtils.SIZE_A)

    @staticmethod
    def SETARG_A(i, v):
        return InstructionUtils.setarg(i, v, InstructionUtils.POS_A, InstructionUtils.SIZE_A)

    @staticmethod
    def GETARG_B(i):
        return InstructionUtils.getarg(i, InstructionUtils.POS_B, InstructionUtils.SIZE_B)

    @staticmethod
    def SETARG_B(i, v):
        return InstructionUtils.setarg(i, v, InstructionUtils.POS_B, InstructionUtils.SIZE_B)

    @staticmethod
    def GETARG_C(i):
        return InstructionUtils.getarg(i, InstructionUtils.POS_C, InstructionUtils.SIZE_C)

    @staticmethod
    def SETARG_C(i, v):
        return InstructionUtils.setarg(i, v, InstructionUtils.POS_C, InstructionUtils.SIZE_C)

    @staticmethod
    def GETARG_Bx(i):
        return InstructionUtils.getarg(i, InstructionUtils.POS_Bx, InstructionUtils.SIZE_Bx)

    @staticmethod
    def SETARG_Bx(i, v):
        return InstructionUtils.setarg(i, v, InstructionUtils.POS_Bx, InstructionUtils.SIZE_Bx)

    @staticmethod
    def GETARG_Ax(i):
        return InstructionUtils.getarg(i, InstructionUtils.POS_Ax, InstructionUtils.SIZE_Ax)

    @staticmethod
    def SETARG_Ax(i, v):
        return InstructionUtils.setarg(i, v, InstructionUtils.POS_Ax, InstructionUtils.SIZE_Ax)

    @staticmethod
    def GETARG_sBx(i):
        return InstructionUtils.GETARG_Bx(i)-InstructionUtils.MAXARG_sBx

    @staticmethod
    def SETARG_sBx(i, v):
        return InstructionUtils.SETARG_Bx(i, v+InstructionUtils.MAXARG_sBx)

    @staticmethod
    def CREATE_ABC(o, a, b, c):
        return (o << InstructionUtils.POS_OP) + (a << InstructionUtils.POS_A) + (b << InstructionUtils.POS_B) + (c << InstructionUtils.POS_C)

    @staticmethod
    def CREATE_ABx(o, a, bc):
        return (o << InstructionUtils.POS_OP) + (a << InstructionUtils.POS_A) + (bc << InstructionUtils.POS_Bx)

    @staticmethod
    def CREATE_Ax(o, a):
        return (o << InstructionUtils.POS_OP) + (a << InstructionUtils.POS_Ax)

    @staticmethod
    def CREATE_sBx(o, a, sbx):
        i = InstructionUtils.CREATE_ABx(o, a, 0)
        return InstructionUtils.SETARG_sBx(i, sbx)


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


class LuaCType:
    luai_ctype_ = [0x00,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x00,  0x08,  0x08,  0x08,  0x08,  0x08,  0x00,  0x00,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x0c,  0x04,  0x04,  0x04,  0x04,  0x04,  0x04,  0x04,
                   0x04,  0x04,  0x04,  0x04,  0x04,  0x04,  0x04,  0x04,
                   0x16,  0x16,  0x16,  0x16,  0x16,  0x16,  0x16,  0x16,
                   0x16,  0x16,  0x04,  0x04,  0x04,  0x04,  0x04,  0x04,
                   0x04,  0x15,  0x15,  0x15,  0x15,  0x15,  0x15,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x04,  0x04,  0x04,  0x04,  0x05,
                   0x04,  0x15,  0x15,  0x15,  0x15,  0x15,  0x15,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x04,  0x04,  0x04,  0x04,  0x00,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,  0x05,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
                   ]
    ALPHABIT = 0
    DIGITBIT = 1
    PRINTBIT = 2
    SPACEBIT = 3
    XDIGITBIT = 4

    @staticmethod
    def MASK(B):
        return 1 << B

    @staticmethod
    def testprop(c, p):
        return LuaCType.luai_ctype_[c+1] & p

    @staticmethod
    def lislalpha(c):
        return LuaCType.testprop(c, LuaCType.MASK(LuaCType.ALPHABIT))

    @staticmethod
    def lislalnum(c):
        return LuaCType.testprop(c, LuaCType.MASK(LuaCType.ALPHABIT) | LuaCType.MASK(LuaCType.DIGITBIT))

    @staticmethod
    def lisdigit(c):
        return LuaCType.testprop(c, LuaCType.MASK(LuaCType.DIGITBIT))

    @staticmethod
    def lisspace(c):
        return LuaCType.testprop(c, LuaCType.MASK(LuaCType.SPACEBIT))

    @staticmethod
    def lisprint(c):
        return LuaCType.testprop(c, LuaCType.MASK(LuaCType.PRINTBIT))

    @staticmethod
    def lisxdigit(c):
        return LuaCType.testprop(c, LuaCType.MASK(LuaCType.XDIGITBIT))


class LuaTValue:
    def __init__(self, value_=None, tt_=None):
        self.value_ = value_
        self.tt_ = tt_

    def val_(self):
        return self.value_

    def setval_(self, value_=None):
        self.value_ = value_

    def tt_(self):
        return self.tt_

    def settt_(self, tt_=None):
        self.tt_ = tt_

    def rttype(self):
        return self.tt_

    def ctb(self, setfield=False):
        _ = LuaTValueUtils.ctb(self)
        if setfield:
            self.tt_ = _
        return _

    def svalue(self, check=False):
        return LuaTValueUtils.svalue(self, check)

    def ivalue(self, check=False):
        return LuaTValueUtils.ivalue(self, check)

    def fltvalue(self, check=False):
        return LuaTValueUtils.fltvalue(self, check)

    def nvalue(self, check=False):
        return LuaTValueUtils.nvalue(self, check)

    def bvalue(self, check=False, asBool=True):
        return LuaTValueUtils.bvalue(self, check, asBool)

    def setfltvalue(self, x):
        return LuaTValueUtils.setfltvalue(self, x)

    def chgfltvalue(self, x):
        return LuaTValueUtils.chgfltvalue(self, x)

    def setivalue(self, x):
        return LuaTValueUtils.setivalue(self, x)

    def chgivalue(self, x):
        return LuaTValueUtils.chgivalue(self, x)

    def setnilvalue(self):
        return LuaTValueUtils.setnilvalue(self)

    def setbvalue(self, x):
        return LuaTValueUtils.setbvalue(self, x)

    def setsvalue(self, x):
        return LuaTValueUtils.setsvalue(self, x)

    def setdeadvalue(self):
        return LuaTValueUtils.setdeadvalue(self)

    def novariant(self):
        return LuaTValueUtils.novariant(self)

    def ttype(self):
        return LuaTValueUtils.ttype(self)

    def ttnov(self):
        return LuaTValueUtils.ttnov(self)

    def checktag(self, t):
        return LuaTValueUtils.checktag(self, t)

    def checktype(self, t):
        return LuaTValueUtils.checktype(self, t)

    def ttisnumber(self):
        return LuaTValueUtils.ttisnumber(self)

    def ttisfloat(self):
        return LuaTValueUtils.ttisfloat(self)

    def ttisinteger(self):
        return LuaTValueUtils.ttisinteger(self)

    def ttisnil(self):
        return LuaTValueUtils.ttisnil(self)

    def ttisboolean(self):
        return LuaTValueUtils.ttisboolean(self)

    def ttislightuserdata(self):
        return LuaTValueUtils.ttislightuserdata(self)

    def ttisstring(self):
        return LuaTValueUtils.ttisstring(self)

    def ttislngstring(self):
        return LuaTValueUtils.ttislngstring(self)

    def ttistable(self):
        return LuaTValueUtils.ttistable(self)

    def ttisfunction(self):
        return LuaTValueUtils.ttisfunction(self)

    def ttisclosure(self):
        return LuaTValueUtils.ttisclosure(self)

    def ttisCclosure(self):
        return LuaTValueUtils.ttisCclosure(self)

    def ttisLclosure(self):
        return LuaTValueUtils.ttisLclosure(self)

    def ttislcf(self):
        return LuaTValueUtils.ttislcf(self)

    def ttisfulluserdata(self):
        return LuaTValueUtils.ttisfulluserdata(self)

    def ttisthread(self):
        return LuaTValueUtils.ttisthread(self)

    def ttisdeadkey(self):
        return LuaTValueUtils.ttisdeadkey(self)

    def l_isfalse(self):
        return LuaTValueUtils.l_isfalse(self)

    def iscollectable(self):
        return LuaTValueUtils.iscollectable(self)


OpDefines = [
    # op-code | op-name | T | A | B | C | mode | inline
    (0, "OP_MOVE", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (1, "OP_LOADK", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgN, OpMode.iABx,
     lambda i: False),
    (2, "OP_LOADKX", 0, 1, OpArgMask.OpArgN, OpArgMask.OpArgN, OpMode.iABx,
     lambda i: True),
    (3, "OP_LOADBOOL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: i.C != 0),
    (4, "OP_LOADNIL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (5, "OP_GETUPVAL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (6, "OP_GETTABUP", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (7, "OP_GETTABLE", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (8, "OP_SETTABUP", 0, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (9, "OP_SETUPVAL", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (10, "OP_SETTABLE", 0, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (11, "OP_NEWTABLE", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: False),
    (12, "OP_SELF", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (13, "OP_ADD", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (14, "OP_SUB", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (15, "OP_MUL", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (16, "OP_MOD", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (17, "OP_POW", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (18, "OP_DIV", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (19, "OP_IDIV", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (20, "OP_BAND", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (21, "OP_BOR", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (22, "OP_BXOR", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (23, "OP_SHL", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (24, "OP_SHR", 0, 1, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: False),
    (25, "OP_UNM", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (26, "OP_BNOT", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (27, "OP_NOT", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (28, "OP_LEN", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (29, "OP_CONCAT", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgR, OpMode.iABC,
     lambda i: False),
    (30, "OP_JMP", 0, 0, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False),
    (31, "OP_EQ", 1, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: True),
    (32, "OP_LT", 1, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: True),
    (33, "OP_LE", 1, 0, OpArgMask.OpArgK, OpArgMask.OpArgK, OpMode.iABC,
     lambda i: True),
    (34, "OP_TEST", 1, 0, OpArgMask.OpArgN, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: True),
    (35, "OP_TESTSET", 1, 1, OpArgMask.OpArgR, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: True),
    (36, "OP_CALL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: False),
    (37, "OP_TAILCALL", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: False),
    (38, "OP_RETURN", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (39, "OP_FORLOOP", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False),
    (40, "OP_FORPREP", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False),
    (41, "OP_TFORCALL", 0, 0, OpArgMask.OpArgN, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: True),
    (42, "OP_TFORLOOP", 0, 1, OpArgMask.OpArgR, OpArgMask.OpArgN, OpMode.iAsBx,
     lambda i: False),
    (43, "OP_SETLIST", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iABC,
     lambda i: i.C == 0),
    (44, "OP_CLOSURE", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABx,
     lambda i: False),
    (45, "OP_VARARG", 0, 1, OpArgMask.OpArgU, OpArgMask.OpArgN, OpMode.iABC,
     lambda i: False),
    (46, "OP_EXTRAARG", 0, 0, OpArgMask.OpArgU, OpArgMask.OpArgU, OpMode.iAx,
     lambda i: False),
    # 超长常规定义范围的指令
    (-1, "OP_UNKNOWN", 0, 0, OpArgMask.OpArgNone, OpArgMask.OpArgNone, OpMode.iNone,
     lambda i: False),
]


class Instruction:
    def __init__(self, instruction):
        self.instruction = instruction
        self.opcode = InstructionUtils.GET_OPCODE(self.instruction)
        self.opdef = OpDefines[-1]
        for op_def in OpDefines:
            if op_def[0] == self.opcode:
                self.opdef = op_def
                break
        self.opmode = self.opdef[6]
        self.A = InstructionUtils.GETARG_A(self.instruction)
        self.B = InstructionUtils.GETARG_B(self.instruction)
        self.C = InstructionUtils.GETARG_C(self.instruction)
        self.Bx = InstructionUtils.GETARG_Bx(self.instruction)
        self.sBx = InstructionUtils.GETARG_sBx(self.instruction)
        self.Ax = InstructionUtils.GETARG_Ax(self.instruction)

    def __str__(self):
        buff = ["<|Instruction|>"]
        buff.append(f"<|{self.opdef[1]}|>")  # op-name
        buff.append(f"<|Instruction-T={self.opdef[2]}|>")  # T
        buff.append(f"<|Instruction-A={self.opdef[3]}|>")  # A
        buff.append(f"<|Instruction-B={OpArgMask.tostr(self.opdef[4])}|>")  # B
        buff.append(
            f"<|Instruction-B-ISK={'true' if InstructionUtils.ISK(self.B) else 'false'}|>")  # ISK(B)
        # INDEXK(B)
        buff.append(f"<|Instruction-B-K={InstructionUtils.INDEXK(self.B)}|>")
        buff.append(f"<|Instruction-B-R={self.B}|>")  # REG(B)
        buff.append(f"<|Instruction-C={OpArgMask.tostr(self.opdef[5])}|>")  # C
        buff.append(
            f"<|Instruction-C-ISK={'true' if InstructionUtils.ISK(self.C) else 'false'}|>")  # ISK(C)
        # INDEXK(C)
        buff.append(f"<|Instruction-C-K={InstructionUtils.INDEXK(self.C)}|>")
        buff.append(f"<|Instruction-C-R={self.C}|>")  # REG(C)
        buff.append(
            f"<|Instruction-MODE={OpMode.tostr(self.opmode)}|>")  # mode
        buff.append(f"<|Instruction-INLINE={self.opdef[7](self)}|>")  # inline
        buff.append(f"<|Instruction-A={self.A}|>")
        buff.append(f"<|Instruction-B={self.B}|>")
        buff.append(f"<|Instruction-C={self.C}|>")
        buff.append("<|Instruction-Bx|>")
        buff.append(f"{self.Bx}")
        buff.append("<|/Instruction-Bx|>")
        buff.append("<|Instruction-sBx|>")
        buff.append(f"{self.sBx}")
        buff.append("<|/Instruction-sBx|>")
        buff.append("<|Instruction-Ax|>")
        buff.append(f"{self.Ax}")
        buff.append("<|/Instruction-Ax|>")
        buff.append("<|/Instruction|>")
        return ''.join(buff)


class LuaConstant:

    escapes_MAP = {
        '\a': '\\a',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\v': '\\v',
        '\\': '\\\\',
        '"': '\\"',
        '\'': '\\\'',
    }

    @staticmethod
    def escape(s):
        buff = bytearray(s, encoding='utf-8')
        dst = []
        for ch in buff:
            # 0x22 => "
            if ch != 0x22 and LuaCType.lisprint(ch):  # 一般字母符号允许保持原样
                dst.append(chr(ch))
            elif LuaConstant.escapes_MAP[ch] is not None:  # 转义字符
                dst.append(LuaConstant.escapes_MAP[ch])
            else:  # 统一用\xXX编码
                dst.append(f"\\x{ch:02X}")
        return ''.join(dst)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        t = self.value.ttnov()
        if t == LuaTValueUtils.LUA_TNIL:
            return "<|Constant|>nil<|/Constant|>"
        elif t == LuaTValueUtils.LUA_TBOOLEAN:
            return "<|Constant|>true<|/Constant|>" if self.value.bvalue(asBool=True) else "<|Constant|>false<|/Constant|>"
        elif t == LuaTValueUtils.LUA_TNUMBER:
            return "<|Constant|>"+str(self.value.nvalue())+"<|/Constant|>"
        elif t == LuaTValueUtils.LUA_TSTRING:
            return f'<|Constant|>"{LuaConstant.escape(self.value.svalue())}"<|/Constant|>'
        else:
            return "<|Constant|>nil<|/Constant|>"


class UpvalDesc:
    def __init__(self, name, instack, idx):
        self.name = name
        self.instack = instack  # lu_byte
        self.idx = idx  # lu_byte

    def updateName(self, name):
        self.name = name

    def __str__(self):
        buff = ["<|Upvaldesc|>", "<|Upvaldesc-name|>"]
        if self.name is None:
            buff.append("<|NULL|>")
        else:
            buff.append(self.name.svalue())
        buff.append("<|/Upvaldesc-name|>")
        buff.append(f"<|Upvaldesc-instack={self.instack}|>")
        buff.append(f"<|Upvaldesc-idx={self.idx}|>")
        buff.append("<|/Upvaldesc|>")
        return ''.join(buff)


class LocVar:
    def __init__(self, varname, startpc, endpc):
        self.varname = varname
        self.startpc = startpc  # int
        self.endpc = endpc  # int

    def __str__(self):
        buff = ["<|LocVar|>", "<|LocVar-varname|>"]
        if self.varname is None:
            buff.append("<|NULL|>")
        else:
            buff.append(self.varname.svalue())
        buff.append("<|/LocVar-varname|>")
        buff.append("<|LocVar-startpc|>")
        buff.append(str(self.startpc))
        buff.append("<|/LocVar-startpc|>")
        buff.append("<|LocVar-endpc|>")
        buff.append(str(self.endpc))
        buff.append("<|/LocVar-endpc|>")
        buff.append("<|/LocVar|>")
        return ''.join(buff)


class LineInfo:
    def __init__(self, lines=[]):
        self.lines = lines

    def add(self, line):
        self.lines.append(line)

    def __str__(self):
        buff = ["<|LineInfo|>"]
        for line in self.lines:
            buff.append(str(line))
            buff.append("<|LineInfo-pad|>")
        buff.append("<|/LineInfo|>")
        return ''.join(buff)

    def __getitem__(self, index):
        return self.lines[index]

    def __len__(self):
        return len(self.lines)

    def __iter__(self):
        return iter(self.lines)

    def __setitem__(self, index, value):
        self.lines[index] = value


class Proto:
    def __init__(self):
        self.numparams = 0  # lu_byte
        self.is_vararg = 0  # lu_byte
        self.maxstacksize = 0  # lu_byte
        self.sizeupvalues = 0  # int
        self.sizek = 0  # int
        self.sizecode = 0  # int
        self.sizelineinfo = 0  # int
        self.sizep = 0  # int
        self.sizelocvars = 0  # int
        self.linedefined = 0  # int
        self.lastlinedefined = 0  # int
        self.k = []  # LuaTValue[]
        self.code = []  # Instruction[]
        self.lineinfo = LineInfo()
        self.locvars = []  # LocVar[]
        self.upvalues = []  # UpValue[]
        self.source = None
        self.p = []  # Proto[]
        self.nupvalues = -1  # -1 == None

    def set_nupvalues(self, nupvalues):
        self.nupvalues = nupvalues

    def __str__(self):
        result = ["<|Proto|>"]
        if self.nupvalues >= 0:
            result.append(f"<|Proto-nupvalues={self.nupvalues}|>")
        result.append(f"<|Proto-numparams={self.numparams}|>")
        result.append(f"<|Proto-is_vararg={self.is_vararg}|>")
        result.append(f"<|Proto-maxstacksize={self.maxstacksize}|>")
        result.append("<|Proto-sizeupvalues|>")
        result.append(str(self.sizeupvalues))
        result.append("<|/Proto-sizeupvalues|>")
        result.append("<|Proto-sizek|>")
        result.append(str(self.sizek))
        result.append("<|/Proto-sizek|>")
        result.append("<|Proto-sizecode|>")
        result.append(str(self.sizecode))
        result.append("<|/Proto-sizecode|>")
        result.append("<|Proto-sizelineinfo|>")
        result.append(str(self.sizelineinfo))
        result.append("<|/Proto-sizelineinfo|>")
        result.append("<|Proto-sizep|>")
        result.append(str(self.sizep))
        result.append("<|/Proto-sizep|>")
        result.append("<|Proto-sizelocvars|>")
        result.append(str(self.sizelocvars))
        result.append("<|/Proto-sizelocvars|>")
        result.append("<|Proto-linedefined|>")
        result.append(str(self.linedefined))
        result.append("<|/Proto-linedefined|>")
        result.append("<|Proto-lastlinedefined|>")
        result.append(str(self.lastlinedefined))
        result.append("<|/Proto-lastlinedefined|>")
        result.append("<|Proto-k|>")
        for idx, k in enumerate(self.k):
            result.append("<|Proto-k-idx|>")
            result.append(str(idx))
            result.append("<|/Proto-k-idx|>")
            result.append(str(k))
        result.append("<|/Proto-k|>")
        result.append("<|Proto-code|>")
        for idx, code in enumerate(self.code):
            result.append("<|Proto-code-idx|>")
            result.append(str(idx))
            result.append("<|/Proto-code-idx|>")
            result.append(str(code))
        result.append("<|/Proto-code|>")
        result.append("<|Proto-lineinfo|>")
        result.append(str(self.lineinfo))
        result.append("<|/Proto-lineinfo|>")
        result.append("<|Proto-locvars|>")
        for idx, locvar in enumerate(self.locvars):
            result.append("<|Proto-locvars-idx|>")
            result.append(str(idx))
            result.append("<|/Proto-locvars-idx|>")
            result.append(str(locvar))
        result.append("<|/Proto-locvars|>")
        result.append("<|Proto-upvalues|>")
        for idx, upvalue in enumerate(self.upvalues):
            result.append("<|Proto-upvalues-idx|>")
            result.append(str(idx))
            result.append("<|/Proto-upvalues-idx|>")
            result.append(str(upvalue))
        result.append("<|/Proto-upvalues|>")
        result.append("<|Proto-source|>")
        if self.source is None:
            result.append("<|NULL|>")
        else:
            result.append(self.source.svalue())
        result.append("<|/Proto-source|>")
        result.append("<|Proto-p|>")
        for idx, p in enumerate(self.p):
            result.append("<|Proto-p-idx|>")
            result.append(str(idx))
            result.append("<|/Proto-p-idx|>")
            result.append(str(p))
        result.append("<|/Proto-p|>")
        result.append("<|/Proto|>")
        return ''.join(result)


class LuaBytecodeParser:
    LUA_SIGNATURE = b'\x1bLua'
    LUAC_VERSION = 0x53  # Lua 5.3
    LUAC_FORMAT = 0
    LUAC_DATA = b'\x19\x93\r\n\x1a\n'
    LUAC_INT = 0x5678
    LUAC_NUM = 370.5

    def __init__(self, data, little_endian=True):
        self.data = data
        self.pos = 0
        self.endian = '<' if little_endian else '>'

    def read_byte(self):
        if self.pos >= len(self.data):
            raise EOFError("Unexpected end of data")
        result = self.data[self.pos]
        self.pos += 1
        return result

    def read_uint(self, size=None):
        if size is None:
            size = self.int_size if self.int_size is not None else 4
        if self.pos + size > len(self.data):
            raise EOFError("Unexpected end of data")
        result = int.from_bytes(
            self.data[self.pos:self.pos+size], byteorder='little' if self.endian == '<' else 'big')
        self.pos += size
        return result

    def read_int(self, size=None):
        if size is None:
            size = self.int_size if self.int_size is not None else 4
        if self.pos + size > len(self.data):
            raise EOFError("Unexpected end of data")
        result = int.from_bytes(
            self.data[self.pos:self.pos+size], byteorder='little' if self.endian == '<' else 'big', signed=True)
        self.pos += size
        return result

    def read_size_t(self, size=None):
        if size is None:
            size = self.size_t_size if self.size_t_size is not None else 4
        return self.read_int(size)

    def read_instruction(self, size=None):
        if size is None:
            size = self.instruction_size if self.instruction_size is not None else 4
        instruction = self.read_uint(size)
        return Instruction(instruction)

    def read_luaint(self, size=None):
        if size is None:
            size = self.lua_int_size if self.lua_int_size is not None else 8
        return self.read_int(size)

    def read_luaflt(self, size=None):
        if size is None:
            size = self.lua_flt_size if self.lua_flt_size is not None else 8
        if self.pos + size > len(self.data):
            raise EOFError("Unexpected end of data")
        # 根据大小读取浮点数，通常为8字节(double)或4字节(float)
        if size == 8:
            # 8字节double类型
            result = struct.unpack(
                self.endian+'d', self.data[self.pos:self.pos+size])[0]
        elif size == 4:
            # 4字节float类型
            result = struct.unpack(
                self.endian+'f', self.data[self.pos:self.pos+size])[0]
        else:
            # 其他大小默认使用double解析
            result = struct.unpack(
                self.endian+'d', self.data[self.pos:self.pos+size])[0]
        self.pos += size
        return result

    def read_string(self):
        size = self.read_byte() & 0xFF
        if size == 0xFF:
            size = self.read_size_t()
        if size == 0:
            return None
        size -= 1
        isshort = size <= LuaTValueUtils.LUAI_MAXSHORTLEN
        if self.pos + size > len(self.data):
            raise EOFError("Unexpected end of data")
        result = self.data[self.pos:self.pos+size].decode('utf-8')
        self.pos += size
        return LuaTValue(value_=result, tt_=LuaTValueUtils.LUA_TSHRSTR if isshort else LuaTValueUtils.LUA_TLNGSTR)

    def check_header(self):
        if len(self.data) < 33:
            raise EOFError("Very short data")
        # 检查签名
        signature = self.data[self.pos:self.pos+4]
        self.pos += 4
        if signature != self.LUA_SIGNATURE:
            raise ValueError("Not a Lua bytecode file")

        # 检查版本
        version = self.read_byte() & 0xff
        if version != self.LUAC_VERSION:
            raise ValueError(f"Unsupported Lua version: {version}")

        # 检查格式
        format_version = self.read_byte() & 0xff
        if format_version != self.LUAC_FORMAT:
            raise ValueError(f"Unsupported format version: {format_version}")

        # 检查 luac 数据
        luac_data = self.data[self.pos:self.pos+6]
        self.pos += 6
        if luac_data != self.LUAC_DATA:
            raise ValueError("Corrupted chunk")

        # 读取各种大小信息
        self.int_size = self.read_byte() & 0xff
        self.size_t_size = self.read_byte() & 0xff
        self.instruction_size = self.read_byte() & 0xff
        self.lua_int_size = self.read_byte() & 0xff
        self.lua_flt_size = self.read_byte() & 0xff
        ckint = self.read_luaint()
        if ckint != self.LUAC_INT:
            raise ValueError("endianness mismatch in")
        ckflt = self.read_luaflt()
        if ckflt != self.LUAC_NUM:
            raise ValueError("float format mismatch in")

    def load_constant(self, proto):
        n = self.read_int()
        proto.sizek = n
        for i in range(n):
            t = self.read_byte() & 0xff
            if t == LuaTValueUtils.LUA_TNIL:
                proto.k.append(LuaConstant(
                    LuaTValue(value_=None, tt_=LuaTValueUtils.LUA_TNIL)))
            elif t == LuaTValueUtils.LUA_TBOOLEAN:
                b = self.read_byte() & 0xff
                proto.k.append(LuaConstant(
                    LuaTValue(value_=True if b != 0 else False, tt_=LuaTValueUtils.LUA_TBOOLEAN)))
            elif t == LuaTValueUtils.LUA_TNUMFLT:
                proto.k.append(LuaConstant(
                    LuaTValue(value_=self.read_luaint(), tt_=LuaTValueUtils.LUA_TNUMFLT)))
            elif t == LuaTValueUtils.LUA_TNUMINT:
                proto.k.append(LuaConstant(
                    LuaTValue(value_=self.read_luaflt(), tt_=LuaTValueUtils.LUA_TNUMINT)))
            elif t == LuaTValueUtils.LUA_TSHRSTR or t == LuaTValueUtils.LUA_TLNGSTR:
                proto.k.append(LuaConstant(self.read_string()))
            else:
                proto.k.append(LuaConstant(
                    LuaTValue(value_=None, tt_=LuaTValueUtils.LUA_TNIL)))

    def load_upvalues(self, proto):
        n = self.read_int()
        proto.sizeupvalues = n
        for _ in range(n):
            instack = self.read_byte() & 0xFF
            idx = self.read_byte() & 0xFF
            proto.upvalues.append(
                UpvalDesc(name=None, instack=instack, idx=idx))

    def read_protos(self, proto):
        n = self.read_int()
        proto.sizep = n
        for _ in range(n):
            newproto = self.load_function(proto.source)
            proto.p.append(newproto)

    def load_code(self, proto):
        n = self.read_int()
        proto.sizep = n
        for _ in range(n):
            proto.code.append(self.read_instruction())

    def read_debug(self, proto):
        n = self.read_int()
        proto.sizelineinfo = n
        for _ in range(n):
            line = self.read_int()
            proto.lineinfo.add(line)
        n = self.read_int()
        proto.sizelocvars = n
        for _ in range(n):
            varname = self.read_string()
            startpc = self.read_int()
            endpc = self.read_int()
            proto.locvars.append(
                LocVar(varname=varname, startpc=startpc, endpc=endpc))
        n = self.read_int()
        for i in range(n):
            name = self.read_string()
            proto.upvalues[i].updateName(name)

    def load_function(self, parent_source=None):
        proto = Proto()
        # 读取源文件名
        proto.source = self.read_string()
        if proto.source is None and parent_source:
            proto.source = parent_source
        # 读取行号信息
        proto.linedefined = self.read_int()
        proto.lastlinedefined = self.read_int()
        # 读取函数参数信息
        proto.numparams = self.read_byte() & 0xFF
        proto.is_vararg = self.read_byte() & 0xFF
        proto.maxstacksize = self.read_byte() & 0xFF
        # 读取指令
        self.load_code(proto)
        # 读取常量
        self.load_constant(proto)
        # 读取上值
        self.load_upvalues(proto)
        # 读取子函数
        self.read_protos(proto)
        # 读取调试信息
        self.read_debug(proto)
        return proto

    def parse(self):
        # 检查头部
        self.check_header()
        # 读取主函数
        self.nupvalues = self.read_byte() & 0xff
        main_proto = self.load_function()
        main_proto.set_nupvalues(self.nupvalues)
        return main_proto


def main():

    filename = "luac.out"
    try:
        with open(filename, 'rb') as f:
            data = f.read()

        parser = LuaBytecodeParser(data)
        proto = parser.parse()

        print("Lua 5.3 Bytecode Analysis:")
        print("=" * 50)
        print(proto)
        with open("luac.lasm", 'w', encoding='utf-8') as f:
            f.write(str(proto))

    except Exception as e:
        print(f"Error parsing bytecode: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
