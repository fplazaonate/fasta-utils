#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sort sequences from a Multi-FASTA file by their length"""

from __future__ import print_function
import argparse
import os

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
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-i', '--input-file', dest='fasta_file', type=is_file, required=True, default=argparse.SUPPRESS,
			help='Multi-FASTA file containing the sequences.')

	parser.add_argument('--order', dest='order', choices=['ascending', 'descending'], default='descending',
			help='Sort order.')

	parser.add_argument('-o', '--output-file', dest='output_file', required=True, default=argparse.SUPPRESS,
			help='Multi-FASTA file with sequences sorted by their length.')

	return parser.parse_args()

def fasta_reader(istream):
	header, seq = None, None
	for line in istream:
		line = line.rstrip()
		if line.startswith(">"):
			if header: yield (header, ''.join(seq))
			header, seq = line[1:], []
		else:
			seq.append(line) 

	if header: yield (header, ''.join(seq))

def main():
	parameters = get_parameters()

	print('Indexing sequences...')
	with open(parameters.fasta_file, 'r') as fasta_file_is:
		entries = [(header,seq,len(seq)) for (header,seq) in fasta_reader(fasta_file_is)]
	print('{0} sequences indexed.\n'.format(len(entries)))
	
	print('Sorting sequences...')
	entries = sorted(entries, key=lambda entry: entry[2], reverse=(parameters.order=='descending'))
	print('Done.\n')

	print('Writing sorted sequences...')
	with open(parameters.output_file, 'w') as output_file_os:
		for entry in entries:
			print('>{0}\n{1}'.format(entry[0],entry[1]), file=output_file_os)
	print('Done.\n')

if __name__ == '__main__':
	main()

