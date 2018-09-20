"""This module checks if there any undefined gflags used in input python
module(s)."""
#!/usr/bin/env python

import importlib
import re
import sys
import tokenize
import traceback

import gflags

from util.base import log

gflags.ADOPT_module_key_flags(log)

GFLAGS_PREFIX = "FLAGS."
GFLAGS_PREFIX_FULL = "gflags.FLAGS."
PY_OPERATORS_DELIMITERS = "+-*/%@<>&|^~=!()[]{},:.;"
GFLAG_NAME_REGEX = re.compile(r"(.*)(FLAGS\.)([a-zA-Z_]\w*)(.*)")
UNDEFINED_GFLAG_FOUND = False

def tokenize_manually(source, module):
  """Tokenizes the python source code file manually and looks for
  gflags used in the file and checks if they are undefined.

  Arguments:
    source: file object of the python source code file
    module: name of the python module in source
  """
  global UNDEFINED_GFLAG_FOUND

  for line in source:
    line = line.strip()
    # Skip single comment lines. Can't avoid multiline comments though.
    if line.startswith('#'):
      continue
    if GFLAGS_PREFIX in line:
      log.DEBUG("line: %s" % line)
      for token in line.split():
        # Remove any operators and delimiters that could be
        # surrounding the gflag.
        token = token.strip(PY_OPERATORS_DELIMITERS)
        if GFLAGS_PREFIX in token:
          token = token.split(GFLAGS_PREFIX)[-1]
          token = token.strip(GFLAGS_PREFIX)
        elif GFLAGS_PREFIX_FULL in token:
          token = token.split(GFLAGS_PREFIX_FULL)[-1]
          token = token.strip(GFLAGS_PREFIX_FULL)
        else:
          continue
        log.DEBUG("%s: %s" % (sys._getframe().f_code.co_name, token))
        if token not in gflags.FLAGS.RegisteredFlags():
          UNDEFINED_GFLAG_FOUND = True
          log.ERROR("%s used in %s is undefined" % (token, module))

def tokenize_regex(source, module):
  """Tokenizes the python source code file manually and looks for
  gflags used in the file and checks if they are undefined.

  Arguments:
    source: file object of the python source code file
    module: name of the python module in source
  """
  global UNDEFINED_GFLAG_FOUND

  for line in source:
    line = line.strip()
    # Skip single comment lines. Can't avoid multiline comments though.
    if line.startswith('#'):
      continue
    try:
      gflag_name = GFLAG_NAME_REGEX.match(line).groups()[2]
    except AttributeError:  # Not a match.
      pass
    else:
      log.DEBUG("line: %s" % line)
      log.DEBUG("%s: %s" % (sys._getframe().f_code.co_name, gflag_name))
      if gflag_name not in gflags.FLAGS.RegisteredFlags():
        UNDEFINED_GFLAG_FOUND = True
        log.ERROR("%s used in %s is undefined" % (gflag_name, module))

def tokenize_lexical_scanner(source, module):
  """Tokenizes the python source code using a lexical scanner and looks
  for gflags used in the file and checks if they are undefined.

  Arguments:
    source: file object of the python source code file
    module: name of the python module in source
  """
  global UNDEFINED_GFLAG_FOUND

  generator = tokenize.generate_tokens(source.readline)
  tkn_lst = []
  for token_type, token_str, _, _, line in generator:
    if token_type == tokenize.COMMENT:
      continue
    # At the end of one line of code.
    if token_str == '\n':
      indices = [idx for idx, tkn in enumerate(tkn_lst) if tkn == "FLAGS"]
      for idx in indices:
        try:
          if tkn_lst[idx + 1] == '.':
            gflag_name = tkn_lst[idx + 2]
            log.DEBUG("line: %s" % line)
            log.DEBUG("token list: %s" % tkn_lst)
            log.DEBUG("%s: %s" % (sys._getframe().f_code.co_name, gflag_name))
            if gflag_name not in gflags.FLAGS.RegisteredFlags():
              UNDEFINED_GFLAG_FOUND = True
              log.ERROR("%s used in %s is undefined" % (gflag_name, module))
        except IndexError:
          log.DEBUG("IndexError: %s" % line)
          continue
      tkn_lst = []
    else:
      tkn_lst.append(token_str)

def check_undefined_gflags(module_list):
  """Checks if any undefined gflags are used in module_list.

  Arguments:
    module_list: list of python modules to check for undefined gflags.
  """
  for module in module_list:
    try:
      imported_module = importlib.import_module(module)
    except ImportError as iexc:
      log.ERROR("Unable to import %s" % module)
      log.ERROR(traceback.format_exc())
      log.ERROR(iexc)
      sys.exit(1)
    except AssertionError:
      log.ERROR("Unable to import %s because of an assert statement in it. "
                "Remove it temporarily to test it with %s" % (module,
                                                              sys.argv[0]))
      sys.exit(1)
    except Exception as exc:
      log.ERROR("Unable to import %s" % module)
      log.ERROR(traceback.format_exc())
      log.ERROR(exc)
      sys.exit(1)

    # Read from .py fle and not .pyc file.
    with open(imported_module.__file__.rstrip('c')) as source:
      #tokenize_manually(source, module)
      #source.seek(0)
      #tokenize_regex(source, module)
      #source.seek(0)
      tokenize_lexical_scanner(source, module)

    del imported_module

  return None

def _parse_cmd_line_opts_args(argv):
  """Parses command-line options and positional arguments.

  Arguments:
    argv: list of command-line arguments
  """
  # Parse the gflags. Note that they are removed from argv.
  argv = gflags.FLAGS(argv)

  return argv[1:]

def main(argv):
  """Main function that parses command-line options and arguments and
  checks for undefined gflags in them.

  Arguments:
    argv: list of command-line arguments
  """
  # Setup logging.
  gflags.FLAGS.logtostderr = True
  log.initialize()

  check_undefined_gflags(_parse_cmd_line_opts_args(argv))

  if UNDEFINED_GFLAG_FOUND:
    sys.exit(1)

if __name__ == "__main__":
  main(sys.argv)
