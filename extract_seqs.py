#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract a set of sequences from a Multi-FASTA file"""

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
	parser = argparse.ArgumentParser(description=__doc__)

	parser.add_argument('-i', '--input-file', dest='fasta_file', type=is_file, required=True,
			help='Multi-FASTA file containing the sequences.')

	parser.add_argument('-s', '--sequences-names', dest='sequences_names', type=is_file, required=True, 
			help='Text file which lists line by line the names of the sequences to extract.')

	parser.add_argument('-o', '--output-file', dest='output_file', required=True,
			help='Multi-FASTA file which contains the sequences extracted.')

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

	print('Indexing names of sequences to extract...')
	with open(parameters.sequences_names, 'r') as sequences_names_is:
		sequences_names = set(name.rstrip() for name in sequences_names_is)
	print('{0} sequences indexed.\n'.format(len(sequences_names)))

	print('Extracting sequences...')
	sequences_extracted = set()
	with open(parameters.fasta_file, 'r') as fasta_file_is, open(parameters.output_file, 'w') as output_file_os:
		for header, seq in fasta_reader(fasta_file_is):
			if header in sequences_names:
				print('>{0}\n{1}'.format(header,seq), file=output_file_os)

				sequences_extracted.add(header)
				if len(sequences_extracted) == len(sequences_names):
					break
	print('{0} sequences extracted.\n'.format(len(sequences_extracted)))

	sequences_missing = sequences_names - sequences_extracted
	if (sequences_missing):
		for sequence_missing in sequences_missing :
			print('warning : sequence \'{0}\' not found'.format(sequence_missing))

if __name__ == '__main__':
	main()

