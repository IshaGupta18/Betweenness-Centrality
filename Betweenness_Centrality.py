#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "Isha Gupta"
    email = "isha18040@iiitd.ac.in"
    roll_num = "2018040"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges

        self.mypaths=[]

        N=len(self.vertices)

        self.divisor=((N-1)*(N-2))/2.0
        
        self.validate()

        self.adjacency_matrix=[]
        self.visited=[0 for x in range(len(self.vertices)+1)]

        for i in range(len(self.vertices)+1):
            l=[0 for x in range(len(self.vertices)+1)]
            self.adjacency_matrix.append(l)
        for i in edges:
            first=i[0]
            second=i[1]
            self.adjacency_matrix[first][second]=1
            self.adjacency_matrix[second][first]=1
        #print (self.adjacency_matrix)

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
        min_path_temp={}
        minimum_path=[]
        pqlist=[start_node]
        visited=[0 for x in range(len(self.vertices)+1)]
        visited[start_node]=1
        min_path_temp[start_node]=-1
        x=False
        while (len(pqlist)!=0):
            front=pqlist[0]
            pqlist.pop(0)
            for i in range(len(self.vertices)+1):
                if (self.adjacency_matrix[front][i]==1 and visited[i]!=1):
                    min_path_temp[i]=front
                    pqlist.append(i)
                    visited[i]=1
                    if i==end_node:
                        x=True
                        break
            if x==True:
                break
        cur=end_node
        while True:
            minimum_path.append(cur)
            if cur==start_node:
                if cur not in minimum_path:
                    minimum_path.append(cur)
                break
            cur=min_path_temp[cur]
        return len(minimum_path)
        

        raise NotImplementedError

    def all_shortest_paths(self, start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        distance=self.min_dist(start_node,end_node)
        #print (distance)
        vis=[0 for i in range(len(self.vertices)+1)]
        paths=self.all_paths(start_node,end_node,distance,vis,"",[])
        return paths

        raise NotImplementedError

    def all_paths(self, node, destination, dist, visited, path,mypaths):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """
        path+=str(node)
        visited[node]=1
        if len(path)==dist and node==destination:
            #print (path, "correct path")
            mypaths.append(path)
        for i in range(1,len(self.vertices)+1):
            if self.adjacency_matrix[node][i]==1 and visited[i]!=1:
                next_node=i
                #print ("next node is",next_node)
                #path+=str(next_node)
                #print (path)

                self.all_paths(next_node,destination,dist,visited,path,mypaths)
        visited[node]=0
        return mypaths
        raise NotImplementedError

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """
        
        
        vert=self.vertices[::]
        c=str(node)
        vert.remove(node)
        pairs=[]
        for i in range(len(vert)-1):
            a=vert[i]
            for j in range(i+1,len(vert)):
                p=[a,vert[j]]
                pairs.append(p)
        bw_cen=0
        for i in pairs:
            #print ("dealing with",i)
            start=i[0]
            end=i[1]
            all_the_paths=self.all_shortest_paths(start,end)
            x=len(all_the_paths)
            y=0
            for j in all_the_paths:
                if c in j:
                    y+=1
            #print ("all paths for",i,all_the_paths)
            #print (float(y)/float(x),i)
            bw_cen+=float(y)/float(x)
        
        
        return bw_cen
            
                               

        raise NotImplementedError
    #this function just calculates standardized betweenness centrality using betweenness_centrality function and just returns it
    def standardized_betweenness_centrality(self,node):
        bw_cent=self.betweenness_centrality(node)
        standarad_betweenness_centrality=bw_cent/self.divisor

    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """
        all_bw_cen=[]
        max_bw=-1
        for i in self.vertices:
            bw=self.betweenness_centrality(i)
            ele=[i,bw]
            all_bw_cen.append(ele)
            if bw>max_bw:
                max_bw=bw
        top_k=[]
        for i in all_bw_cen:
            if i[1]==max_bw:
                top_k.append(i[0])
    
        return top_k
        

        raise NotImplementedError

if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (3,6 ), (4, 5), (4, 6)]

    graph = Graph(vertices, edges)
    """print (graph.min_dist(1,6))
    x= (graph.all_paths(1,6,4,[0,0,0,0,0,0,0],"",[]))
    print (x)"""
    #print(graph.all_shortest_paths(1,6))
    #print(graph.betweenness_centrality(3))
    #print (graph.top_k_betweenness_centrality())
