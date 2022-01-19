import os
import unittest

from eufrates.exceptions import WorkflowTaskExecException

from eufrates import Task, WorkflowException

from eufrates.bpmn.workflow import BpmnWorkflow

from eufrates.dmn.parser.BpmnDmnParser import BpmnDmnParser
from tests.eufrates.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase
from tests.eufrates.dmn.DecisionRunner import DecisionRunner


class InvalidBusinessRuleNameErrorTest(unittest.TestCase):

    def test_integer_decision_string_output_inclusive(self):
        runner = DecisionRunner('invalid_decision_name_error.dmn',
                                debug='DEBUG')
        try:
            res = runner.decide({'spam': 1})
        except Exception as e:
            self.assertRegexpMatches(str(e), "did you mean one of \['spam'\]")

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(InvalidBusinessRuleNameErrorTest)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
