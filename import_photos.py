#!/usr/bin/env python

import subprocess
import sys
import argparse
import glob
import os

def call_process(cmd):
  print("cmd: %s" % cmd)
  child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = child.communicate()
  if child.returncode != 0:
    print("Failed: %s: %s" % (cmd, stderr))
  return (stdout.rstrip(), stderr, child.returncode)

def create_permanode(*args):
  """ args is just an array """
  cmd = ['camput', 'permanode']
  if args is not None:
    cmd.extend(args)
  return call_process(cmd)

def put_attr(permanode, *args):
  cmd = ['camput', 'attr', '--add', permanode ]
  if args is not None:
    cmd.extend(args)
  return call_process(cmd)

def put_file(f):
    return call_process(['camput', 'file', f])

def main():
  argparser = argparse.ArgumentParser(description='upload pics to camlistore')
  argparser.add_argument("-g", "--glob-path", required=True, action="store", help="path (and glob) -- e.g., '/home/pics/*jpeg'")
  argparser.add_argument("-t", "--title", required=True, action="store", help="title of album")
  args = argparser.parse_args()
  album_title = args.title
  glob_path = args.glob_path

  folder_permanode, stderr, rc = create_permanode()
  if rc != 0:
    sys.exit(1)
  stdout, stderr, rc = put_attr(folder_permanode, "title", album_title)
  if rc != 0:
    sys.exit(1)    
  # FIXME... please
  for photo in glob.glob(glob_path):
    stdout, stderr, rc = pic_permanode, stderr, rc = create_permanode()
    if rc != 0:
      continue
    stdout, stderr, rc = put_attr(pic_permanode, "title", os.path.basename(photo)) 
    if rc != 0:
      continue
    new_file, stderr, rc = put_file(photo)
    if rc != 0:
      continue
    stdout, stderr, rc = put_attr(pic_permanode, "camliContent", new_file)
    if rc != 0:
      continue
    stdout, stderr, rc = put_attr(folder_permanode, "camliPath:%s" % os.path.basename(photo) , pic_permanode)
    if rc != 0:
      continue    

if __name__ == '__main__':
  main()
