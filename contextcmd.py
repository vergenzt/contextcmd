#!/usr/bin/env python
'''
ContextCmd
Tim Vergenz
10/3/2013

Allows default arguments to shell commands to be context-dependent. Currently
this means that I can change my default arguments to `ls` depending on what
folder I'm in, but I suppose it could be extended to be used for other
contextual information.
'''
import sys
import os.path
import subprocess
from collections import defaultdict


class ArgRules(object):
    def __init__(self, base=None, rules=None):
        if base: self.rules = base.rules.copy()
        else: self.rules = defaultdict(list)
        for rule in rules:
            self.rules[rule.path].append(rule)

class Rule(object):
    def __init__(self, path, args='', extend=False, id=None, exclude=None):
        self.path = os.path.realpath(path)
        self.args = args
        self.extend = extend
        self.id = id
        if exclude:
            self.exclude = (exclude if isinstance(exclude,list) else [exclude])
        else:
            self.exclude = []
    def __repr__(self):
        return "<Rule ({path}) {args}{extend}{id}{exclude}>".format(
                path=self.path,
                args='args=' + self.args,
                extend=', extend=True' if self.extend else '',
                id=', id='+self.id if self.id else '',
                exclude=', exclude='+str(self.exclude) if self.exclude else ''
            )

def run_command(cmd, loc, argrules):
    applied_rules = []
    exclusions = []
    def process_rule(rule):
        applied_rules.insert(0, rule)
        for id in rule.exclude:
            if id: exclusions.append(id)

    # apply rules for this particular directory
    for rule in argrules.rules[loc]:
        process_rule(rule)

    # ascend the directory tree and apply any rules there
    curpath = loc
    while curpath != '/':
        curpath,_ = os.path.split(curpath)
        for rule in argrules.rules[curpath]:
            if rule.extend:
                process_rule(rule)

    # filter the exclusions out
    for id in exclusions:
        applied_rules = [r for r in applied_rules if r.id != id]

    # build the arguments
    args = ' '.join([rule.args for rule in applied_rules])
    subprocess.call([cmd] + args.split() + sys.argv[2:])


if __name__=='__main__':
    import settings
    cmd = sys.argv[1]
    loc = os.path.realpath(os.getcwd())
    for arg in sys.argv:
        if os.path.isdir(arg):
            loc = os.path.realpath(arg)
            break
    run_command(cmd, loc, getattr(settings, cmd))

