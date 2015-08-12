#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Compute the length of each sequence of a FASTA file"""

from __future__ import print_function
import argparse
import os
import time

__author__ = "Florian Plaza Oñate"
__copyright__ = "Copyright 2015, Enterome"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Florian Plaza Oñate"
__email__ = "fplaza-onate@enterome.com"
__status__ = "Development"

def is_file(path):
    """Check if path is an existing file.
    """

    if not os.path.isfile(path):
        if os.path.isdir(path):
            msg = "{0} is a directory".format(path)
        else:
            msg = "{0} does not exist.".format(path)
            raise argparse.ArgumentTypeError(msg)
    return path

def get_parameters():
    """Parse command line parameters.
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-i', '--input-file', dest='fasta_file', type=is_file, required=True, 
            help='Multi-FASTA file')

    parser.add_argument('-o', '--output-file', dest='output_file', required=True, 
            help='Output file which contains line by line, tab separated pairs of values <seq_name> <seq_length>')

    return parser.parse_args()

def fasta_seqs_length(istream):
    header, seq_length = None, 0
    for line in istream:
        line = line.rstrip()
        if line.startswith(">"):
            if header: yield (header, seq_length)
            header, seq_length = line[1:], 0
        else:
            seq_length = seq_length + len(line)

    if header: yield (header, seq_length)


def main():
    parameters = get_parameters()

    print('Computing length of sequences...')
    start = time.clock()
    with open(parameters.fasta_file, 'r') as istream, open(parameters.output_file, 'w') as ostream:
        for header, seq_length in fasta_seqs_length(istream):
            print('"{0}"\t{1}'.format(header, seq_length), file=ostream)
    stop = time.clock()
    elapsed = stop -start
    print('Done in {0} seconds'.format(elapsed))

if __name__ == '__main__':
    main()

