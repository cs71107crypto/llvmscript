# llvmscript

One-for-all python script for running experiment with LLVM 


# Prerequisites

- cset: required if `use_cset` is enabled. [NOPASSWD for sudo](https://askubuntu.com/questions/147241/execute-sudo-without-password) should be set as well

# Commands

`python3 run.py clone --cfg <.json file (ex: examples/llvm.json)>`

- Clones LLVM (as well as Clang, if mentioned in the config file)


`python3 run.py build --cfg <.json file> --build <release/relassert/debug> --core <# of cores to use>`

- Builds LLVM (as well as Clang)


`python3 run.py lntclone --cfg <.json file>`

- Clones & initializes LLVM Nightly Tests


`python3 run.py lnt --cfg <.json file> --lntcfg <.json file> --runcfg <.json file>`

- Runs LLVM Nightly Tests
