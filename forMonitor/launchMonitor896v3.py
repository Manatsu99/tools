# -*- coding: utf-8 -*-
# 2021/10/07
import utils.loggingTool as lTool

def run(profile, test, debug):
    l = lTool.loggingTool(True,True,True, "TEST")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Launch monitor896.py with premade profiles.')
    parser.add_argument('profile', help='Path of the launch profile.')
    parser.add_argument('--test', '-t', help='Add the letters \"test\" to the end of products.', action='store_true')
    parser.add_argument('--debug', '-d', help='For debug this script', action='store_true')
    args = parser.parse_args()
    run(args.profile, args.test, args.debug)