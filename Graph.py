class UnweightedGraph:
	def __init__(self):
		self.nodes = list()
		self.connections = list()
		self.connectedNodes = set()
	
	def printGraph(self):
		'''Prints graph as an adjacency list'''
		print("Node\t\tConnected")
		print("--------------------------------")
		#Iterates through the node list
		for node in self.nodes:
			print(str(node.value) + "\t\t", end='')
			count = 0
			#Prints adjacent nodes for current node
			for connected in node.connectedTo:
				if count == (len(node.connectedTo) - 1):
					print(str(connected.value))
				else:
					print(str(connected.value) + ", ", end = '')
					count += 1
	
	def addNode(self, nodeVal):
		'''Adds a node to the graph
		   Takes a positive integer as an argument'''
		if isinstance(nodeVal, int) and nodeVal >= 0:
			#Uses a boolean to track if the node is already in the graph
			self.marker = False
			for node in self.nodes:
				if nodeVal == node.value:
					print("Node already exists")
					self.marker = True
					break
			if not self.marker:
				#If node does not exist, create it
				self.node = GraphNode(nodeVal)
				self.nodes.append(self.node)
		else:
			#Raise error if invalid value is given
			raise ValueError("Value given is not a positive integer")
			
	def removeNode(self, nodeVal):
		'''Removes a node from the graph
		   Takes a node's integer value as an argument'''
		self.nodeRef = None
		for node in self.nodes:
			if node.value == nodeVal:
				self.nodeRef = node
				break
			else:
				continue
		
		#If node is not in the graph, an error is raised
		if self.nodeRef == None:
			raise ValueError("Node does not exist in the graph, operation unable to complete")
		else:
			#Removes any connections to the node being deleted
			for connection in self.connections:
				if self.nodeRef in connection:
					self.node1 = connection[0]
					self.node2 = connection[1]
					self.removeConnection(self.node1, self.node2)
				else:
					continue
			#Removes the node itself from the node list
			self.nodes.remove(self.nodeRef)
		
	def addConnection(self, node1, node2):
		'''Adds a connection to the graph
		   Can take the nodes as arguments in two ways, either:
			   Give the integer values of the nodes
			   Or give the node objects themselves'''
		self.nodeRef1 = None
		self.nodeRef2 = None
		#Finds the nodes within the graph and creates references to them
		for node in self.nodes:
			if node1 == node.value:
				self.nodeRef1 = node
			elif node2 == node.value:
				self.nodeRef2 = node
			else:
				continue
		#If either node is not in the graph, an error is raised
		if self.nodeRef1 == None or self.nodeRef2 == None:
			raise ValueError("One or more nodes does not exist in the graph, operation unable to complete")
		#If both nodes are found in the graph the connection is created in the Graph and in each of the nodes
		else:
			self.connections.append((self.nodeRef1, self.nodeRef2))
			self.nodeRef1.connectedTo.append(self.nodeRef2)
			self.nodeRef2.connectedTo.append(self.nodeRef1)
			
	def removeConnection(self, node1, node2):
		'''Removes a connection from the graph
		   Can take the nodes as arguments in two ways, either:
			   Give the integer values of the nodes
			   Or give the node objects themselves'''
		if isinstance(node1, GraphNode) and isinstance(node2, GraphNode):
			self.nodeRef1 = node1
			self.nodeRef2 = node2
		else:
			self.nodeRef1 = None
			self.nodeRef2 = None
			#Finds the nodes within the graph and creates references to them
			for node in self.nodes:
				if node1 == node.value:
					self.nodeRef1 = node
				elif node2 == node.value:
					self.nodeRef2 = node
				else:
					continue
		#If either node is not in the graph, an error is raised
		if self.nodeRef1 == None or self.nodeRef2 == None:
			raise ValueError("One or more nodes does not exist in the graph, operation unable to complete")
		else:
			#If both nodes are found then the connection is removed from the graph
			for connection in self.connections:
				if connection == (self.nodeRef1, self.nodeRef2):
					self.connections.remove((self.nodeRef1, self.nodeRef2))
					break
				elif connection == (self.nodeRef2, self.nodeRef1):
					self.connections.remove((self.nodeRef2, self.nodeRef1))
					break
				else:
					continue
			#Removes the connections from the nodes themselves
			self.nodeRef1.connectedTo.remove(self.nodeRef2)
			self.nodeRef2.connectedTo.remove(self.nodeRef1)
			
	def isPath(self, start, destination):
		'''Checks if there is a path between two nodes
		   and prints it out if it finds one'''
		self.startNode = None
		self.destNode = None
		#Finds the nodes within the graph and creates references to them
		for node in self.nodes:
			if start == node.value:
				self.startNode = node
			elif destination == node.value:
				self.destNode = node
			else:
				continue
		#If either node is not in the graph, an error is raised
		if self.startNode == None or self.destNode == None:
			raise ValueError("One or more nodes does not exist in the graph, operation unable to complete")
		else:
			self.path = list()
			#Checks if either node is unconnected
			if (not self.startNode.connectedTo) or (not self.destNode.connectedTo):
				self.connected = False
			
			self.connected = self.traversal(self.startNode, self.destNode)
			if self.connected:
				self.path = self.traversed
			
			#Sets the output for when the graph is not connected
			if not self.connected:
				self.path.append("No Path Exists")
				
			#Prints the path (or lack of) to the Path.txt file
			self.pathFile = open("Path.txt", 'w')
			self.pathFile.write("Path from: " + str(self.startNode.value) + " to " + str(self.destNode.value) + "\n")
			if self.path[0] == "No Path Exists":
				self.pathFile.write(self.path[0])
			else:
				self.count = 0
				for word in self.path:
					if self.count == (len(self.path) - 1):
						self.pathFile.write(str(word.value))
					else:
						self.pathFile.write(str(word.value) + "\n")
						self.count += 1

			#Closes the file and resets the list
			self.pathFile.close()
			self.traversed = list()
	
	def traversal(self, start, end):
		'''Recursive traversal through the graph,
		   similar to DFS traversal
		   
		   Takes a start and end node object'''
		self.node = start
		if self.node == end:
			#If node is the target end traversal
			self.traversed.append(self.node)
			return True
		elif set(self.traversed) == set(self.nodes):
			#If node is not found
			return False
		
		if self.node not in self.traversed:
			self.traversed.append(self.node)
		
		for node in self.node.connectedTo:
			if node not in self.traversed:
				if self.traversal(node, end):
					return True
				else:
					self.traversed.remove(node)
					continue
				
	def isConnected(self, startNode = None):
		'''Checks if a graph is connected or not
		   Takes a node object as an argument, if not
		   provided it starts from the first one in the
		   node list'''
		#Creates starting node if not given
		if startNode == None:
			self.startNode = self.nodes[0]
			
		#If the start node has no neighbours the graph is not connected
		if not self.startNode.connectedTo:
			return "No"
		
		#Adds first number to set
		self.connectedNodes.add(self.startNode)
		#Runs recursive function to explore all connections
		self.findConnections(self.startNode)
				
		self.connected = True
		for node in self.nodes:
			#Checks if any node was missed during connection check
			if node not in self.connectedNodes:
				self.connected = False
				break
		if self.connected:
			#Resets the connectedNodes set and returns yes
			self.connectedNodes = set()
			return "Yes"
		else:
			#Resets the connectedNodes set and returns no
			self.connectedNodes = set()
			return "No"
		
	def findConnections(self, startNode):
		'''Recursively searches through all connections of
		   each node'''
		self.start = startNode
		for node in self.start.connectedTo:
			#If node has not been checked yet
			if node not in self.connectedNodes:
				self.connectedNodes.add(node)
				self.findConnections(node)
				
	def BFS(self, startNode = None):
		'''Runs a Breadth First Search on a graph
		   Will start from first node in list if not
		   otherwise given a node object as an argument'''
		#Creates starting node if not given
		if startNode == None:
			self.start = self.nodes[0]
		else:
			self.start = startNode
		#Sets up the empty lists and sets
		self.traversed = list()
		self.checked = set()
		#Marks start node as visited
		self.traversed.append(self.start)
		#Runs the recursive traversal
		self.BFSTraversal(self.start)
		
		#Prints to the BFS.txt file
		self.file = open("BFS.txt", 'w')
		self.output = ""
		for node in self.traversed:
			if self.traversed.index(node) == (len(self.traversed) - 1):
				self.output = self.output + str(node.value)
			else:
				self.output = self.output + str(node.value) + "\n"
		self.file.write(self.output)
		
		#Closes file and resets list
		self.file.close()
		self.traversed = list()
		
	def BFSTraversal(self, node):
		'''Recursive traversal of graph for a
		   Breadth First Search
		   Takes a node object as an argument'''
		self.node = node
		for connected in self.node.connectedTo:
			if connected not in self.traversed:
				self.traversed.append(connected)
		self.checked.add(node)
		
		if set(self.traversed) == set(self.nodes):
			#Stops when all nodes have been visited
			return None
		else:
			self.inList = False
			self.i = 0
			while not self.inList:
				if self.traversed[self.i] not in self.checked:
					self.inList = True
				else:
					self.i += 1
			self.BFSTraversal(self.traversed[self.i])
			
	def DFS(self, startNode = None):
		'''Runs a Depth First Search on a graph
		   Will start from first node in list if not
		   otherwise given a node object as an argument'''
		#Creates starting node if not given
		if startNode == None:
			self.start = self.nodes[0]
		else:
			self.start = startNode
			
		self.traversed = list()
		#Runs recursive traversal
		self.DFSTraversal(self.start)
		
		#Prints to file
		self.file = open("DFS.txt", 'w')
		self.output = ""
		for node in self.traversed:
			if self.traversed.index(node) == (len(self.traversed) - 1):
				self.output = self.output + str(node.value)
			else:
				self.output = self.output + str(node.value) + "\n"
		self.file.write(self.output)
		
		#Closes file and resets list
		self.file.close()
		self.traversed = list()
	
	def DFSTraversal(self, node):
		'''Recursive traversal of graph for
		   Depth First Search
		   
		   Takes a node object as an argument'''
		self.node = node
		if node not in self.traversed:
			#Adds unvisited nodes to the visited nodes
			self.traversed.append(self.node)
			
		#Recursive call for any node not traversed yet
		for node in self.node.connectedTo:
			if node not in self.traversed:
				self.DFSTraversal(node)
				
		
				

class GraphNode:
	def __init__(self, nodeValue):
		'''Creates the node objects'''
		self.value = nodeValue
		self.connectedTo = list()

if __name__ == "__main__":
	graph = UnweightedGraph()
	graph.addNode(1)
	graph.addNode(2)
	graph.addNode(3)
	graph.addNode(4)
	graph.addNode(5)
	print(graph.isConnected())
	print("-------------------------")
	graph.addConnection(1, 2)
	graph.addConnection(1, 3)
	graph.addConnection(2, 3)
	graph.addConnection(2, 5)
	graph.addConnection(3, 4)
	graph.addConnection(4, 5)
	graph.printGraph()
	print("-------------------------")
	graph.BFS()
	print("-------------------------")
	graph.DFS()
	print("-------------------------")
	graph.isPath(1, 4)
	print("-------------------------")
	nodeA = graph.nodes[0]
	print(graph.nodes)
	print(nodeA.connectedTo)
	print("-------------------------")
	print(graph.isConnected())
	print("-------------------------")
	graph.removeNode(2)
	print(graph.nodes)
	print(nodeA.connectedTo)
	print("-------------------------")
	
