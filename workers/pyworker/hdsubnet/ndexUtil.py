# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 11:10:59 2014

@author: Dexter Pratt
"""
import sys

import networkx as nx


def ndexNetworkStats(network):

    stats = {}
    stats['nodeCount'] = len(network.get('nodes'))
    stats['edgeCount'] = len(network.get('edges'))
    stats['supports'] = len(network.get('supports'))
    stats['citations'] = len(network.get('citations'))
    stats['properties'] = len(network.get('properties'))
    stats['baseTerms'] = len(network.get('baseTerms'))
    stats['functionTerms'] = len(network.get('functionTerms'))
    stats['reifiedEdgeTerms'] = len(network.get('reifiedEdgeTerms'))
    stats['namespaces'] = len(network.get('namespaces'))
    stats['name'] = network.get('name')
    stats['description'] = network.get('description')
    return stats


# Convert NDEx property graph json to a trivial networkx network
def ndexPropertyGraphNetworkToNetworkX(ndexPropertyGraphNetwork):

    g = nx.MultiDiGraph()
    for node in ndexPropertyGraphNetwork['nodes'].values():
        g.add_node(node['id'])
    for edge in ndexPropertyGraphNetwork['edges'].values():
        g.add_edge(edge['subjectId'], edge['objectId'])
    return g


# This is specific to summarizing a BEL network.
# Need to generalize
def stripPrefixes(input, targetPrefix='hgnc:'):
    st = input.lower()
    if st.startswith('bel:'):
        return input[4:len(input)]
    elif st.startswith(targetPrefix):
        return input[len(targetPrefix):len(input)]
    else:
        return st


# This is BEL specific, since BEL is the only current user of funciton terms
def getFunctionAbbreviation(input):
    st = input.lower()
    fl = stripPrefixes(st)
    if fl == "abundance":
        return "a"
    elif fl == "biological_process":
        return "bp"
    elif fl == "catalytic_activity":
        return "cat"
    elif fl == "complex_abundance":
        return "complex"
    elif fl == "pathology":
        return "path"
    elif fl == "peptidase_activity":
        return "pep"
    elif fl == "protein_abundance":
        return "p"
    elif fl == "rna_abundance":
        return "r"
    elif fl == "protein_modification":
        return "pmod"
    elif fl == "transcriptional_activity":
        return "tscript"
    elif fl == "molecular_activity":
        return "act"
    elif fl == "degradation":
        return "deg"
    elif fl == "kinase_activity":
        return "kin"
    elif fl == "substitution":
        return "sub"
    else:
        return fl


class NetworkWrapper:

    def __init__(self, ndexNetwork):
        self.network = ndexNetwork
        self.supportToEdgeMap = {}
        self.citationToSupportMap = {}
        self.nodeLabelMap = {}
        self.termLabelMap = {}

        for nodeId, node in ndexNetwork['nodes'].iteritems():
            self.nodeLabelMap[int(nodeId)] = self.getNodeLabel(node)

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

    def getEdgeLabel(self, edge):
        subjectLabel = "missing"
        objectLabel = "missing"
        predicateLabel = "missing"
        subjectId = edge['subjectId']
        objectId = edge['objectId']
        if subjectId in self.nodeLabelMap:
            subjectLabel = self.nodeLabelMap[subjectId]
        if objectId in self.nodeLabelMap:
            objectLabel = self.nodeLabelMap[objectId]
        predicateId = edge['predicateId']
        predicateLabel = stripPrefixes(self.getTermLabel(predicateId))
        label = "%s %s %s" % (subjectLabel, predicateLabel, objectLabel)
        return label

    def getNodeLabel(self, node):
        if 'name' in node and node['name']:
            return node['name']

        elif 'represents' in node:
            return self.getTermLabel(node['represents'])

        else:
            return "node %s" % (node['id'])

    def getTermById(self, termId):
        termIdStr = str(termId)
        if termIdStr in self.network['baseTerms']:
            return self.network['baseTerms'][termIdStr]
        elif termIdStr in self.network['functionTerms']:
            return self.network['functionTerms'][termIdStr]
        elif termIdStr in self.network['reifiedEdgeTerms']:
            return self.network['reifiedEdgeTerms'][termIdStr]
        else:
            return None

    def getNamespaceById(self, namespaceId):
        namespaceIdStr = str(namespaceId)
        if namespaceIdStr in self.network['namespaces']:
            return self.network['namespaces'][namespaceIdStr]

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

            elif type == "functionterm":
                functionTermId = term['functionTermId']
                functionLabel = self.getTermLabel(functionTermId)
                functionLabel = getFunctionAbbreviation(functionLabel)
                parameterLabels = []
                for parameterId in term['parameterIds']:
                    parameterLabel = self.getTermLabel(parameterId)
                    parameterLabels.append(parameterLabel)
                label = "%s(%s)" % (functionLabel, ",".join(parameterLabels))

            elif type == "reifiededgeterm":
                edgeId = term['edgeId']
                edges = self.network['edges']
                if edgeId in edges:
                    reifiedEdge = edges[edgeId]
                    label = "(%s)" % (self.getEdgeLabel(reifiedEdge))
                else:
                    label = "(reifiedEdge: %s)" % (edgeId)

            else:
                label = "term: %s" % (termId)

            self.termLabelMap[termId] = label
            return label

    def writeBELScript(self, fileName=None):
        if fileName:
            output = open(fileName, 'w')
        else:
            output = sys.stdout


            # Print definitions in header
        output.write('\n# Definitions Section\n')

        # Print namespaces
        for _, ns in self.network['namespaces'].iteritems():
            if ns['uri'].endswith('.belns'):
                output.write('DEFINE NAMESPACE %s AS URL "%s"\n' % (ns['prefix'], ns['uri']))

                # Print annotations
        for _, ann in self.network['namespaces'].iteritems():
            if ann['uri'].endswith('.belanno'):
                output.write('DEFINE ANNOTATION %s AS URL "%s"\n' % (ann['prefix'], ann['uri']))

                # Print BEL statements
        output.write('\n#Statements section\n')

        print
        print 'Unhandled statements'
        print '===================='

        # Iterate by citation
        for citationId, supportIdList in self.citationToSupportMap.iteritems():
            # Start a group for each citation
            output.write('\nSET STATEMENT_GROUP = "Group %d"\n' % citationId)
            try:
                citation = self.network['citations'][str(citationId)]
                citation_title = citation['title']
                citation_terms = citation['identifier'].split(':')
                if citation_terms[0] == 'pmid':
                    citation_type = 'PubMed'
                    citation_id = citation_terms[1]
                else:
                    citation_type = 'N/A'
                    citation_id = citation['identifier']
                output.write(('SET Citation = {"%s","%s","%s"}\n' % (
                citation_type, citation_title, citation_id)).encode('utf8', 'replace'))
            except KeyError:
                output.write('SET Citation = {"","",""}\n')

                # Iterate by evidence within each citation
            for supportId in supportIdList:
                support = self.network['supports'][str(supportId)]
                supportText = support['text'].replace('"', '').replace('\n', ' ')
                output.write((u'\nSET Evidence = "%s"\n' % supportText).encode('utf8', 'replace'))
                edgeList = self.supportToEdgeMap[supportId]
                # Print BEL statements 
                for edge in edgeList:
                    outstr = self.getEdgeLabel(edge)
                    if outstr.find('missing') != -1:
                        continue

                        # Generate valid translocation statements - not used
                        # outstr = re.sub(r'GOCCACC:GO:(\d+),GOCCACC:GO:(\d+)',r'fromLoc(GOCCACC:\1),toLoc(GOCCACC:\2)',outstr)

                    # Reified edges not handled
                    if outstr.find('reifiedEdge') == -1:
                        # Translocation not handled
                        if outstr.find('translocation') == -1:
                            # 'None' modifiers not handled
                            if outstr.find('None') == -1:
                                output.write("%s\n" % outstr)
                            else:
                                print outstr
                        else:
                            print outstr
                    else:
                        print outstr
                output.write('\nUNSET STATEMENT_GROUP\n')
        if fileName:
            output.close()

    def writeSummary(self, fileName=None):
        if fileName:
            output = open(fileName, 'w')
        else:
            output = sys.stdout

        for citationId, supportIdList in self.citationToSupportMap.iteritems():
            citations = self.network['citations']
            citation = citations[str(citationId)]
            citationId = citation['identifier']
            # Write Citation
            output.write(
                "\n=========================================================================\n")
            output.write("        Citation: %s\n" % (citationId))
            output.write(
                "=========================================================================\n\n")

            for supportId in supportIdList:
                support = self.network['supports'][str(supportId)]
                # Write Support
                output.write("_______________________________\n")
                output.write("Evidence: %s\n\n" % support['text'])

                edgeList = self.supportToEdgeMap[supportId]
                for edge in edgeList:
                    # Write Edge
                    output.write("       %s\n" % self.getEdgeLabel(edge))
                    for pv in edge['properties']:
                        output.write(
                            "                %s: %s\n" % (pv['predicateString'], pv['value']))

        if fileName:
            output.close()
