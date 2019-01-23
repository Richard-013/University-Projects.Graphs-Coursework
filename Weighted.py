class WeightedGraph:
	def __init__(self):
		self.nodes = list() #List of all nodes in graph
		self.connections = list() #List of all connections in graph
		
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
				self.node = GraphNode(nodeVal)
				self.nodes.append(self.node)
		else:
			#If the value is not a +ve int an error raised
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
			for connection in self.connections:
				if self.nodeRef in connection:
					self.node1 = connection[0]
					self.node2 = connection[1]
					self.removeConnection(self.node1, self.node2, connection[2])
				else:
					continue
			self.nodes.remove(self.nodeRef)
		
	def addConnection(self, node1, node2, weight):
		'''Adds a connection to the graph
		   Can take the nodes as arguments in two ways, either:
			   Give the integer values of the nodes
			   Or give the node objects themselves
			   
		   Weight however must be a positive integer'''
		self.nodeRef1 = None
		self.nodeRef2 = None
		if weight == None:
			self.weight = 0
		else:
			self.weight = weight
		#Finds the nodes within the graph and creates references to them
		for node in self.nodes:
			if node1 == node.value:
				self.nodeRef1 = node
			elif node2 == node.value:
				self.nodeRef2 = node
			else:
				continue
				
		#If the weight is not an integer, an error is raised
		if not isinstance(self.weight, int):
			raise ValueError("Weight must be an integer value")
		#If either node is not in the graph, an error is raised
		if self.nodeRef1 == None or self.nodeRef2 == None:
			raise ValueError("One or more nodes does not exist in the graph, operation unable to complete")
		#If both nodes are found in the graph the connection is created in the Graph and in each of the nodes
		else:
			self.connections.append((self.nodeRef1, self.nodeRef2, self.weight))
			self.nodeRef1.connectedTo.append((self.nodeRef2, self.weight))
			self.nodeRef2.connectedTo.append((self.nodeRef1, self.weight))
	
	#Takes weight as there can be multiple direct routes between two nodes of different distances/weights
	def removeConnection(self, node1, node2, weight):
		'''Removes a connection from the graph
		   Can take the nodes as arguments in two ways, either:
			   Give the integer values of the nodes
			   Or give the node objects themselves
			   
		   Weight however must be a positive integer and match the weight
		   of the connection you want to remove'''
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
		
		self.weight = weight
		
		#If either node is not in the graph, an error is raised
		if self.nodeRef1 == None or self.nodeRef2 == None:
			raise ValueError("One or more nodes does not exist in the graph, operation unable to complete")
		else:
			#If both nodes are found then the connection is removed from the graph
			for connection in self.connections:
				if connection == (self.nodeRef1, self.nodeRef2, self.weight):
					self.connections.remove((self.nodeRef1, self.nodeRef2, self.weight))
					break
				elif connection == (self.nodeRef2, self.nodeRef1, self.weight):
					self.connections.remove((self.nodeRef2, self.nodeRef1, self.weight))
					break
				else:
					continue
			
			#Removes the connections from the nodes themselves
			self.nodeRef1.connectedTo.remove((self.nodeRef2, self.weight))
			self.nodeRef2.connectedTo.remove((self.nodeRef1, self.weight))
			
	def dijkstra(self, start, end):
		'''Runs dijkstra's algorithm on the graph
		   Can take the start and end nodes as arguments in two ways, either:
			   Give the integer values of the nodes
			   Or give the node objects themselves
			   
		   Will print the final path and its weight'''
		#Sets up the start and end references depending on data type passed as argument
		if isinstance(start, GraphNode) and isinstance(end, GraphNode):
			self.startRef = start
			self.endRef = end
		else:
			self.startRef = None
			self.endRef = None
			for node in self.nodes: #Finds the nodes within the graph and creates references to them
				if start == node.value:
					self.startRef = node
				elif end == node.value:
					self.endRef = node
				else:
					continue
		
		self.visited = list() #List of nodes that have been visited
		self.unvisited = self.nodes.copy() #List of nodes yet to be visited
		
		self.currentNode = self.startRef #Sets up the current node
		self.currentNode.tWeight = 0 #Sets up the first nodes values
		self.currentNode.previous = "START"
		
		while self.unvisited:
			for neighbour in self.currentNode.connectedTo:
				#If node is unvisited (infinite distance)
				if neighbour[0].tWeight == float("inf"):
					neighbour[0].tWeight = neighbour[1] + self.currentNode.tWeight
					neighbour[0].previous = self.currentNode
				#If new distance is less than the current path
				elif (neighbour[1]+neighbour[0].tWeight) < neighbour[0].tWeight:
					neighbour[0].tWeight = neighbour[1] + neighbour[0].tWeight + self.currentNode.tWeight
					neighbour[0].previous = self.currentNode
			
			#Marks current node as visited
			self.visited.append(self.currentNode)
			self.unvisited.remove(self.currentNode)
			
			#Finds the next smallest distance from current node
			self.min = float("inf")
			for neighbour in self.currentNode.connectedTo:
				#If node is unvisited and closer than the current nearest use that node
				if (neighbour[0] not in self.visited) and (neighbour[0].tWeight < self.min):
					self.currentNode = neighbour[0]
					self.min = self.currentNode.tWeight
		
		#Reads back through to create the final path
		self.currentNode = self.endRef
		self.finalPath = list()
		self.finalDist = self.currentNode.tWeight
		while self.startRef not in self.finalPath:
			self.finalPath.append(self.currentNode)
			self.currentNode = self.currentNode.previous
		
		#Prints out the final path and distance
		print("Final Path:")
		for node in reversed(self.finalPath):
			if node == self.endRef:
				print(node.value)
			else:
				print(node.value, "--> ", end='')
		print("Total Distance:", self.finalDist)
		
class GraphNode:
	def __init__(self, nodeValue):
		'''Creates the node object, requires a value to be
		   passed in'''
		self.value = nodeValue
		self.connectedTo = list()
		self.previous = None #Node tWeight came from
		self.tWeight = float("inf") #Temporary weight
		
if __name__ == "__main__":
	graph = WeightedGraph()
	
	graph.addNode(13)
	graph.addNode(6)
	graph.addNode(9)
	graph.addNode(4)
	graph.addNode(21)
	graph.addConnection(4, 13, 4)
	graph.addConnection(4, 6, 8)
	graph.addConnection(6, 9, 12)
	graph.addConnection(13, 9, 2)
	graph.addConnection(13, 21, 5)
	graph.addConnection(9, 21, 9)
	graph.dijkstra(21, 6)