import os
import unittest

from eufrates import Task

from eufrates.bpmn.workflow import BpmnWorkflow

from eufrates.dmn.parser.BpmnDmnParser import BpmnDmnParser
from tests.eufrates.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

class DmnVersionTest(BpmnWorkflowTestCase):
    PARSER_CLASS = BpmnDmnParser

    def setUp(self):
        self.parser = BpmnDmnParser()

    def testLoad(self):
        dmn = os.path.join(os.path.dirname(__file__), 'data',
                            'dmn_version_20191111_test.dmn')
        self.assertIsNone(self.parser.add_dmn_file(dmn))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(DmnVersionTest)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
