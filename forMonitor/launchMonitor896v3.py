# -*- coding: utf-8 -*-
# 2021/10/07




import argparse
parser = argparse.ArgumentParser(description='Launch monitor896.py with premade profiles.')
parser.add_argument('profile', help='Path of the launch profile.')
parser.add_argument('--test', '-t', default=None, help='Add the letters \"test\" to the end of products.')
parser.add_argument('--debug', default=None, help='For debug this script')
args = parser.parse_args()