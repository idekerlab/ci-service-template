#!/usr/bin/env python

import csv
from optparse import OptionParser
import operator

import numpy as np
from scipy.sparse import csc_matrix

import kernel_scipy as kernel
import automateHeatKernel as ahk


class EstablishedKernel(kernel.SciPYKernel):

    def __init__(self, kernel_file):
        """
           Input:
                    kernel_file - filename of tab delemited kernel file,
                    as made by kernel_scipy.SciPYKernel
        """
        self.readKernel(kernel_file)

    def readKernel(self, input_file):
        ker = []
        start = True
        for line in csv.reader(open(input_file, 'r'), delimiter='\t'):
            if start:
                self.labels = line[1:]
                start = False
            else:
                ker.append([float(x) for x in line[1:]])

        self.kernel = csc_matrix(np.asarray(ker))


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-k", "--kernel", dest="kernel", action="store", type="string",
                      default="kernel.txt", help="Tab delimited file containing kernel")
    parser.add_option("-q", "--query", dest="query", action="store", type="string",
                      help="File containing list of query genes, one per line")
    parser.add_option("-d", "--diffused-query", dest="diffused_query", type="string",
                      default="diffused.txt", help="Output file for diffused query.")

    (opts, args) = parser.parse_args()

    ker = EstablishedKernel(opts.kernel)

    gene_file = opts.query

    f = open(gene_file, 'r')

    get_these = []

    for line in f:
        get_these.append(line.rstrip())

    queryVec = ahk.queryVector(get_these, ker.labels)

    diffused = ker.diffuse(queryVec)
    sorted_diffused = sorted(diffused.items(), key=operator.itemgetter(1), reverse=True)

    writer = csv.writer(open(opts.diffused_query, 'wb'))

    for key, value in sorted_diffused:
        writer.writerow([key, value])
