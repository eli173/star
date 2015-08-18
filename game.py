#80#############################################################################

class Game:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.open_cells = []
        for cg in cell_groups:
            for c in cg:
                self.open_cells.append(list(c))
        self.p1_cells = []
        self.p2_cells = []
    def import_string(self,bstr):
        if len(bstr)!=50:
            return len(bstr)
        cells = []
        ls = ['*','s','t','a','r']
        for cg in cell_groups:
            cells+=list(cg)
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
    def get_regions(self):
        b = Board()
        regions = {}
        regions[self.p1] = b.get_regions(self.p1_cells)
        regions[self.p2] = b.get_regions(self.p2_cells)
        regions[None] = b.get_regions(self.open_cells)
        return regions
    def calc_score(self):
        ls = ['*','s','t','a','r']
        score = {}
        score[self.p1] = {}
        score[self.p2] = {}
        stars = {}
        # score[player][points from what (i.e. peris, quarks, stars)]
        ls = ['*','s','t','a','r']
        peris = list(cell_groups[3])
        peris.sort(key=lambda p: str(ls.index(p[0]))+p[1:])
        unscored_peris = list(peris)
        quarks = ['*40','s40','t40','a40','r40']
        peris.sort(key=lambda p: str(ls.index(p[0]))+p[1:])
        regions = self.get_regions()
        stars[self.p1] = list(regions[self.p1])
        for region in stars[self.p1]:
            list(filter(region,lambda p: p in peris))
        stars[self.p2] = list(regions[self.p2])
        for region in stars[self.p2]:
            list(filter(region,lambda p: p in peris))
        for i in range(len(stars[self.p1])):
            if len(stars[self.p1][i])<2:
                stars[self.p1].pop(i)
        for i in range(len(stars[self.p2])):
            if len(stars[self.p2][i])<2:
                stars[self.p2].pop(i)
        for player in (self.p1,self.p2):
            for star in stars[self.p1]:
                for peri in star:
                    score[self.p1]['peris']+=1
                    unscored_peris.reomve(peri)
        # now for peris not in a star...
        

            
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
        self.peris = list(cell_groups[3])
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
    def get_regions(self,vtx_ls):
        vls = list(vtx_ls)
        regions = []
        while(len(vls)!=0):
            not_checked = [vls.pop(0)]
            this_region = [not_checked[0]]
            while(len(not_checked)!=0):
                curr = not_checked.pop(0)
                nbrs = self.get_edges(curr)
                for nbr in nbrs:
                    if nbr in vls:
                        vls.remove(nbr)
                        if nbr not in not_checked:
                            not_checked.append(nbr)
                        if nbr not in this_region:
                            this_region.append(nbr)
            regions.append(this_region)
        return regions