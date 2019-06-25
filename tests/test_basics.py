
import os
import sys 
import unittest
import tempfile
import shutil
import runpy

import pyloco
import frelpt

_here = os.path.dirname(__file__)
_complex3 = os.path.join(_here, "sca", "complex3", "org")
_target = os.path.join(_complex3, "main.f90")
_clean_cmd = "cd %s; make clean"%_complex3
_build_cmd = "cd %s; make org"%_complex3

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        shutil.copy(os.path.join(_complex3, "Makefile"), self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_basic(self):

        retval, forward = pyloco.perform(frelpt.FrelptTask, argv=[
            _target,
            _clean_cmd,
            _build_cmd,
            "--outdir", str(self.tempdir),
            "--log", "basictests",
            "--debug",
        ])
 
        out1 = pyloco.system("make", cwd=_complex3)
        out2 = pyloco.system("make", cwd=self.tempdir)

        self.assertEqual(out1[0], 0) 
        self.assertEqual(out2[0], 0) 
        self.assertEqual(out1[1].split()[-1], '38042808.0') 
        self.assertEqual(out2[1].split()[-1], '38042808.0') 


test_classes = (BasicTests,)

