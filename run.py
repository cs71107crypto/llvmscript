import os
import argparse
import sys
import json
import uuid
from subprocess import Popen


# Check whether given config is valid
def checkLLVMConfigForClone(js):
  # Destination of src should exist
  assert ("src" in js)
  # Should have cloninig repo info
  assert ("repo" in js)
  # LLVM repo should exist
  assert ("llvm" in js["repo"])
  # For each repo, url should exist
  for i in js["repo"]:
    assert ("url" in js["repo"][i])


class LLVMScript(object):

  def __init__(self):
    parser = argparse.ArgumentParser(
      usage = '''python3 run.py <command> [<args>]

Commands:
  clone    Clone LLVM into local
  build    Build LLVM
  lnt      Initialize / Run LLVM Nightly Tests
  spec2017 Run SPEC CPU2017

Type 'python3 run.py <command> help' to get details
''')
    parser.add_argument('command', help='clone/build/lnt/spec2017')
    args = parser.parse_args(sys.argv[1:2])
    if not hasattr(self, args.command):
      print ("Unrecognized command")
      parser.print_help()
      exit(1)
    getattr(self, args.command)()

  def clone(self):
    parser = argparse.ArgumentParser(
        description = 'Arguments for clone command')
    parser.add_argument('--cfg', help='config path for LLVM (json file)', action='store',
        required=True)
    parser.add_argument('--depth', help='commit depth to clone (-1 means inf)', nargs='?', const=-1, type=int)
    args = parser.parse_args(sys.argv[2:])

    cfgpath = args.cfg
    f = open(cfgpath)
    cfg = json.load(f)
    checkLLVMConfigForClone(cfg)

    # Make git clone commands.
    def make_cmd (cfg, name):
      cmd = ["git",
             "clone",
             cfg["repo"][name]["url"],
             cfg["src"] + "/" + name]

      if "branch" in cfg["repo"][name]:
        cmd.append("--branch")
        cmd.append(cfg["repo"][name]["branch"])

      if args.depth:
        if args.depth != -1:
          cmd.append("--depth")
          cmd.append(str(args.depth))

      return cmd

    cmds = []
    cmds.append(make_cmd(cfg, "llvm"))
    if "clang" in cfg["repo"]:
      cmds.append(make_cmd(cfg, "clang"))

    # git clone LLVM.
    try:
      os.makedirs(cfg["src"])
      pipes = []
      for cmd in cmds:
        print (" ".join(cmd))
        pipes.append(Popen(cmd))
      for p in pipes:
        p.wait()
    except OSError as e:
      print ("Cannot create directory '{0}'.".format(cfg["src"]))
      exit(1)

if __name__ == '__main__':
  LLVMScript()

# LLVM_EXTERNAL_{CLANG,LLD,POLLY}_SOURCE_DIR:PATH

