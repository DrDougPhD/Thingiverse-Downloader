import logging

from .. import authentication

logger = logging.getLogger(__name__)


class ThingiverseBase(object):
    @authentication.required
    def __init__(self):
        logger.info('Thingiverse Base Class init')