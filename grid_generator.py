import random
import matplotlib.pyplot as plt
import seaborn as sns
import copy

dim = 15
successes = set()
success_flag = False
graph_num = 0

def display_cross(crossword):
    for row in crossword: print("\t"+str(row))
    print("\n")

def graph_cross(crossword,graph_num):
    with sns.axes_style("white"):
        ax = sns.heatmap(crossword, vmax=2, square=True,  cmap="Pastel1_r", cbar = False, linewidth = 3)
        ax.axis('off')
        ax.set_title("Potential Crossword: " + str(graph_num))
        plt.savefig(str(graph_num)+".png")

def mirror_cross(crossword,success_flag):
    for x in range(dim):
        for y in range(dim):
            if y <= x:
                mirrored_x = dim - x - 1
                mirrored_y = dim - y - 1
                if crossword[y][x] != 0 and crossword[y][x] != crossword[mirrored_y][mirrored_x]:
                    success_flag = False
                crossword[y][x] = crossword[mirrored_y][mirrored_x]
    return [crossword,success_flag]

def seed_cross(crossword,success_flag):
    for x in range(dim):
        for y in range(dim):
            if y >= x and crossword[y][x] == 0:
                [crossword,success_flag] = seed_square(crossword,x,y,random.randint(1,2),success_flag)
                #print(x,y)
            elif crossword[y][x] == 1:
                [crossword,success_flag] = seed_square(crossword,x,y,1,success_flag)
                #print("reseeding: x:",x," y:",y)
    [crossword,success_flag] = mirror_cross(crossword,success_flag)
    return [crossword,success_flag]

def seed_square(crossword,x,y,value,success_flag):

    #tried to do some cheater sq logic but failed
    #if x == 0 or y == 0:
    #    boarder = True
    #else:
    #    boarder = False

    crossword[y][x] = value
    
    if value == 1:
        #look left
        w_left = 0
        continue_looking = True
        while crossword[y][x-w_left] == 1 and continue_looking:
            w_left += 1
            if x-w_left >= 0: continue_looking = True
            else: continue_looking = False

        #add to right
        for adding in range(0,3-w_left):
            #print("x:",x," y:",y," adding:",adding)
        
            #if x+1+adding < dim: crossword = seed_square(crossword,x+1+adding,y,1)
            if x+1+adding < dim:
                crossword[y][x+1+adding] = 1
            else:
                success_flag = False
        #look up
        w_up = 0
        continue_looking = True
        while crossword[y-w_up][x] == 1 and continue_looking:
            w_up += 1
            if y-w_up >= 0: continue_looking = True
            else: continue_looking = False

        #add to bottom
        for adding in range(0,3-w_up):
            #if y+1+adding < dim: crossword = seed_square(crossword,x,y+1+adding,1)
            if y+1+adding < dim:
                crossword[y+1+adding][x] = 1
            else:
                success_flag = False

    return [crossword,success_flag]

#This will look for a state in each crossword find the size of that shape. 
#If it is smaller than the required size it will know the crossword is not continuous
def check_cont(crossword, success_flag):
    cont = True
    havent_found_crossword = True
    dist_in_question = 1
    population_per_crossword = 0
    for row in crossword:
        population_per_crossword += row.count(dist_in_question)
    
    temp_crossword = copy.deepcopy(crossword)
    #Look in random squares to find a state that is of the desired crossword
    while havent_found_crossword:
        x = random.randint(0,dim-1)
        y = random.randint(0,dim-1)
        if temp_crossword[y][x] == dist_in_question:
            havent_found_crossword = False
    places_to_explore = \
    [
        [y,x]
    ]
    if find_size(temp_crossword,places_to_explore,dist_in_question,population_per_crossword) < population_per_crossword:
        success_flag = False
    return success_flag

def find_size(temp_crossword,places_to_explore,dist_in_question,population_per_crossword):
    size = 0
    paths = 1
    #Find # of paths you can take from your location
    while size < population_per_crossword and paths:
        paths = paths - 1
        for del_x, del_y in [(-1,0), (1,0), (0,-1), (0,1)]:
            if check_bounds(places_to_explore[0][1],del_x,places_to_explore[0][0],del_y) and dist_in_question == temp_crossword[places_to_explore[0][0]+del_y][places_to_explore[0][1]+del_x]:
                paths = paths + 1
                places_to_explore.append([places_to_explore[0][0]+del_y,places_to_explore[0][1]+del_x])
                #77 is meant to be jibberish. Makes it so it won't be double counted
                temp_crossword[places_to_explore[0][0]+del_y][places_to_explore[0][1]+del_x] = 77 
        temp_crossword[places_to_explore[0][0]][places_to_explore[0][1]] = 77
        size = size + 1
        places_to_explore.remove([places_to_explore[0][0],places_to_explore[0][1]])
    return size

def check_bounds(x,del_x,y,del_y):
    if x+del_x > dim-1 or x+del_x < 0 or y+del_y > dim-1 or y+del_y < 0:
        return False
    return True

def create_cross(dim):
    success_flag = False

    while success_flag == False:
        success_flag = True #starts as true and can only be set to false from here on out
        crossword = [[0 for i in range(dim)] for i in range(dim)]
        [crossword,success_flag] = seed_cross(crossword,success_flag)
        if success_flag:
            success_flag = check_cont(crossword, success_flag)
    return crossword

def flatten_cross(crossword):
    return [x for sublist in crossword for x in sublist]

def unflatten_cross(flat_crossword):
    crossword = []
    for row in range(dim): crossword.append(flat_crossword[row*dim:(row+1)*dim])
    return crossword

while len(successes) < 10000:
    crossword = create_cross(dim)
    flat_cross = flatten_cross(crossword)
    tuple_flat_cross = tuple(flat_cross)

    old_len = len(successes)
    successes.add(tuple_flat_cross)
    if len(successes) > old_len:
        graph_num += 1
        graph_cross(crossword,graph_num)
        print(graph_num)
