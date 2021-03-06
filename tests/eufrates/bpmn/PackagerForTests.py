# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from io import BytesIO
from eufrates.bpmn.serializer.Packager import Packager, main
from tests.eufrates.bpmn.BpmnLoaderForTests import TestBpmnParser

__author__ = 'matth'


class PackagerForTests(Packager):

    PARSER_CLASS = TestBpmnParser

    @classmethod
    def package_in_memory(cls, workflow_name, workflow_files, editor='signavio'):
        s = BytesIO()
        p = cls(s, workflow_name, meta_data=[], editor=editor)
        p.add_bpmn_files_by_glob(workflow_files)
        p.create_package()
        return s.getvalue()

if __name__ == '__main__':
    main(packager_class=PackagerForTests)
