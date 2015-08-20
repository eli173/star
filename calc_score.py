

import game

peris = list(game.cell_groups[3])
ls = ['*','s','t','a','r']

peris.sort(key=lambda p: str(ls.index(p[0]))+p[1:])

def between(a,b,ls):
    ai = ls.index(a)
    bi = ls.index(b)
    if ai<bi:
        return ls[ai+1:bi]
    else:
        return ls[ai+1:]+ls[:bi]


# idea: choose a star, look on both sides of it
# 
# okok this works, but gotta check if center-crossing stars at both sides...
# 
# so if a peri between two different cc stars, just check the area in between
# if it's a peri there then we're golden, else not
# 
# 
# 

def get_stars(regions):
    p1 = list(regions.keys())[0]
    p2 = list(regions.keys())[1]
    stars = {p1:[],p2:[]}
    for region in regions[p1]+regions[p2]:
        if len(list(filter(lambda c: c in peris,region))) >= 2:
            if region in regions[p1]:
                stars[p1].append(region)
            else:
                stars[p2].append(region)
    return stars

def get_center_crossing_stars(g):
    # change to only take ones that actually _cross_,
    # i.e. exists a space between two center pieces (or just 3+ pcs)
    # there can be two at most I guess...
    # go ahead and throw back any stars that have center points
    ccs = {g.p1:[],g.p2:[]}
    stars = get_stars(g.get_regions())
    def on_center(star):
        cs = list(filter(lambda c: c[1:] == '10',star))
        return cs != []
    for star in stars[g.p1]:
        if on_center(star):
            ccs[g.p1] = star
    for star in stars[g.p2]:
        if on_center(star):
            ccs[g.p2] = star
    centers = {}
    centers[g.p1] = list(filter(lambda c: c[1:] == '10',ccs[g.p1]))
    centers[g.p2] = list(filter(lambda c: c[1:] == '10',ccs[g.p2]))
    if len(centers[g.p1])<2:
        ccs[g.p1] = []
    if len(centers[g.p2])<2:
        ccs[g.p2] = []
    if len(centers[g.p1])==2: # next to
        c0 = ls.index(centers[g.p1][0])
        c1 = ls.index(centers[g.p1][1])
        if c0==(c1+1)%5 or (c0+1)%5==c1:
            ccs[g.p1] = []
    if len(centers[g.p2])==2: # next to
        c0 = ls.index(centers[g.p2][0])
        c1 = ls.index(centers[g.p2][1])
        if c0==(c1+1)%5 or (c0+1)%5==c1:
            ccs[g.p2] = []
    return ccs
        
    
    

def get_sections(star):
    star_peris = []
    for cell in star:
        if cell in peris:
            star_peris.append(cell)
    star_peris.sort(key=lambda p: str(ls.index(p[0]))+p[1:])
    if len(star_peris)<2:
        return list(peris)
    i = 1
    sections = []
    print(star_peris)
    while i<len(star_peris)-1:
        sections.append(between(star_peris[i-1],star_peris[i],peris))
        i+=1
    sections.append(between(star_peris[-1],star_peris[0],peris))
    return sections
    

def calc_score(g, b): # game and board
    regions = g.get_regions()
    stars = get_stars(regions)
    ccs = get_center_crossing_stars(g)

    score = {g.p1:{'peri':0}, g.p2:{'peri':0}}

    peris_left = list(peris)
    
    # easy ones: peris in stars
    starpcs = {g.p1:[],g.p2:[]}
    for star in stars[g.p1]:
        starpcs[g.p1] += star
    for star in stars[g.p2]:
        starpcs[g.p2] += star
    for peri in peris:
        if peri in starpcs[g.p1]:
            score[g.p1]['peri']+=1
            peris_left.remove(peri)
        elif peri in starpcs[g.p2]:
            score[g.p2]['peri']+=1
            peris_left.remove(peri)

    def get_next_peri(curr,l_or_r):
        # l true, r false
        return peris[peris.index(curr) + (1 if l_or_r else -1)]
    def get_star(peri):
        # returns {player: star}
        for star in stars[g.p1]:
            if peri in star:
                return {g.p1:star}
        for star in stars[g.p2]:
            if peri in star:
                return {g.p2:star}
        return {}
    for peri in peris_left:
        # look at star peris to l and r:
        #   - part of same star? great!
        # else:
        #   - if one star is a ccs, it goes to ccs-owner
        #   - if both in a ccs,
        left_peri = None
        right_peri = None
        left_star = None
        right_star = None
        curr = peri
        counter = 0
        peri_star = {}
        while left_star == None and counter <= 50:
            curr = get_next_peri(curr,True)
            peri_star = get_star(curr)
            if peri_star != {}:
                left_peri = curr
                left_star = peri_star
        counter = 50
        curr = peri
        peri_star = {}
        while right_star == None and counter <=50:
            curr = get_next_peri(peri,False)
            peri_star = get_star(curr)
            if peri_star != {}:
                right_peri = curr
                right_star = peri_star
        # y'know what? this should only accept completed games...
        # now...
        if left_peri in ccs[g.p1]:
            if right_peri in ccs[g.p2]:
                pass # not claimed?
            else:
                score[g.p1]['peri']+=1


        
