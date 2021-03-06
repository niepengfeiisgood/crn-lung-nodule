import argparse
import datetime
import logging

import sys

import os

from crn_lung_nodule import mylogger
from crn_lung_nodule.danforth_algorithm import extract_files
from crn_lung_nodule.util.constants import ALGORITHMS, TOKENS, PHRASE_SEARCH_METHODS, STRING


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('-i', '--input-dir', required=True,
                        help='Name of input directory containing text files.')
    parser.add_argument('-o', '--output', required=True,
                        help='Name of output file.')
    parser.add_argument('-L', '--log-dir', default='log',
                        help='Directory to output log files.')
    parser.add_argument('-a', '--algorithm', default=ALGORITHMS[0], choices=ALGORITHMS,
                        help='Algorithm to use: {}.'.format(', '.join(ALGORITHMS)))
    parser.add_argument('--psm', default=STRING, choices=PHRASE_SEARCH_METHODS,
                        help='Name of phrase search method to be used: {}.'.format(', '.join(PHRASE_SEARCH_METHODS)))
    parser.add_argument('--r6psm', default=TOKENS, choices=PHRASE_SEARCH_METHODS,
                        help='Rule 6 phrase search method to be used '
                             '(defaults to psm).')
    parser.add_argument('--get-largest-nodule-size', action='store_true',
                        default=False,
                        help='Retrieve largest nodule size.')
    parser.add_argument('--codec', default=None, required=False,
                        help='Specify character encoding for input documents. '
                             'See: https://docs.python.org/library/codecs.html#standard-encodings.')
    parser.add_argument('--use-base-sentence-splitter', action='store_true', default=False,
                        help='Do not use the Punkt Tokenizer.')
    args = parser.parse_args()

    # todo: set logger
    if not args.r6psm:
        args.r6psm = args.psm

    if args.output:
        out = open(args.output, 'w')
    else:
        out = sys.stdout

    mylogger.config(os.path.join(args.log_dir, datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
                    loglevel=logging.DEBUG)

    out.write('File,Decision,MaxNoduleSize{}\n')
    for args in extract_files(args.input_dir,
                              phrase_search_method=args.psm,
                              get_largest_nodule_size=args.get_largest_nodule_size,
                              rule6_phrase_search_method=args.r6psm,
                              algorithm=args.algorithm, codec=args.codec,
                              use_base_sentence_splitter=args.use_base_sentence_splitter):
        out.write('{}\n'.format(','.join(str(x) for x in args)))
    out.close()


if __name__ == '__main__':
    main()
