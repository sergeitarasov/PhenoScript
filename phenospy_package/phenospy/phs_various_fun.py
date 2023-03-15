# -----------------------------------------------------------
# various handy functions to translate phs into xml
#
# (C) 2023 Sergei Tarasov
# email sergei.tarasov@helsinki.fi
# -----------------------------------------------------------
import uuid


# print(uuid_n(6))  # For example, da86ce
def uuid_n(string_length=6):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    # random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]


# --------- auto ids for nodes
# nid = nodeIdGenerator(prefix='xx', starting_id=1)
# nid
# nid.makeId()
class nodeIdGenerator:
    def __init__(self, prefix='', starting_id=1):
        self.current_id = starting_id
        self.out_id = 0
        self.prefix = prefix
    def makeId(self):
        self.out_id = self.current_id
        self.out_id = self.prefix + str(self.out_id)
        self.current_id += 1
        return self.out_id
    def reset(self, prefix='', starting_id=1):
        self.current_id = starting_id
        self.out_id = 0
        self.prefix = prefix
    def __repr__(self):
        return str(self.out_id)


# -----------------------------------------
# This functions check is parentheses are balanced in a string
# from: https://stackoverflow.com/questions/38833819/python-program-to-check-matching-of-simple-parentheses/38834005
# is_balanced(str)
# -----------------------------------------
def is_balanced(expr):
    print('Checking if parentheses are balanced...', flush=True)
    opening = set('([{')
    new = set(')]}{[(')
    match = set([('(', ')'), ('[', ']'), ('{', '}')])
    stack = []
    stackcount = []
    for i, char in enumerate(expr, 1):
        if char not in new:
            continue
        elif char in opening:
            stack.append(char)
            stackcount.append(i)
        else:
            if len(stack) == 0:
                # print(i)
                print('Some parentheses might be disbalanced, see line:', txt[1:i].count('\n') + 1, flush=True)
                return False
            lastOpen = stack.pop()
            lastindex = stackcount.pop()
            if (lastOpen, char) not in match:
                # print (i)
                print('Some parentheses might be disbalanced, see line:', txt[1:i].count('\n') + 1, flush=True)
                return False
    length = len(stack)
    if length != 0:
        elem = stackcount[0]
        print(elem, flush=True)
    return length == 0
