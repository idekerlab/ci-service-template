import automateHeatKernel as ahk
import multiplyEstablishedKernel as mek
import os

# This service gets an annotated node network
# typically derived from an uploaded TSV
# and uses a reference network to find a
# relevant subnetwork.  The annotations are
# applied to the subnetwork and it is returned
# as CX network as the result of the job


KERNEL_LOCATION = 'resource/kernel.txt'
NETWORK_LOCATION = 'resource/underlying_network.sif'

k_file = os.path.abspath(os.path.dirname(__file__)) + '/' + KERNEL_LOCATION
net_file = os.path.abspath(os.path.dirname(__file__)) + '/' + NETWORK_LOCATION
sif = ahk.readSif(net_file)
ker = mek.EstablishedKernel(k_file)


class SubNetworkFinder():

    def __init__(self, kernel_url, network_url):
        self.__sif = ahk.readSif(network_url)
        self.__ker = mek.EstablishedKernel(kernel_url)

    def __sif2cx(self, triples, scores=None):

        cx_out = []
        identifierToNodeIdMap = {}

        id_counter = 1000

        for tr in triples:
            subj_node_id = identifierToNodeIdMap.get(tr[0])
            obj_node_id = identifierToNodeIdMap.get(tr[2])

            if not subj_node_id:
                subj_node_id = "_" + str(id_counter)
                id_counter = id_counter + 1
                identifierToNodeIdMap[tr[0]] = subj_node_id
                cx_out.append({"nodes": [{"@id": subj_node_id}]})
                cx_out.append({"nodeIdentities": [{"node": subj_node_id, "represents": tr[0]}]})

            if not obj_node_id:
                obj_node_id = "_" + str(id_counter)
                id_counter = id_counter + 1
                identifierToNodeIdMap[tr[2]] = obj_node_id
                cx_out.append({"nodes": [{"@id": obj_node_id}]})
                cx_out.append({"nodeIdentities": [{"node": obj_node_id, "represents": tr[2]}]})

            cx_out.append(
                {
                    "edges": [
                        {
                            "source": subj_node_id, "@id": "_" + str(id_counter),
                            "target": obj_node_id
                        }
                    ],
                    "edgeIdentities": [
                        {
                            "edge": "_" + str(id_counter),
                            "relationship": tr[1]
                        }
                    ]
                }
            )
            id_counter = id_counter + 1

        if scores:
            for node_name, value in scores.iteritems():
                node_id = identifierToNodeIdMap.get(node_name)
                if node_id:
                    cx_out.append({"elementProperties": [{"node": node_id,
                                                          "property": "subnet_finder_score",
                                                          "value": value}]})
        return cx_out

    def get_sub_network(self, identifiers):
        query_vector = ahk.queryVector(identifiers, ker.labels)
        diffused = ker.diffuse(query_vector)
        filtered = ahk.filterSif(sif, diffused)

        return self.__sif2cx(filtered, scores=diffused)
