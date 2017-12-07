# ospfcli2dot

Converts the output of Cisco IOS command "show ip ospf database router" into
a GraphViz DOT file.

GraphViz can then plot the DOT file into a vertex / edge style graph depicting
your network topology and the associated OSPF costs. Any asymmetric link costs
(different cost set on each end of the link) show up in red.

The script seems to also work with the output of Cisco ASAs and IOS-XE (it is 
basically identical to that of IOS).

Support has been added for broadcast networks. At the moment it just shows the DR as
opposed to the full network / mask as this information in not available in the output of
"show ip ospf database router". I may add support to populate the missing details from
the output of "show ip ospf network" later.

This release adds support for a unix format hostfile, if the router isn't able
to resolve the hostnames for itself, and also allows automatic group creation
based on hostnames. Simply tell it what your separator is and whether to use the
first or last part as the site ID. Simple but handles common hostname formats
like "rtr1.site" or "site-rtr1".

This script requires Python 3.

Usage - Linux / Mac
===================

Set the ospfcli2dot.py file as executable (chmod 755 ospfcli2dot.py) then run it

Usage - Windows
===============

Run python 3 then execute:

exec(open("./ospfcli2dot.py").read())

Example
=======

foeh@feeble ~ $ ./ospfcli2dot.py
ospfcli2dot - takes the output of "show ip ospf database router" and optionally a hostfile
outputs a GraphViz DOT file corresponding to the network topology

v0.3 alpha, By Foeh Mannay, December 2017

Enter input filename: cli-output.txt
Enter hostnames file or press enter to continue without one: hosts
If you want to group by hostname, enter the separator now
 (or press enter to continue): -
Do you want to group by the [f]irst or [l]ast part of the hostname? f
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

My Python is pretty scruffy but it seems to work.
