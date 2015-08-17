#!/usr/bin/env python

import sys

import operator
from ndex.client import Ndex as nc
import ndexUtil as util

from optparse import OptionParser
import csv
import numpy as np

from ..kernel.kernel_generator import SciPyKernel


class TableEntityMapper():
    """This class is a container for a mapping table between two namespaces.
    Expects a filename for a file that is two tab delimited columns, source\ttarget
    Retutns a list (!) of ids"""

    def __init__(self, filename, missingStrList=[]):
        self.mappingTable = {}
        self.readFileToMappingTable(filename)
        self.missingStrList = missingStrList

    def readFileToMappingTable(self, filename):
        with open(filename, "r") as ins:
            for line in ins:
                arr = line.split('\t')
                if arr[0] not in self.mappingTable:
                    self.mappingTable[arr[0]] = [arr[1].rstrip()]
                else:
                    print("multiple mappings of %s detected" % arr[0])
                    self.mappingTable[arr[0]].append(arr[1])

    def map(self, entity):
        try:
            return self.mappingTable[entity]
        except:
            return self.missingStrList


def mapByPrefix(i, MGImapper, RGDmapper, HGNCmapper=None, targetPrefix='hgnc:'):
    st = i.lower()
    if st.startswith(targetPrefix):
        hgout = [i[len(targetPrefix):len(i)]]
    elif st.startswith('hgnc:'):
        hgout = HGNCmapper.map(i[5:len(i)])
    elif st.startswith('mgi:'):
        hgout = MGImapper.map(i[4:len(i)])
    elif st.startswith('rgd:'):
        hgout = RGDmapper.map(i[4:len(i)])
    else:
        hgout = [i]
    return hgout


def filterByPrefix(l, targetPrefix='hgnc:'):
    out = []
    for i in l:
        st = i.lower()
        if not st.startswith('bel:'):
            if st.startswith(targetPrefix):
                out.append(i[len(targetPrefix):len(i)])
            else:
                out.append(i)
    return out


class NdexToGeneSif(util.NetworkWrapper):

    def __init__(self, ndexNetwork):
        self.network = ndexNetwork
        self.supportToEdgeMap = {}
        self.citationToSupportMap = {}
        self.nodeLabelMap = {}
        self.termLabelMap = {}
        # new vars
        self.basetermMap = {}
        self.missingBaseterms = []
        self.nodeBaseterms = {}

        for nodeId, node in ndexNetwork['nodes'].iteritems():
            self.nodeLabelMap[int(nodeId)] = self.getNodeLabel(node)
            self.nodeBaseterms[int(nodeId)] = self.getNodeBaseterms(node)

        for edge in ndexNetwork['edges'].values():
            for supportId in edge['supportIds']:
                supports = ndexNetwork['supports']
                support = supports[str(supportId)]
                if supportId in self.supportToEdgeMap:
                    edgeList = self.supportToEdgeMap[supportId]
                else:
                    edgeList = []
                edgeList.append(edge)
                self.supportToEdgeMap[supportId] = edgeList

        for supportId in self.supportToEdgeMap.keys():
            support = ndexNetwork['supports'][str(supportId)]
            citationId = support['citationId']
            if citationId in self.citationToSupportMap:
                supportIdList = self.citationToSupportMap[citationId]
            else:
                supportIdList = []
            supportIdList.append(supportId)
            self.citationToSupportMap[citationId] = supportIdList

    # this is new
    def edgeExpandToSIF(self, edge):
        """Takes an edge and simplifies to gene symbol and interaction type.
        All baseterms associated with subject inherit all interactions with all objects"""
        subjectBasetermList = []
        objectBasetermList = []
        predicateLabel = "missing"
        subjectId = edge['subjectId']
        objectId = edge['objectId']
        if subjectId in self.nodeBaseterms:
            subjectBasetermList = self.nodeBaseterms[subjectId]
        if objectId in self.nodeBaseterms:
            objectBasetermList = self.nodeBaseterms[objectId]
        predicateId = edge['predicateId']
        predicateLabel = util.stripPrefixes(self.getTermLabel(predicateId), targetPrefix=prefix)
        sifTriples = []

        subjMapped = []
        for subj in subjectBasetermList:
            subjMapped.extend(
                mapByPrefix(subj, MGImapper, RGDmapper, HGNCmapper, targetPrefix=prefix))
        subjMapped = filterByPrefix(subjMapped)

        objMapped = []
        for obj in objectBasetermList:
            objMapped.extend(
                mapByPrefix(obj, MGImapper, RGDmapper, HGNCmapper, targetPrefix=prefix))
        objMapped = filterByPrefix(objMapped)

        for subj in subjMapped:
            for obj in objMapped:
                sifTriples.append([subj, predicateLabel, obj])

        return sifTriples

    def getNodeBaseterms(self, node):
        if 'name' in node and node['name']:
            return node['name']

        elif 'represents' in node:
            return self.basetermMap[node['represents']]

        else:
            return "node %s" % (node['id'])

    def writeSIF(self, fileName=None):
        if fileName:
            output = open(fileName, 'w')
        else:
            output = sys.stdout

        for edge in self.network['edges'].values():
            sifs = self.edgeExpandToSIF(edge)
            for s in sifs:
                output.write('\t'.join(s) + '\n')

        if fileName:
            output.close()

    def getTermLabel(self, termId):
        if termId in self.termLabelMap:
            return self.termLabelMap[termId]
        else:
            label = "error"
            term = self.getTermById(termId)
            type = term['type'].lower()
            if type == "baseterm":
                name = term['name']
                if 'namespaceId' in term and term['namespaceId']:
                    namespaceId = term['namespaceId']
                    namespace = self.getNamespaceById(namespaceId)

                    if namespace:
                        if namespace['prefix']:
                            label = "%s:%s" % (namespace['prefix'], name)
                        elif namespace['uri']:
                            label = "%s%s" % (namespace['uri'], name)
                        else:
                            label = name
                    else:
                        label = name
                else:
                    label = name
                self.basetermMap[termId] = [label]

            elif type == "functionterm":
                functionTermId = term['functionTermId']
                functionLabel = self.getTermLabel(functionTermId)
                functionLabel = util.getFunctionAbbreviation(functionLabel)
                parameterLabels = []
                if (termId not in self.basetermMap):
                    self.basetermMap[termId] = []
                for parameterId in term['parameterIds']:
                    parameterLabel = self.getTermLabel(parameterId)
                    parameterLabels.append(parameterLabel)
                    if parameterId in self.basetermMap:
                        self.basetermMap[termId].extend(self.basetermMap[parameterId])
                    else:
                        self.missingBaseterms.append(parameterId)
                label = "%s(%s)" % (functionLabel, ",".join(parameterLabels))

            elif type == "reifiededgeterm":
                edgeId = term['edgeId']
                edges = self.network['edges']
                self.basetermMap[termId] = []
                if edgeId in edges:
                    reifiedEdge = edges[edgeId]
                    label = "(%s)" % (self.getEdgeLabel(reifiedEdge))
                else:
                    label = "(reifiedEdge: %s)" % (edgeId)

            else:
                label = "term: %s" % (termId)
                self.basetermMap[termId] = []

            self.termLabelMap[termId] = label
            return label


def queryVector(query, labels):
    out = {}
    weight_sum = 0.0
    for i in labels:
        if i in query:
            out[i] = 1.0
            weight_sum += 1.0
        else:
            out[i] = 0.0

    for i in labels:
        out[i] = out[i] / weight_sum

    return out


def weightedQueryVector(query, labels, weights):
    out = {}
    weight_sum = 0
    for i in labels:
        if i in query:
            try:
                out[i] = weights[i]
                weight_sum += weights[i]
            except KeyError:
                out[i] = 1
                weight_sum += 1
        else:
            out[i] = 0

    for i in labels:
        out[i] = np.float32(out[i] / weight_sum)

    return out


def readNodeWeights(filename):
    weights = {}
    for line in csv.reader(open(filename, 'rb'), delimiter='\t'):
        weights[line[0]] = float(line[1])
    return weights


def readSif(file_url):
    triples = []
    for line in csv.reader(open(file_url, 'rb'), delimiter='\t'):
        triples.append(line)
    return triples


def filterSif(triples, scores, desired_nodes=30):
    scores_made_the_cut = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[
                          0:(desired_nodes)]
    nodes_made_the_cut = [i[0] for i in scores_made_the_cut]
    edges_made_the_cut = []
    for tr in triples:
        if (tr[0] in nodes_made_the_cut) and (tr[2] in nodes_made_the_cut):
            edges_made_the_cut.append(tr)
    return edges_made_the_cut


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-q", "--query", dest="query", action="store", type="string",
                      help="File containining a list of query genes")
    parser.add_option("-s", "--sif", dest="sif", action="store", type="string", default="out.sif",
                      help="Output file for intermediate sif, translated to HGNC")
    parser.add_option("-k", "--kernel", dest="kernel", action="store", type="string",
                      default="kernel.txt", help="Output file for kernel")
    parser.add_option("-t", "--diffusion-time", dest="diffusion_time", type="float", default=0.1,
                      help="Time parameter (scale) for diffusion.  Default is 0.1")
    parser.add_option("-d", "--diffused-query", dest="diffused_query", type="string",
                      default="diffused.txt", help="Output file for diffused query.")
    parser.add_option("-u", "--username", dest="username", type="string", default=None,
                      help="NDEx username")
    parser.add_option("-p", "--password", dest="password", type="string", default=None,
                      help="NDEx password")
    parser.add_option("-n", "--network-uuid", dest="network_uuid", type="string",
                      default="7e57f74d-a39b-11e4-bda0-000c29202374",
                      help="uuid of query, default is for the BEL large corpus")
    parser.add_option("-m", "--mgi-mapping-table", dest="mgi", type="string",
                      default="bel_MGItoHGNC.tab",
                      help="file with MGI to target species mapping table")
    parser.add_option("-r", "--rgd-mapping-table", dest="rgd", type="string",
                      default="bel_RGDtoHGNC.tab",
                      help="file with RGC to target species mapping table")
    parser.add_option("-H", "--hgnc-mapping-table", dest="hgnc", type="string", default=None,
                      help="file with HGNC to target species mapping table")
    parser.add_option("-b", "--bel-file", dest="bel", type="string", default=None)
    parser.add_option("-S", "--species", dest="species", type="string", default="human",
                      help="Target species to map to.  Default is 'human', other options right now are 'rat' and 'mouse'")

    (opts, args) = parser.parse_args()


    # lib_path = os.path.abspath('/Users/danielcarlin/projects/TieDIE/lib')
    # sys.path.append(lib_path)

    # establishes orthology mappers
    if (opts.species == 'human'):
        MGImapper = TableEntityMapper(opts.mgi)
        RGDmapper = TableEntityMapper(opts.rgd)
        HGNCmapper = None
        prefix = 'hgnc:'
    elif (opts.species == 'mouse'):
        HGNCmapper = TableEntityMapper(opts.hgnc)
        RGDmapper = TableEntityMapper(opts.rgd)
        MGImapper = None
        prefix = 'mgi:'
    elif (opts.species == 'rat'):
        MGImapper = TableEntityMapper(opts.mgi)
        HGNCmapper = TableEntityMapper(opts.hgnc)
        RGDmapper = None
        prefix = 'rgd:'
    else:
        sys.exit("Unrecognized species.  Please choose mouse, rat or human.")


    # read in the query genes and build the request string
    gene_file = opts.query

    f = open(gene_file, 'r')

    get_these = []

    for line in f:
        get_these.append(line.rstrip())

    requestString = " ".join(get_these)

    # establishes connections to ndex.  Search via direct neighbors
    if opts.password is not None:
        myNdex = nc.Ndex("http://ndexbio.org", username='decarlin', password='perfect6')
    else:
        myNdex = nc.Ndex("http://ndexbio.org")

    myNet = myNdex.getNeighborhood(opts.network_uuid, requestString, searchDepth=1)

    network = util.ndexPropertyGraphNetworkToNetworkX(myNet)

    # convert Ndex to sif, mapping orthology and collapsing baseterms
    wrapped = NdexToGeneSif(myNet)

    wrapped.writeSIF(opts.sif)

    if opts.bel is not None:
        wrapped.writeBELScript(fileName=opts.bel)

    # calculates the heat kernel
    ker = SciPyKernel(opts.sif, time_t=opts.diffusion_time)

    ker.writeKernel(opts.kernel)

    # establishes and diffuses the query vector
    queryVec = queryVector(get_these, ker.labels)
    diffused = ker.diffuse(queryVec)

    sorted_diffused = sorted(diffused.items(), key=operator.itemgetter(1), reverse=True)

    writer = csv.writer(open(opts.diffused_query, 'wb'), delimiter='\t')
    for key, value in sorted_diffused:
        writer.writerow([key, value])

    # filter the sif, leaving only interactions between the top N genes
    scores = readNodeWeights(opts.diffused_query)
    ints = readSif(opts.sif)
    filtered = filterSif(ints, scores)

    output = open('filtered.sif', 'wb')
    for s in filtered:
        output.write('\t'.join(s) + '\n')
