# frr-ospfclitdot
Based onthe orifinal with fixes 
frr-ospfcli2dot - takes the output of "show ip ospf database router"and optionally a hostfile
outputs a GraphViz DOT file corresponding to the network topology

usage: frr-ospfcli2dot [-h] [--hosts_file HOSTS_FILE]

                       [--ip_decimal IP_DECIMAL] [--add_stubs ADD_STUBS]
                       
                       [--force_output FORCE_OUTPUT]
                       
                       source_file destination_file

Extract Topology from OSPF

positional arguments:

  source_file           The file name for the input OSPF Database text file
  
  destination_file      The file name for the output dot file

optional arguments:

  -h, --help            show this help message and exit
  
  --hosts_file HOSTS_FILE
  
                        The file name for the input Host Names Database text
                        
                        file
  --ip_decimal IP_DECIMAL
  
                        Print IP in decimal format
                        
  --add_stubs ADD_STUBS
  
                        Print Stub networks in node
                        
  --force_output FORCE_OUTPUT
  
                        Don't check for output file
                        

This is the original - for other OS.

# ospfcli2dot

Converts the output of Cisco IOS command "show ip ospf database router" into
a GraphViz DOT file.

GraphViz can then plot the DOT file into a vertex / edge style graph depicting
your network topology and the associated OSPF costs. Any asymmetric link costs
(different cost set on each end of the link) show up in red.

The script seems to also work with the output of Cisco ASAs and IOS-XE (it is 
basically identical to that of IOS).

Support has been added for broadcast networks. At the moment it just shows the DR as
opposed to the full network / mask as this information is not available in the output of
"show ip ospf database router". I may add support to populate the missing details from
the output of "show ip ospf network" later.

This release adds support for a unix format hostfile, if the router isn't able
to resolve the hostnames for itself, and also allows automatic group creation
based on hostnames. Simply tell it what your separator is and whether to use the
first or last part as the site ID. Simple but handles common hostname formats
like "rtr1.site" or "site-rtr1".

The script juni-ospfcli2dot.py takes the output of "show ospf database extensive" on
JunOS devices and performs the same function.

These scripts require Python 3.

Usage - Linux / Mac
===================

Set all python files as executable (chmod 755 *.py) then run

Usage - Windows
===============

Run python 3 then execute:

exec(open("./ospfcli2dot.py").read())

Example
=======

foeh@feeble ~ $ ./ospfcli2dot.py
ospfcli2dot - takes the output of "show ip ospf database router" and optionally a hostfile
outputs a GraphViz DOT file corresponding to the network topology

v0.4 alpha, By Foeh Mannay, September 2018

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

Not really my bug but the output of this script is *really* good at upsetting the
graphviz "Error: trouble in init_rank" bug - I was pulling my hair out with this for
the longest time but they have now fixed the layout engine. Upgrade to v1.4 or later
and it should magically go away.


