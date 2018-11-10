
import logging
import re
from .defs import Status

log = logging.getLogger('slurmy')


class Parser(object):
    _prefix = '@SLURMY.'
    def __init__(self, config):
        ## The job/jobhandler config of the parent
        self.config = config

    def replace(self, string):
        ## Replace config variables
        for prop in self.config._properties:
            prop = prop.strip('_')
            parse_string = '{}{}'.format(self._prefix, prop)
            if parse_string not in string: continue
            prop_val = getattr(self.config, prop)
            string = string.replace(parse_string, prop_val)
        ## Make sanity check and print warning if prefix string still exists in script
        problem_lines = [l for l in string.split('\n') if self._prefix in string]
        if problem_lines:
            log.warning('Unknown {} variable(s) in input string:'.format(self._prefix))
            for line in problem_lines:
                log.warning('  '+line)

        return string

    def set_status_label(self, string, identifier, status):
        label = '{}{}'.format(self._prefix, status.name)
        if label in string:
            label_file = '{}.{}.{}'.format(self.config.tmp_dir, identifier, status.name)
            string = string.replace(label, 'touch {}'.format(label_file))
            return string, label_file
        else:
            return string, None
