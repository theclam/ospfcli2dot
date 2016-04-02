# ospf2dot

Converts the output of Cisco IOS command "show ip ospf database neighbor" into
a GraphViz DOT file.

GraphViz can then plot the DOT file into a vertex / edge style graph depicting
your network topology and the associated OSPF costs. Any asymmetric link costs
(different cost set on each end of the link) show up in red.

This script requires Python 3

Usage - Linux / Mac
===================

Set the ospf2dot.py file as executable (chmod 755 ospf2dot.py) then run it

Usage - Windows
===============

Run python 3 then execute:

exec(open("./ospf2dot.py").read())

Example
=======

foeh@feeble ~ $ ./ospf2dot.py
ospf2dot - takes the output of "show ip ospf database router" and outputs a
GraphViz DOT file corresponding to the network topology

v0.1 alpha, By Foeh Mannay, April 2016

Enter input filename: cli-output.txt
Enter output filename: mytopology.dot
foeh@feeble ~ $

Using DOT files
===============

Several applications can deal with DOT files.

Example: Native graphviz "dot" processor to output a .gif file:

foeh@feeble ~ $ dot -Tgif -omytopology.gif mytopology.dot

(Or use xdot under Linux / gvedit under Windows to see it directly)

Bugs
====

So far I have only tested this againts one device's output. I expect that means
it will break when output from other devices is used :D

Oh, and I won't lie to you, I write terrible Python.
