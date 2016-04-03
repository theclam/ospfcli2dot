#!/usr/bin/python3

# ospf2dot - by Foeh Mannay
#
# Converts the output of the "show ip ospf database router" command into a GraphViz DOT 
# file.
#
# The DOT file can then be used to automatically plot network topology diagrams and, while
# the layout can often leave a lot to be desired, it is very easy to spot asymmetric OSPF
# costs and other anomalies. Routers are enumerated first so you can group them by hand if
# you so desire.

import re

def toslash(str):
	# Dictionary to convert masks to slash notation
	return {
		'0.0.0.0':			'/0',
		'128.0.0.0':		'/1',
		'192.0.0.0':		'/2',
		'224.0.0.0':		'/3',
		'240.0.0.0':		'/4',
		'248.0.0.0':		'/5',
		'252.0.0.0':		'/6',
		'254.0.0.0':		'/7',
		'255.0.0.0':		'/8',
		'255.128.0.0':		'/9',
		'255.192.0.0':		'/10',
		'255.224.0.0':		'/11',
		'255.240.0.0':		'/12',
		'255.248.0.0':		'/13',
		'255.252.0.0':		'/14',
		'255.254.0.0':		'/15',
		'255.255.0.0':		'/16',
		'255.255.128.0':	'/17',
		'255.255.192.0':	'/18',
		'255.255.224.0':	'/19',
		'255.255.240.0':	'/20',
		'255.255.248.0':	'/21',
		'255.255.252.0':	'/22',
		'255.255.254.0':	'/23',
		'255.255.255.0':	'/24',
		'255.255.255.128':	'/25',
		'255.255.255.192':	'/26',
		'255.255.255.224':	'/27',
		'255.255.255.240':	'/28',
		'255.255.255.248':	'/29',
		'255.255.255.252':	'/30',
		'255.255.255.254':	'/31',
		'255.255.255.255':	'/32',
	}[str]

def toDecimal(addr):
	# Converts an IP address to a decimal
	addrlist = addr.split('.')
	return(int(addrlist[3]) + 256 * (int(addrlist[2]) + 256 * (int(addrlist[1]) + 256 * int(addrlist[0]))))
	
def sameP2P(addr1, addr2):
	# Returns true if the two addresses provided are one apart (assume same /30 or /31 network)
	if(abs(toDecimal(addr1) - toDecimal(addr2)) == 1):
		return True
	else:
		return False
	
def Reduce(list):
	# Takes a list of links and merges entries for two ends of the same link, provided the metric matches
	l = 0
	while(l < len(list) - 1):
		if(list[l][0] == list[l+1][1] and list[l+1][0] == list[l][1] and sameP2P(list[l][2], list[l+1][2]) and list[l][3] == list[l+1][3]):
			# if two links are A->B and B->A and in same subnet and have same metric then merge into an undirected edge
			list[l][4]='none'
			list.remove(list[l+1])
		l = l + 1
	return(list)

def mergeSort(list):
	# Performs a standard merge sort on a list of link entries based on IP address
	sorted = []
	listlen = len(list)
	i = 0
	j = 0
	
	if(listlen > 1):
		# If we have 2 or more items, split the list and merge sort each half
		left=mergeSort(list[:listlen//2])
		right=mergeSort(list[listlen//2:])
		# Then merge the two sorted halves together
		while(i < len(left) and j < len(right)):
			if(toDecimal(left[i][2]) < toDecimal(right[j][2])):
				sorted.append(left[i])
				i = i + 1
			else:
				sorted.append(right[j])
				j = j + 1
		while(i < len(left)):
			sorted.append(left[i])
			i = i + 1
		while(j < len(right)):
			sorted.append(right[j])
			j = j + 1
	else:
		sorted = list
	return(sorted)

class Router:
	# Class to store a single router's identity, stub networks and links
	def __init__(self, rid):
		self.routerid = rid
		self.hostname = rid
		self.stubs = []
		self.links = []
		self.transits = []
	
	def sethostname(self, str):
		self.hostname = str
	
	def addstub(self, subnet, mask, metric):
		self.stubs.append([subnet, mask, metric])
	
	def addlink(self, neighbour, ip, metric):
		self.links.append([neighbour, ip, metric])
	
	def addtransit(self, dr, metric):
		self.transits.append([dr, metric])
		
	def dottifyrouter(self):
		# Produces a DOT representation of the router this object represents
		rv = ('\th' + re.sub('\.','x',self.routerid) + ' [label="' + self.routerid)
		if(self.routerid != self.hostname):
			rv = rv + '\\n' + self.hostname
		# Unhash this if you want all stubs to be listed on your nodes
		#for i in self.stubs:
		#	rv += ('\n' + i[0] + toslash(i[1]))
		rv +=('"]\n')
		return(rv)

routers=[]
links=[]
transits=[]

print("ospf2dot - takes the output of \"show ip ospf database router\" and outputs a GraphViz DOT file corresponding to the network topology\n")
print("v0.2 alpha, By Foeh Mannay, April 2016\n")

filename = input("Enter input filename: ")
neighbour = None
stubnet = None
transit = None

with open(filename, 'r') as infile:
	for line in infile:
		m = re.search('Link State ID: (\d*.\d*.\d*.\d*)', line)
		if(m):
			rtr=Router(m.group(1))
			routers.append(rtr)
			continue
		m = re.search('Advertising Router: (\S*)', line)
		if(m):
			rtr.sethostname(m.group(1))
			continue
		m = re.search('\(Link ID\) Network/subnet number: (\d*.\d*.\d*.\d*)', line)
		if(m):
			stubnet = m.group(1)
			continue
		m = re.search('\(Link Data\) Network Mask: (\d*.\d*.\d*.\d*)', line)
		if(m):
			stubmask = m.group(1)
			continue
		m = re.search('\(Link ID\) Neighboring Router ID: (\d*.\d*.\d*.\d*)', line)
		if(m):
			neighbour = m.group(1)
			continue
		m = re.search('\(Link Data\) Router Interface address: (\d*.\d*.\d*.\d*)', line)
		if(m):
			interfaceip = m.group(1)
			continue
		m = re.search('\(Link ID\) Designated Router address: (\d*.\d*.\d*.\d*)', line)
		if(m):
			transit = m.group(1)
			continue
		m = re.search('TOS 0 Metrics: (\d*)', line)
		if(m):
			if(neighbour is not None):
				rtr.addlink(neighbour, interfaceip, m.group(1))
				neighbour = None
				interfaceip = None
			elif(stubnet is not None):
				rtr.addstub(stubnet, stubmask, m.group(1))
				stubnet = None
				stubmask = None
			elif(transit is not None):
				if(transit not in transits):
					transits.append(transit)
				rtr.addtransit(transit, m.group(1))
				transit = None
			continue

filename = input("Enter output filename: ")
with open(filename, 'w') as outfile:
	outfile.write("digraph Topology {\n")
	for r in routers:
		# Ask each Router object in turn to describe itself
		outfile.write(r.dottifyrouter())
	for t in transits:
		# Create items for transit networks
		outfile.write('\tt' + re.sub('\.','x',t) + ' [label="LAN with DR\\n' + t + '", shape=box]\n')
	for r in routers:
		for t in r.transits:
			# Dump transit connections
			outfile.write('\th' + re.sub('\.','x',r.routerid) + ' -> t' + re.sub('\.','x',t[0]) + '[label="' + t[1] + '"]\n')
		for l in r.links:
			# Create a list of all router links (src, dest, IP, metric, style)
			links.append([r.routerid, l[0], l[1], l[2], 'forward color="red"'])
	for l in Reduce(mergeSort(links)):
		# Pair up symmetrically costed links (so we get an undirected edge rather than two directed edges) then output to the DOT file 
		outfile.write('\th' + re.sub('\.','x',l[0]) + ' -> h' + re.sub('\.','x',l[1]) + '[label="' + l[3] + '", dir=' + l[4] + ']\n')
	outfile.write("}\n")

