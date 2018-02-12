import glob

import json

import pickle

import gzip

import os

import hashlib

import re
names = set([name for name in glob.glob('htmls/*')])

urls = set()
for name in names:
  print(gzip.decompress(open(name,'rb').read()).decode())
