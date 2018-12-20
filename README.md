# DataViz
## Description
Simple and not very efficient realization of layered drawing of digraphs.

**Literature**: "Graph Drawing, Algorithms for the Visualization of Graphs", Battista, Eades, Tamassia, Tollis. Chapter 9, "Layered Drawings of Digraphs".

## Requirements
* python >= 3.4
* networkx 
* maybe also pygraphviz and pydot

## Usage
**python graph.py --file <path_to_file_with_graph>**

Each line in the file should have one of the formats:
* \<v1> \<v2> -- edge between vertices 'v1' and 'v2'
* \<u> -- separate vertex 'u'

Or you can just call **python graph.py** and try to draw my sample.

## Outputs
All pictures would be in the directory 'outputs'. 

## Samples
[Output pictures for sample graph](../outputs/samples)
