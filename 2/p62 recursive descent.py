# page [62() - 85]
grammarText = '''
stmt -> expr ;
      | if ( expr ) stmt
      | for ( opt-expr ; opt-expr ; opt-expr ) stmt
      | other
opt-expr -> \epsilon
          | expr
'''

grammarText = '''
stmt -> expr ;                      { print }
      |                             { put('if ') }
        if ( expr )                 { put('jmp {}'.format(newLabel())) }
        stmt                        { print curLabel() }
      | for ( opt-expr ;            { print }
                                    { print newLabel() }
                                    { put('if') }
        opt-expr ;                  { }
        opt-expr ) stmt
      | other
opt-expr -> \epsilon
          | expr { put('e') }
'''
