import re

# Value selectors; aliases, tags, etc.

def tag(*tags):
    """Select a (list of) tag(s)."""
    vtag = [t for t in tags]
    return {"tag": vtag}

def tag_and(*tag_ands):
    """Select a (list of) tag_and(s)."""
    vtag_and = [t for t in tag_ands]
    return {"tag_and": vtag_and}

def tag_not(*tag_nots):
    """Select a (list of) tag_not(s)."""
    vtag_not = [t for t in tag_nots]
    return {"tag_not": vtag_not}

def alias(*alias):
    """Select a (list of) alias(es)."""
    valias = [t for t in alias]
    return {"alias": valias}

def registration_id(*reg_ids):
    """Select a (list of) registration_id(s)."""
    vregistration_id = [t for t in reg_ids]
    return {"registration_id": vregistration_id}

def segment(*segments):
    """Select a (list of) segment(s)."""
    vsegment = [t for t in segments]
    return {"segment": vsegment}

def abtest(*abtests):
    """Select a (list of) abtest(s)."""
    vabtest = [t for t in abtests]
    return {"abtest": vabtest}
