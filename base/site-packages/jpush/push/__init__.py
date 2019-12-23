from .core import Push

from .audience import (
    tag,
    tag_and,
    tag_not,
    alias,
    registration_id,
    segment,
    abtest
)

from .payload import (
    android,
    ios,
    winphone,
    platform,
    cid,
    notification,
    message,
    audience,
    options,
    smsmessage,
)

# Common selector for audience & platform

all_ = "all"
"""Select all, to do a broadcast.

Used in both ``audience`` and ``platform``.
"""

__all__ = [
    all_,
    Push,
    tag,
    tag_and,
    tag_not,
    alias,
    registration_id,
    segment,
    abtest,
    notification,
    message,
    platform,
    cid,
    audience,
    options,
    smsmessage,
]
