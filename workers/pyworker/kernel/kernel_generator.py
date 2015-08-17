from array import array
import time
import urllib2
import logging

from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm

logging.basicConfig(level=logging.DEBUG)


class KernelGenerator:

    def __init__(self, network_file, time_t=0.1):
        """ 
        Input:

            network_file - a tab-delimited file in .sif network format:
            <source> <interaction> <target>

        Returns:

            Kernel object.                 

        """

        start = time.clock()

        self.time_T = time_t
        self.labels = {}
        # The number of rows and columns for each kernel
        self.ncols = {}
        self.nrows = {}

        # parse the network, build indexes
        edges, nodes, node_out_degrees = self.__parse_net(network_file)
        num_nodes = len(nodes)
        node_order = list(nodes)
        index2node = {}
        node2index = {}

        logging.debug('Nodes: ' + str(num_nodes))
        logging.debug('Edges: ' + str(len(edges)))

        for i in range(0, num_nodes):
            index2node[i] = node_order[i]
            node2index[node_order[i]] = i

        # construct the diagonals
        # SCIPY uses row and column indexes to build the matrix
        # row and columns are just indexes: the data column stores 
        # the actual entries of the matrix
        row = array('i')
        col = array('i')
        data = array('f')
        # build the diagonals, including the out-degree 
        for i in range(0, num_nodes):
            # diag entries: out degree
            degree = 0
            if index2node[i] in node_out_degrees:
                degree = node_out_degrees[index2node[i]]
                # append to the end
            # array object: first argument is the index, the second is the data value
            # append the out-degree to the data array
            data.insert(len(data), degree)
            # build the diagonals
            row.insert(len(row), i)
            col.insert(len(col), i)

            # add off-diagonal edges
        for i in range(0, num_nodes):
            for j in range(0, num_nodes):
                if i == j:
                    continue
                if (index2node[i], index2node[j]) not in edges:
                    continue
                # append index to i-th row, j-th column
                row.insert(len(row), i)
                col.insert(len(col), j)
                # -1 for laplacian: i.e. the negative of the adjacency matrix 
                data.insert(len(data), -1)

        # Build the graph laplacian: the CSC matrix provides a sparse matrix format
        # that can be exponentiated efficiently
        l = coo_matrix((data, (row, col)), shape=(num_nodes, num_nodes)).tocsc()
        self.laplacian = l
        self.index2node = index2node

        end = time.clock()
        logging.debug('prep done: ' + str(end - start) + ' sec.')

        start = time.clock()
        # this is the matrix exponentiation calculation.
        # Uses the Pade approximiation for accurate approximation.
        # Computationally expensive.
        # O(n^2), n= # of features, in memory as well. 
        self.kernel = expm(-self.time_T * l)
        self.labels = node_order
        end = time.clock()
        logging.debug('expm done: ' + str(end - start) + ' sec.')

    def get_labels(self):
        """
            Return the set of all node/gene labels used by this kernel object
        """
        all_labels = set()
        for label in self.labels:
            print(label)
            all_labels = all_labels.union(set(self.labels[label]))

        return all_labels

    def write_kernel(self, output_stream):
        """
        Write the computer kernel to the supplied output file
        """
        # out_fh = open(output_file, 'w')
        cx = self.kernel.tocoo()
        edges = {}
        for i, j, v in zip(cx.row, cx.col, cx.data):
            a = self.index2node[i]
            b = self.index2node[j]
            edges[(a, b)] = str(v)

        # iterate through rows
        # sort labels in alphabetical order

        output_stream.write("Key\t" + "\t".join(sorted(self.labels)) + "\n")

        for nodeA in sorted(self.labels):
            printstr = nodeA
            # through columns       
            for nodeB in sorted(self.labels):
                if (nodeA, nodeB) in edges:
                    printstr += "\t" + edges[(nodeA, nodeB)]
                else:
                    printstr += "\t0"

            output_stream.write(printstr + "\n")

        return output_stream.getvalue()

    def __print_laplacian(self):
        """
        Debug function
        """
        cx = self.laplacian.tocoo()
        for i, j, v in zip(cx.row, cx.col, cx.data):
            a = self.index2node[i]
            b = self.index2node[j]
            print "\t".join([a, b, str(v)])

    def __parse_net(self, sif):
        """
        Parse .sif network, using just the first and third columns
        to build an undirected graph. Store the node out-degrees
        in an index while we're at it. 
        """
        edges = set()
        nodes = set()
        degrees = {}

        for line in urllib2.urlopen(sif):

            parts = line.rstrip().split()
            source = parts[0]
            target = parts[2]

            # if inputing a multi-graph, skip this
            if (source, target) in edges:
                continue
            if source == target:
                continue

            edges.add((source, target))
            edges.add((target, source))
            nodes.add(source)
            nodes.add(target)

            if source not in degrees:
                degrees[source] = 0
            if target not in degrees:
                degrees[target] = 0

            degrees[source] += 1
            degrees[target] += 1

        return edges, nodes, degrees
