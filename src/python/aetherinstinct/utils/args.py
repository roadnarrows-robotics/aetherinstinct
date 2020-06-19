"""
Command-line argument parsing with structured printing.

See the argparse python module for details to extend argument parsing.

\LegalBegin
 Copyright 2019-2020 Aether Instinct LLC. All Rights Reserved

 Licensed under the MIT License (the "License").

 You may not use this file except in compliance with the License. You may
 obtain a copy of the License at:

   https://opensource.org/licenses/MIT

 The software is provided "AS IS", without warranty of any kind, express or
 implied, including but not limited to the warranties of merchantability,
 fitness for a particular purpose and noninfringement. in no event shall the
 authors or copyright holders be liable for any claim, damages or other
 liability, whether in an action of contract, tort or otherwise, arising from,
 out of or in connection with the software or the use or other dealings in the
 software.
\LegalEnd
"""

import argparse
import textwrap

class SmartFormatter(argparse.RawTextHelpFormatter):
  """ Extend the argparse formatter to support indented multiline help. """

  def _split_lines(self, text, width):
    """
    Smart split of text.

    Parameters:
      text    String.
      width   Maximum width.

    Returns:
      Returns list of lines.
    """
    if text.startswith('R|'):
      return text[2:].splitlines()
    else:
      # this is the RawTextHelpFormatter._split_lines
      return argparse.HelpFormatter._split_lines(self, text, width)

def add_subparsers(argparser, helptext):
  """
  Conditionally add subparsers to argument parser.

  An ArgumentParser can only have one assigned subparsers.

  The subparsers object is added to the argparser attributes.
    argparser.subparsers

  Parameters:
    argparser   ArgumentParser object.
    helptext    Help text.

  Returns:
    Returns subparsers object.
  """
  try:
    if argparser.subparsers is None:
      argparser.subparsers = argparser.add_subparsers(help=helptext)
  except AttributeError:
    argparser.subparsers = argparser.add_subparsers(help=helptext)
  return argparser.subparsers
