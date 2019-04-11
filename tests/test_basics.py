
import os
import sys 
import unittest
import tempfile
import shutil
import runpy

import pyloco
import frelpt

_here = os.path.dirname(__file__)
_complex1 = os.path.join(_here, "sca", "complex1")
_target = os.path.join(_complex1, "main.f90")
_clean_cmd = "cd %s; make clean"%_complex1
_build_cmd = "cd %s; make org"%_complex1

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_basic(self):

        retval, forward = pyloco.perform(frelpt.FrelptTask, argv=[
            _target,
            _clean_cmd,
            _build_cmd,
            "--outdir", str(self.tempdir),
            "--log", "basictests",
            "--debug"
        ])
 
            #"--debug",

        self.assertEqual(retval, 0) 

test_classes = (BasicTests,)

