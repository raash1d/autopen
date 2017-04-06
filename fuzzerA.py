#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function # Only Python 2.x
import subprocess
import sys


def execute(cmd):
	popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True, universal_newlines=True)
	for stdout_line in iter(popen.stdout.readline, ""):
		yield stdout_line 
	popen.stdout.close()
	return_code = popen.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code, cmd)

even = 0

arb = sys.argv[1]
num = sys.argv[2]

for i in range(int(num)):
	if even == 0:
		for line in execute(["cansend vcan0 {}#11.2233.44556667.88".format(arb)]):
			even = 1

	if even == 1:
		for line in execute(["cansend vcan0 {}#11.2233.44556667.88".format(arb)]):
			even = 0
