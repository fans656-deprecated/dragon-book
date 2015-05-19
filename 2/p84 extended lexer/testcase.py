testcases = [

("Adjacent C++ style comments",
'''\
// foo
// bar\
'''),

("Adjacent C style comments",
'''\
/* foo *//* bar */\
'''),

("Nonterminated comments",
'''\
/*
'''),

("Nonterminated comments",
'''\
/* foo *\
'''),

("Everything",
'''
// c++ style comment
a = b + c;
d = 1 / 234 * foo - 2. + .2 + 2.2;
if what /* c style comment */what;
for a1 == b2 a1 != b2;
while a1 < b2 a1 > b2;
a1 <= b2;
a1 >= b2;
'''),

("id",
'''
foo
'''),

("Nonterminated comment",
'''\
// foo
/*hello*\
'''),

("2 id",
'''\
a b
'''),

("int float",
'''\
1. .1 1.2 12.34
1 12 123
'''),

("id = floats, ints",
'''\
a = 1. .1 1.2 12.34;
1 12 123
'''
),

("logical operators",
'''\
<<=!=>>==
'''
),

("",
'''\
'''
),

]
