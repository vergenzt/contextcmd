from contextcmd import ArgRules, Rule

'''
A rule consists of a path on which the rule applies, and the default arguments
to add for that path (and an optional `id`). `extend` determines whether to
apply the rule to subdirectories as well, and `exclude` determines rules to
exclude on the application of the current rule.


'''

ls = ArgRules(rules=[
    Rule('/', args='--color=auto --group-directories-first', extend=True),
    Rule('/home/tim', id='dereference', args='--dereference', extend=True),
    Rule('/home/tim/Programming/projects', args='-lt'),
    Rule('/home/tim/Documents/Resume', exclude='dereference', extend=True),
])
#lsr = ArgRules(ls, [Rule('/', exclude='dereference', extend=True)])

