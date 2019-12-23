"""Python package for using the JPush API"""
from .core import JPush, GroupPush, Admin
from .common import JPushFailure, Unauthorized

from .push import (
    Push,
    all_,
    tag,
    tag_and,
    tag_not,
    alias,
    registration_id,
    notification,
    ios,
    android,
    winphone,
    platform,
    audience,
    options,
    message,
    smsmessage,
)

from .device import (
    Device,
    add,
    remove,
    device_tag,
    device_alias,
    device_regid,
    device_mobile,
)

from .report import (
    Report,
    ReportResponse,
)

from .schedule import (
    Schedule,
    schedulepayload,
)

__all__ = [
    JPush,
    GroupPush,
    Admin,
    JPushFailure,
    Unauthorized,
    all_,
    Push,
    tag,
    tag_and,
    tag_not,
    alias,
    registration_id,
    notification,
    ios,
    android,
    winphone,
    message,
    smsmessage,
    platform,
    audience,
    options,
    Device,
    add,
    remove,
    device_tag,
    device_alias,
    device_regid,
    Report,
    ReportResponse,
    Schedule,
    schedulepayload,
]

__version__ = '3.3.0'
VERSION = tuple(map(int,  __version__.split('.')))

# Silence urllib3 INFO logging by default

import logging
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
