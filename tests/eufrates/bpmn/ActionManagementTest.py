# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
import unittest
import datetime
import time
from eufrates.task import Task
from eufrates.bpmn.workflow import BpmnWorkflow
from tests.eufrates.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

__author__ = 'matth'


class ActionManagementTest(BpmnWorkflowTestCase):

    def setUp(self):
        self.spec = self.load_spec()
        self.workflow = BpmnWorkflow(self.spec)

        start_time = datetime.datetime.now() + datetime.timedelta(seconds=0.5)
        finish_time = datetime.datetime.now() + datetime.timedelta(seconds=1.5)

        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.workflow.get_tasks(Task.READY)[0].set_data(
            start_time=start_time, finish_time=finish_time)

    def load_spec(self):
        return self.load_workflow_spec('Test-Workflows/*.bpmn20.xml', 'Action Management')

    def testRunThroughHappy(self):
        self.do_next_exclusive_step("Review Action", choice='Approve')
        self.workflow.do_engine_steps()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual('NEW ACTION', self.workflow.get_tasks(
            Task.READY)[0].get_data('script_output'))
        self.assertEqual('Cancel Action (if necessary)',
                          self.workflow.get_tasks(Task.READY)[0].task_spec.description)

        time.sleep(0.6)
        self.workflow.refresh_waiting_tasks()
        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(2, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step("Start Work")
        self.workflow.do_engine_steps()

        self.do_next_named_step("Complete Work", choice="Done")
        self.workflow.do_engine_steps()

        self.assertTrue(self.workflow.is_completed())

    def testRunThroughOverdue(self):
        self.do_next_exclusive_step("Review Action", choice='Approve')
        self.workflow.do_engine_steps()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual('Cancel Action (if necessary)',
                          self.workflow.get_tasks(Task.READY)[0].task_spec.description)

        time.sleep(0.6)
        self.workflow.refresh_waiting_tasks()
        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(2, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step("Start Work")
        self.workflow.do_engine_steps()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual('Finish Time', self.workflow.get_tasks(
            Task.WAITING)[0].task_spec.description)
        time.sleep(1.1)
        self.workflow.refresh_waiting_tasks()
        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertNotEqual(
            'Finish Time', self.workflow.get_tasks(Task.WAITING)[0].task_spec.description)

        overdue_escalation_task = [
            t for t in self.workflow.get_tasks() if t.task_spec.description == 'Overdue Escalation']
        self.assertEqual(1, len(overdue_escalation_task))
        overdue_escalation_task = overdue_escalation_task[0]
        self.assertEqual(Task.COMPLETED, overdue_escalation_task.state)
        self.assertEqual(
            'ACTION OVERDUE', overdue_escalation_task.get_data('script_output'))

        self.do_next_named_step("Complete Work", choice="Done")
        self.workflow.do_engine_steps()

        self.assertTrue(self.workflow.is_completed())

    def testRunThroughCancel(self):

        self.do_next_exclusive_step("Review Action", choice='Cancel')
        self.workflow.do_engine_steps()

        self.assertTrue(self.workflow.is_completed())

    def testRunThroughCancelAfterApproved(self):
        self.do_next_exclusive_step("Review Action", choice='Approve')
        self.workflow.do_engine_steps()

        self.do_next_named_step("Cancel Action (if necessary)")
        self.workflow.do_engine_steps()

        self.assertTrue(self.workflow.is_completed())
        self.assertEqual(
            'ACTION CANCELLED', self.workflow.get_data('script_output'))

    def testRunThroughCancelAfterWorkStarted(self):
        self.do_next_exclusive_step("Review Action", choice='Approve')
        self.workflow.do_engine_steps()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        time.sleep(0.6)
        self.workflow.refresh_waiting_tasks()
        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(2, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step("Start Work")
        self.workflow.do_engine_steps()

        self.do_next_named_step("Cancel Action (if necessary)")
        self.workflow.do_engine_steps()

        self.assertTrue(self.workflow.is_completed())
        self.assertEqual(
            'ACTION CANCELLED', self.workflow.get_data('script_output'))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ActionManagementTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
