from dragonfly import Compound, RuleRef, RuleWrap

def get_ruleref(compound: Compound, rulewrap_name):
    return RuleRef(RuleWrap("", compound).rule, rulewrap_name)
