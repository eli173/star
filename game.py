

class Game:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.open_cells = []
        for cg in cell_groups:
            for c in cg:
                self.open_cells.append(c)
        self.p1_cells = []
        self.p2_cells = []
    def import_string(self,bstr):
        if len(bstr)!=50:
            return len(bstr)
        cells = []
        ls = ['*','s','t','a','r']
        for cg in cell_groups:
            cells+=cg
        cells.sort(key=lambda c: str(ls.index(c[0]))+c[1:])
        self.p1_cells = []
        self.p2_cells = []
        self.open_cells = []
        for i in range(50):
            if bstr[i]=='0':
                self.open_cells.append(cells[i])
            elif bstr[i]=='1':
                self.p1_cells.append(cells[i])
            else:
                self.p2_cells.append(cells[i])
    def move(self,player,cell):
        self.open_cells.remove(cell)
        if player==self.p1:
            self.p1_cells.append(cell)
        else:
            self.p2_cells.append(cell)
    def is_over(self):
        return len(self.open_cells)==0
    def __get_regions(self):
        regions = {}
        regions[self.p1] = self.__get_p_regions(self.p1)
        regions[self.p2] = self.__get_p_regions(self.p2)
        regions[None] = self.__get_p_regions()
        return regions
    def __get_p_regions(self,player=None):
        board = Board()
        ls = []
        if player==None:
            ls = list(self.open_cells)
        elif player==self.p1:
            ls = list(self.p1_cells)
        else: # p2
            ls = list(self.p2_cells)
        regions = []
        while len(ls)!=0:
            checked = []
            candidates = [ls.pop(0)]
            for c in candidates:
                reg = []
                for n in board.get_edges(c):
                    if n not in checked and n not in candidates:
                        if n in ls:
                            candidates.append(n)
                            regions.append(n)
                            ls.remove(n)
                candidates.remove(c)
                checked.append(c)
                regions.append(reg)
        return regions
            
    def calc_score(self):
        ls = ['*','s','t','a','r']
        peris = cell_groups[3]
        quarks = ['*40','s40','t40','a40','r40']
        peris.sort(key=lambda p: str(ls.index(p[0]))+p[1:])
        
        
        


            
cell_groups = [['s10','t10','a10','r10','*10'],
               ['s20','t20','a20','r20','*20',
                's21','t21','a21','r21','*21'],
               ['s30','t30','a30','r30','*30',
                's31','t31','a31','r31','*31',
                's32','t32','a32','r32','*32'],
               ['s40','t40','a40','r40','*40',
                's41','t41','a41','r41','*41',
                's42','t42','a42','r42','*42',
                's43','t43','a43','r43','*43']]


    


class Board(Graph):
    def __init__(self,big=False):
        super().__init__()
        self.peris = cell_groups[3]
        self.quarks = ['s40','t40','a40','r40','*40']
        ls = ['*','s','t','a','r']
        next_one = lambda c: ls[(ls.index(c)+1) % 5]
        prev_one = lambda c: ls[(ls.index(c)-1) % 5]
        next_chr = lambda c: chr(ord(c)+1)
        prev_chr = lambda c: chr(ord(c)-1)
        for cell in cell_groups[0]:
            self.add_vertex(cell)
        for cell in cell_groups[0]:
            for other in cell_groups[0]:
                self.add_edge(cell,other)
        # first layer done
        for cell in cell_groups[1]:
            self.add_vertex(cell)
        for cell in self.get_verts():
            for other in self.get_verts():
                if cell[0]==other[0]:
                    self.add_edge(cell,other)
        for cell in cell_groups[1]:
            if cell[2]=='1':
                self.add_edge(cell,next_one(cell[0])+'20')
                self.add_edge(cell,next_one(cell[0])+'10')
        # second layer done
        for cell in cell_groups[2]:
            self.add_vertex(cell)
        for cell in cell_groups[2]:
            if cell[2]=='0':
                self.add_edge(cell,prev_one(cell[0])+'32')
                self.add_edge(cell,cell[0]+'31')
                self.add_edge(cell,cell[0]+'20')
            elif cell[2]=='1':
                self.add_edge(cell,cell[0]+'32')
                self.add_edge(cell,cell[0]+'20')
                self.add_edge(cell,cell[0]+'21')
            else:
                self.add_edge(cell,cell[0]+'21')
                self.add_edge(cell,next_one(cell[0])+'20')
        # third layer done (?)
        for cell in cell_groups[3]:
            self.add_vertex(cell)
        for cell in cell_groups[3]:
            if cell[2]=='0':
                self.add_edge(cell,prev_one(cell[0])+'43')
                self.add_edge(cell,cell[0]+'41')
                self.add_edge(cell,cell[0]+'30')
            elif cell[2]=='3':
                self.add_edge(cell,cell[0]+'42')
                self.add_edge(cell,next_one(cell[0])+'30')
                self.add_edge(cell,cell[0]+'32')
            else:
                self.add_edge(cell,cell[0:2]+next_chr(cell[2]))
                self.add_edge(cell,cell[0]+'3'+cell[2])
                self.add_edge(cell,cell[0]+'3'+prev_chr(cell[2]))
        # done with small board
        # this actually probably works in general... for larger boards
                

class EdgeList:
    """
    List of edges for graph class
    """
    def __init__(self, vertex=None):
        self.vertex = vertex
        self.edge_list = []
    def __str__(self):
        return str(self.vertex)+': '+str(self.edge_list)
    def add_edge(self, vtx):
        if vtx not in self.edge_list:
            self.edge_list.append(vtx)
        
class Graph:
    """
    generic graph class
    
    supports directed and undirected
    """
    def __init__(self, is_directed=False, is_reversed=False):
        self.edge_lists = []
        self.directed = is_directed
        self.reverse = is_reversed
    def _get_edge_list(self,vert):
        tmp_edge_list = list(filter((lambda v: v.vertex == vert),
                                    self.edge_lists))
        if tmp_edge_list != []:
            #print(tmp_edge_list[0])
            #print("edge list ^\n")
            return tmp_edge_list[0]
    def make_directed(self):
        self.directed = True
    def make_undirected(self):
        self.directed = False
    def get_verts(self):
        vt_ls = []
        for el in self.edge_lists:
            vt_ls.append(el.vertex)
        return vt_ls
    def has_vertex(self,vtx):
        tmp_verts = list(filter((lambda el: el.vertex == vtx),
                            self.edge_lists))
        return len(tmp_verts)!=0
    def has_edge(self,v1,v2):
        #return (self.get_edges(v1).edge_list.count(v2)!=0)
        v1_edges = self.get_edges(v1)
        return v2 in v1_edges
    def get_edges(self,vert):
        elarr = list(filter(lambda x:
                         x.vertex == vert,
                         self.edge_lists))
        if len(elarr)==0:
            return []
        el = elarr[0]
        return el.edge_list
    def add_vertex(self, vtx_name):
        self.edge_lists.append(EdgeList(vtx_name))
    def add_edge(self, vtx1, vtx2):
        if vtx1==vtx2:
            return
        if not self.directed:
            for el in self.edge_lists:
                if el.vertex == vtx1:
                    el.add_edge(vtx2)
                if el.vertex == vtx2:
                    el.add_edge(vtx1)
        elif not self.reverse:
            for el in self.edge_lists:
                if el.vertex == vtx1:
                    el.add_edge(vtx2)
        else:
            for el in self.edge_lists:
                if el.vertex == vtx2:
                    el.add_edge(vtx1)
