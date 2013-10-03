from contextcmd import ArgRules, Rule

ls = ArgRules(rules=[
    Rule('/', args='--color=auto --group-directories-first', extend=True),
    Rule('/home/tim', id='dereference', args='--dereference', extend=True),
    Rule('/home/tim/Programming/projects', args='-lt'),
    Rule('/home/tim/Documents/Resume', exclude='dereference', extend=True),
])
#lsr = ArgRules(ls, [Rule('/', exclude='dereference', extend=True)])

