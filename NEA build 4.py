try:
    import pygame
    import random
    import time
    import math
    import json
    import sys
except:
    print("you do not have the required libraries to run this program")
    sys.exit()
default = {'layer-1': {'food': 2000, 'herbivores': 10, 'carnivores': 10}}
vgui_warning_config = False
try:
    Config = json.load(open("config.json","r"))
except:
    file = open("config.json", "a")
    json.dump(default, file)
    file.close()
    Config = json.load(open("config.json","r"))
    vgui_warning_config = True
pygame.init()
panel = pygame.display.set_mode((1700,800),pygame.NOFRAME)
screen_size = panel.get_size()
#font_main = pygame.font.Font('Bahnschrift.ttf', 10)
font_alt = pygame.font.Font('freesansbold.ttf', 12)
ui_font_scale_3 = pygame.font.Font('freesansbold.ttf', 10)
big = pygame.font.Font('freesansbold.ttf', 40)
try:
    dvd = pygame.image.load('logo.png')
    dvd = pygame.transform.scale(dvd, (100, 50))
except:
    print("logo.png not found")
    dvd = big.render("logo.png is missing, please download it", True, (0,0,255))
img_size = dvd.get_rect().size

x = random.randint(150, 1700-160)
y = random.randint(150, 800-160)
x_speed = 1.5
y_speed = 1.5

foreground = (20,20,20)
vgui_fore = (40,40,40)
vgui_bounding = (120,120,120)
vgui_state_0 = (10,10,220)
vgui_state_1 = (20,20,200)
vgui_state_2 = (20,20,180)
vgui_state_3 = (20,20,150)
vgui_state_4 = (20,20,120)
vgui_state_5 = (20,20,80)
vgui_important = (0,0,0)
vgui_aux_text_internal = (200,200,200)
vgui_aux_text_external = (200,200,200)
vgui_warning_1 = (150,20,20)

vgui_ray_broken = (250,0,0)
vgui_ray_beam = (0,255,0)

vgui_color_ON = (0,255,0)
vgui_color_OFF = (255,0,0)
vgui_group_fore = (190,190,190)
vgui_entity_herbivore = (0,250,0)
vgui_herbivore_egg = (221,100,221)
vgui_entity_dead = (70,70,70)
vgui_entity_carnivore = (250,0,0)
vgui_entity_nose = (0,0,0)
entity_object_array = []
hunter_object_array = []
food_object_array = []
producer_object_array = []
egg_object_array = []
log_index = []
tab = 0
lag_comp = 0
bases = ["G","A","T","C"]
GPP = 0
NPP_SAMPLES = []
TSC_SAMPLES = []
NPP = 0
GSP = 0
TSC = 0
BMI = 0
PE = 0
tick = 0
balance = 0
sight_average = []
log_var = 0
def biodiversity_index():
    num_organisms = len(entity_object_array)
    register = []
    for e in entity_object_array:
        if e.introgenic_dna not in register:
            register.append(e.introgenic_dna)
    num_species = len(register)
    N = num_organisms * (num_organisms - 1)
    n = 0
    for r in register:
        n+=entity_object_array.count(r) * (entity_object_array.count(r)  - 1)
    return N / n
class log_entry:
    def __init__(this,text = "",label = "",label_text = ""):
        global log_var
        this.txt = text #main text displayed on log
        this.label = label #special hoverable text
        this.label_text = label_text #text displayed on the hover
        txt = ui_font_scale_3.render(this.txt, True, vgui_aux_text_internal) #rect of text for display
        this.label_dimensions = [txt.get_width() + 20,40]
        #if (log_var != 0):
         #   log_var+=1
    def handle_hover(this):
       # if (30 + (log_index.index(this) * 15)) > 760:
            #del log_index[0] #remove off the screen logs from back to front
        if len(log_index) > 51:
            log_onscreen = log_index[len(log_index) - 51 - log_var : len(log_index) - 1 - log_var]
        else:
            log_onscreen = log_index
        if this not in log_onscreen:
            return
        label_text = ui_font_scale_3.render(this.label_text, True, vgui_aux_text_internal)
        label = ui_font_scale_3.render(this.label, True, (255,255,0)) 
        c_vec = pygame.mouse.get_pos() # mouse pos
        c_bool = pygame.mouse.get_pressed()[0] # mouse state
        txt = ui_font_scale_3.render(this.txt, True, vgui_aux_text_internal)
        panel.blit(txt,(1000 - ((txt.get_width() + label.get_width()) / 2),30 + (log_onscreen.index(this) * 15))) #display main text
        panel.blit(label,(1000 + ((txt.get_width() - label.get_width()) / 2),30 + (log_onscreen.index(this) * 15)))# display special text
        #print(c_vec[0] > 1000 + (txt.get_width() / 2),c_vec[0] < 1000+label.get_width())
        if (c_vec[0] > 1000 + ((txt.get_width() - label.get_width()) / 2) and c_vec[0] < 1000+label.get_width()+ ((txt.get_width() - label.get_width()) / 2)):
            if (c_vec[1] > 30 + (log_onscreen.index(this) * 15) and c_vec[1] <  40 + (log_onscreen.index(this) * 15)): #check for hover
                if (this.label_text == ""):
                    return #remove empty special text
                if ((1000 + (txt.get_width() / 2)) + label_text.get_width()+2) > 1200:
                    recession = ((1000 + (txt.get_width() / 2)) + label_text.get_width()+2) - 1200 + 5 #recess ui bounder formula to prevent it going off screen
                    pygame.draw.rect(panel, vgui_fore, pygame.Rect(1000 + (txt.get_width() / 2) - recession,30 + (log_onscreen.index(this) * 15),label_text.get_width()+2,15))#fore scope
                    panel.blit(label_text,(1000 + (txt.get_width() / 2) - recession,30 + (log_onscreen.index(this) * 15) + 3))
                    box = group_box((1000 + (txt.get_width() / 2) - recession,30 + (log_onscreen.index(this) * 15)),"",label_text.get_width()+2,15)
                    box.draw() #draw bounding ui 
                    return
                pygame.draw.rect(panel, vgui_fore, pygame.Rect(1000 + (txt.get_width() / 2),30 + (log_onscreen.index(this) * 15),label_text.get_width()+2,15))#fore scope
                box = group_box((1000 + (txt.get_width() / 2),30 + (log_onscreen.index(this) * 15)),"",label_text.get_width()+2,15)
                box.draw() #draw an unrecessed box
                panel.blit(label_text,(1000 + (txt.get_width() / 2),30 + (log_onscreen.index(this) * 15) + 3))
def generate_dna_sequence(length):
    strand = []
    for i in range(length):
        strand.append(random.choice(bases)) # randomly add a nucleotide base
    return strand
def read_dna_protein(strand):
    active_site = read_dna_binary(strand[0:3])
    op_code = read_dna_binary(strand[4:7])
    if bases.index(strand[len(strand) - 1]) == 0:
        sign = True # handle negative sign bases
    else:
        sign = False
    if (sign):
        op_code -= op_code * 2 # make the opcode negative
    return [active_site,op_code]
def read_dna_binary(strand):
    binary = ""
    for base in strand:
        if bases.index(base) == 1 or bases.index(base) == 2: # checks for a non complementary base e.g A or G as A and T are complementary
            binary += "0"
        else:
            binary += "1"
    return int(binary,2) #convert bases to binary 
def create_mutation(strand): 
    if (strand == None):
        return 
    mutated = strand[0 : len(strand)] #make a copy of the argument
    mutation_type = random.randint(1,300) # insertion and base deletion mutations are rarer so their chances are reduced
    if (len(strand) == 1):
        mutation_type = random.randint(1,249)
    #frame shift aka deletion
    if (mutation_type <= 300 and mutation_type > 250):
        del mutated[mutated.index(random.choice(mutated))] # remove a base
        return (mutated,"DELETION")
    #substitution
    if (mutation_type <= 100):
        mutated[mutated.index(random.choice(mutated))] = random.choice(bases) #change a base
        return (mutated,"SUBSTITUTION")
    #inversion
    if (mutation_type <= 200 and mutation_type > 150): 
        return(mutated[::-1],"INVERSION")
    #duplication
    if (mutation_type <= 150 and mutation_type > 100):
        mutated.append(mutated[len(mutated) - 1])
        return(mutated,"DUPLICATION")
    #insertion
    if (mutation_type <= 250 and mutation_type > 200):
        mutated.append(random.choice(bases)) #  add a base
        return (mutated,"INSERTION")
    
#class genetic_code:
    #def __init__(this,length):
        #this.strand = generate_dna_sequence(length)
        #this.numerical_value = read_dna_binary(this.strand)
    #def update(this):
        #this.numerical_value = read_dna_binary(this.strand)
    #def mutation(this):
        #this.strand = create_mutation(this.strand)
        #this.update()
def Sqr(num):
    return num*num #simple math for cleanliness
def distance_to(vec_point_a,vec_point_b):
    change_in_x = abs(vec_point_a[0] - vec_point_b[0])
    change_in_y = abs(vec_point_a[1] - vec_point_b[1])
    return math.sqrt(Sqr(change_in_x) + Sqr(change_in_y)) #pythagoras
def rad_to_deg(vec_point_a,vec_point_b):
    x1, y1 = vec_point_a
    x2, y2 = vec_point_b 
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) 
    return angle
    #hyp = distance_to(vec_point_a,vec_point_b) 
    #opp = distance_to((vec_point_b[0],vec_point_a[1]),vec_point_b) # find unknown sides
    #raw_angle = pythag(opp,hyp)
    #X = vec_point_b[0] - vec_point_a[0]
    #Y = vec_point_b[1] - vec_point_a[1]
    #if X < 0 and Y < 0:
     #   angle = raw_angle + 180 # add preexisting offset
    #elif X < 0:
     #   angle = -raw_angle + 180
    #elif Y < 1:
     #   angle = -raw_angle
    #else:
    #    angle = raw_angle
    #return angle
def pythag(opp,hyp):
    try:
        sine = (opp/hyp) # only used for sight cone as second method can cause an error when the object is perfectly adjacent 
    except:
        return 0
    return (math.asin(sine) * 57.296)
def point_of_orbit(host_vec,rotation_float,radius_int):
    c = math.cos(rotation_float * 0.0174)
    s = math.sin(rotation_float * 0.0174)
    return [(host_vec[0] + radius_int * c),(host_vec[1] + radius_int * s)] # create a tangent and add an offset
def trace_ray(from_vec,to_vec,array):
    lazy_trace_threshold = 0
    ray_skip_mult = 1 # skip a ray step per trace
    ray_visualize = True
    ray_ignore_groups = [False,False]
    ray_hitbox_add = 0 # remove ray precision
    ray_angle = rad_to_deg(from_vec,to_vec) #angle to trace
    for ray in range(500 - lazy_trace_threshold):
        RayPos = point_of_orbit(from_vec,ray_angle,ray*ray_skip_mult)
        if (not ray_ignore_groups[0]):
            for food_obj in array: # food group 
                if (distance_to(RayPos,food_obj.pos) > 3):
                    continue # exclude non collided
                if (food_obj.pos == to_vec):
                    pygame.draw.line(panel,vgui_ray_beam,from_vec,to_vec) # collided with the target
                    return True
                else:
                    #hit something else so missed (meaning its colluded)
                    #if (ray_visualize):
                    #pygame.draw.line(panel,vgui_ray_beam,from_vec,to_vec)
                    #pygame.draw.line(panel,vgui_ray_broken,RayPos,to_vec)
                    return False
def get_next_move_to(from_vec,rotation_float,radius = 0.2):
    #old method
    if (not vgui_checkbox_sim_lag_comp.state):
        return point_of_orbit(from_vec,rotation_float,radius)
    return point_of_orbit(from_vec,rotation_float,radius / lag_comp + 1)
def think_next_move(to_vec,from_vec,step):
    if (to_vec == None or from_vec == None):
        return
    #primitive, will change maybe using tensorflow
    step *= 0.5
    step /= lag_comp # account for lag
    if from_vec[0] < to_vec[0]:
        from_vec[0] += step
    else:
        from_vec[0] -= step
    if (from_vec[1] < to_vec[1]):
        from_vec[1] += step
    else:
        from_vec[1] -= step
    return from_vec
def is_in_triangle(point_a_vec,point_b_vec,point_c_vec,target_vec):
    if (area_of_triangle(target_vec,point_a_vec,point_b_vec) < 0 and area_of_triangle(target_vec,point_b_vec,point_c_vec) < 0 and area_of_triangle(target_vec,point_c_vec,point_a_vec) < 0): # formula checking if coordinates are in a triangle, compares the areas of triangles derived from the coordinates of the target. explained in design
        return True
def area_of_triangle(point_a_vec,point_b_vec,point_c_vec):
    return ((point_a_vec[0] * (point_b_vec[1] - point_c_vec[1])) + (point_b_vec[0] * (point_c_vec[1] - point_a_vec[1])) + (point_c_vec[0] * (point_a_vec[1] - point_b_vec[1]))) / 2 
def clamp(value,maxi,mini):
    #prevent a value getting too large, substitute method too std::clamp
    if (value > maxi):
        return maxi
    if (value < mini):
        return mini
    return value

class vector2:
    #need to add overloads, will use these next rewrite
    def __init__(this,x,y):
        this.x = x
        this.y = y
class vector3:
    def __init__(this,x,y,z):
        this.x = x
        this.y = y
        this.z = z

class food:
    def __init__(this):
        this.pos = [random.randint(150,650),random.randint(50,550)] #random spot in the simulation area
        this.carbs = random.randint(0,255)    
        this.protein = random.randint(0,255)
        this.being_eaten = False
    def draw(this):
        pygame.draw.circle(panel,(this.carbs,this.protein,0),this.pos,2)
class egg:
    def __init__(this,pos,genes,intron):
        this.pos = pos
        this.genes = genes
        this.intron = intron
        this.count_down = 3000
        this.log = log_entry("egg laid: progress: " + str(this.count_down)," parent",str(this.genes)) # add a dynamic log entry showing the egg progress 
        log_index.append(this.log)
        
    def draw(this):
        pygame.draw.circle(panel,vgui_herbivore_egg,this.pos,3) #draw the egg
    def tick(this):
        this.count_down -= (1 / lag_comp) * balance
        if (this.count_down < 0): #herbivore being born
            infant = herbivore()
            infant.egg_progress = -600
            log_index.append(log_entry("herbivore born: ","genome",str(infant.genes)))
            infant.introgenic_dna = this.intron
            infant.pos = this.pos
            infant.genes = this.genes
            if (random.randint(1,100) < vgui_slider_birth_muta_chance.val): #simulate independant assortment 
                index_to_patch = infant.genes.index(random.choice(infant.genes))
                mutated = create_mutation(infant.genes[index_to_patch])
                old_strand = infant.genes[index_to_patch]
                try:
                    mutated[1]
                except:
                    mutated = [mutated]
                    mutated.append("SHORT") # temporary measure to stop genetic material being completely deleted
                log_index.append(log_entry("a mutation has occured on birth! type: " + mutated[1]," details",str(str(old_strand) + "  ->  " +  str(mutated[0])) + " -> " + str(read_dna_binary(old_strand)) + " -> " + str(read_dna_binary(mutated[0]))))
                infant.genes[index_to_patch] = mutated[0]
            infant.refold() #refold proteins
            entity_object_array.append(infant)
            del egg_object_array[egg_object_array.index(this)]
            try:
                del log_index[log_index.index(this.log)]
            except:
                return
            return
        try:
            this.new_log = log_entry("egg laid: progress: " + str(math.ceil(this.count_down)),"parent",str(this.genes))
            log_index[log_index.index(this.log)] = this.new_log
            this.log = this.new_log
        except:
            return
class herbivore:
    def __init__(this):
        this.genes = [generate_dna_sequence(7),generate_dna_sequence(2),generate_dna_sequence(6),generate_dna_sequence(2),generate_dna_sequence(8),generate_dna_sequence(1)]
        this.pos = [random.randint(150,650),random.randint(50,550)]
        this.rotation = 0 # vision cone rotation
        this.introgenic_dna = generate_dna_sequence(25) # dna that doesnt do anything significant, will make this add visual remarks on species later 
        this.target = None
        this.wait_for = 0
        this.dummy = None
        this.egg_progress = 0
        
        this.nutrition = 100
        this.dead = False
        this.nose = 0

        #hormone levels for fight or flight
        this.epinephrine = 0
        this.cns_stimulant = 0
        this.cns_depressant = 0
        this.tolerance_factor = 1
        this.refold()
    def refold(this):
        #reset variables after a dna change
        this.stomach = 10
        this.stomach_max = read_dna_binary(this.genes[0]) + 20
        this.bmr = read_dna_binary(this.genes[1]) + 1
        this.sight = read_dna_binary(this.genes[2])
        this.speed = read_dna_binary(this.genes[3])
        this.litter_size = read_dna_binary(this.genes[5]) + 1
    def draw(this,custom = False,custom_pos = None):
        this.nose = point_of_orbit(this.pos,this.rotation,10)
        pygame.draw.line(panel,vgui_entity_nose,this.pos,this.nose,3)#nose layer
        pygame.draw.circle(panel,vgui_entity_herbivore,this.pos,5)#body layer
        if (this.dead):
            pygame.draw.circle(panel,vgui_entity_dead,this.pos,5)#body layer
        #txt = font_alt.render(str(math.ceil(this.stomach)), True, (0,0,0))
        #panel.blit(txt,this.pos)
    def sight_check(this,target_vec):
        #check if a target is in the vision cone 
        p_1 = point_of_orbit(this.pos, this.rotation + 270, this.sight)
        p_2 = point_of_orbit(this.pos, this.rotation + 90, this.sight)
        p_3 = point_of_orbit(this.pos, this.rotation, this.sight)
        #pygame.draw.line(panel,vgui_warning_1,p_1,p_2)
        #pygame.draw.line(panel,vgui_warning_1,p_1,p_3)
        #pygame.draw.line(panel,vgui_warning_1,p_3,p_2)
        if (is_in_triangle(p_1,p_2,p_3,target_vec)):
            #was in the vision cone
            return True
        else:
            return False
    def create_move(this):
        try:
            #check if the target was killed by by other means
            food_object_array.index(this.target)
        except:
            this.target = None
            return
        this.rotation = rad_to_deg(this.pos,this.target.pos)  #calculate the relative angle 
        this.pos = think_next_move(this.target.pos,this.pos,this.speed + 2 + (this.epinephrine /100)) # update the position
        if (distance_to(this.pos,this.target.pos) <= (4/lag_comp) + 1):
            this.stomach+= (this.target.carbs * 0.1 + this.target.protein * 0.1)
            if (this.stomach > (this.stomach_max * 0.95)):
                this.nutrition+= ((this.target.carbs * 0.1 + this.target.protein * 0.1) * 0.35)
            del food_object_array[food_object_array.index(this.target)]
            this.wait_for = random.randint(math.ceil(60 / this.bmr),math.ceil(250 / this.bmr))
            #force them to pause for a second after eating, making them vulnerable
    def wander(this):
        if (this.dummy == None):
            this.dummy = dummy()
        this.rotation = rad_to_deg(this.pos,this.dummy.pos)
        this.pos = think_next_move(this.dummy.pos,this.pos,(((this.speed - (this.cns_depressant*1.3)) + 2 + (this.epinephrine / 200))))
        if (distance_to(this.pos,this.dummy.pos) <= (4/lag_comp) + 1):
             this.dummy = None
             this.wait_for = random.randint(math.ceil(60 / this.bmr),math.ceil(250 / this.bmr))
             #force them to pause for a second after eating, making them vulnerable
    def kill(this):
        this.dead = True
        #only reason this is a method is because there will be more here in the future 
        #create_blood_effect()
    def decay(this):
        #visual bleeding,
        pygame.draw.line(panel,(255,0,0),this.pos,point_of_orbit(this.pos,random.randint(0,360),random.randint(1,10)),10)
        if (this.nutrition < 0):
            del entity_object_array[entity_object_array.index(this)]
            return
        this.nutrition -= 0.1 / lag_comp
        if (random.randint(1,200) != 20):
            return
        decay = food()
        #return their biomass to the ecosytem
        decay.pos = [this.pos[0] + 2 + random.randint(-7,5),this.pos[1] + 2 + random.randint(-7,5)]
        food_object_array.append(decay)
    def run(this,obj):
        # the fight or flight respinse
        this.wait_for = 0
        this.target = None
        this.dummy = dummy()
        this.dummy.pos = point_of_orbit(this.pos, obj.rotation + random.randint(-5,5), 50) # face them precisely away from their pursuer 
        this.epinephrine+=0.7 * this.cns_depressant # add adrenaline, dulled by exhaustion
        this.epinephrine = clamp(this.epinephrine,20 * this.cns_depressant,0)
        if (clamp(this.dummy.pos[0],650,150) != this.dummy.pos[0] or clamp(this.dummy.pos[1],550,50) != this.dummy.pos[1]): # check if they are being chased off the map
                this.dummy = dummy()
        this.wander()
class carnivore:
    def __init__(this):
        this.pos = [random.randint(150,650),random.randint(50,550)]
        this.rotation = 0
        this.strand_stomach = generate_dna_sequence(7)
        this.strand_bmr = generate_dna_sequence(3)
        this.strand_sight = generate_dna_sequence(6)
        this.strand_speed = generate_dna_sequence(3)
        this.strand_reprod = generate_dna_sequence(8)
        this.strand_litter_size = generate_dna_sequence(1)
        this.sight = read_dna_binary(this.strand_sight) + 30
        this.target = None
        this.dummy = None
        this.stomach_max = read_dna_binary(this.strand_stomach) + 70
        this.stomach = this.stomach_max / 2
        this.speed = read_dna_binary(this.strand_speed) - 1
        this.bmr = read_dna_binary(this.strand_bmr)+1
        this.litter_size = read_dna_binary(this.strand_litter_size)+1
        this.nose = 0
        this.egg_progress = 0
        this.dead = False
        this.wait_for = 0
    def draw(this):
        this.nose = point_of_orbit(this.pos,this.rotation,10)
        pygame.draw.line(panel,vgui_entity_nose,this.pos,this.nose,3)#nose layer
        pygame.draw.circle(panel,vgui_entity_carnivore,this.pos,5)#body layer
    def sight_check(this,target_vec):
        p_1 = point_of_orbit(this.pos, this.rotation + 270, this.sight)
        p_2 = point_of_orbit(this.pos, this.rotation + 90, this.sight)
        p_3 = point_of_orbit(this.pos, this.rotation, this.sight)
        if (is_in_triangle(p_1,p_2,p_3,target_vec)):
            return True
        else:
            return False
    def create_move(this):
        try:
            entity_object_array.index(this.target)
        except:
            this.target = None
            return
        if (not this.sight_check(this.target.pos)):
            this.target = None
            #give the prey a chance to escape, if they are fast enough 
            return
        this.target.run(this) # trigger their fight or flight response
        this.rotation = rad_to_deg(this.pos,this.target.pos)
        this.pos = think_next_move(this.target.pos,this.pos,this.speed + 2)
        if (distance_to(this.pos,this.target.pos) <= (4/lag_comp) + 1):
            log_index.append(log_entry("herbivore killed: ","victim genes",str(this.target.introgenic_dna))) 
            this.target.kill()
            this.stomach+=this.target.nutrition * 0.65
            this.target.nutrition-=this.target.nutrition * 0.65
            this.target = None
            this.wait_for = random.randint(math.ceil(160 / this.bmr),math.ceil(400 / this.bmr)) # prevent them from killing too many at once in the same area 
    def wander(this):
        if (this.dummy == None):
            this.dummy = dummy()
            this.dummy.pos = point_of_orbit(this.pos,random.randint(1,360),random.randint(40,120))
            while (clamp(this.dummy.pos[0],650,150) != this.dummy.pos[0] or clamp(this.dummy.pos[1],550,50) != this.dummy.pos[1]):
                this.dummy.pos = point_of_orbit(this.pos,random.randint(1,360),random.randint(40,120))
        this.rotation = rad_to_deg(this.pos,this.dummy.pos) 
        this.pos = think_next_move(this.dummy.pos,this.pos,this.speed + 2)
        if (distance_to(this.pos,this.dummy.pos) <= (4/lag_comp) + 1):
             this.dummy = None
             this.wait_for = random.randint(math.ceil(60 / this.bmr),math.ceil(250 / this.bmr))
    def kill(this):
        this.dead = True
    def decay(this):
        x = 2 # as of right now predators cant be killed so this is empty
class dummy:
    def __init__(this): #creates a fake creature for the organism to "chase", can be fed into wander and create move 
        this.pos = [random.randint(150,650),random.randint(50,550)]
        this.pos[0] = clamp(this.pos[0],650,150)
        this.pos[1] = clamp(this.pos[1],550,50)
for i in range(Config["layer-1"]["food"]):
    #add starting food
    food_object_array.append(food())
for i in range(Config["layer-1"]["herbivores"]):
    #add starting herbivores
    entity_object_array.append(herbivore())
for i in range(Config["layer-1"]["carnivores"]):
    #add starting carnivores 
    hunter_object_array.append(carnivore())
class button: #probably will revisit but looks alright
    def __init__(this,position_vec,label_str,color = vgui_fore,color_hover = vgui_state_4,color_text = vgui_aux_text_internal):
        this.pos = position_vec # button pos
        this.label = label_str # button label
    def draw(this):
        c_vec = pygame.mouse.get_pos() # mouse pos
        c_bool = pygame.mouse.get_pressed()[0] # L mouse state
        #pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52,12))#bounding scope
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],60,13))#fore scope
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 60 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 13):
            if (c_bool):
                return True
            else:
                #pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52,12))#bounding scope
                pygame.draw.rect(panel, vgui_state_4, pygame.Rect(this.pos[0],this.pos[1],60,13))#aux scope
                txt = font_alt.render(this.label, True, vgui_aux_text_internal)
                panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 30,this.pos[1]))#overlap scope
                return False
        txt = font_alt.render(this.label, True, vgui_aux_text_internal)
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 30,this.pos[1]))#overlap scope
class slider: #too primitive
    def __init__(this,position_vec,label_str,min_int,max_int,value_int,invert = False,experimental = False):
        this.pos = position_vec
        this.label = label_str
        this.min = min_int
        this.max = max_int#value = (cursor.x - x) / (float(position) / float(max_value))
        this.val = abs((value_int / (this.max-this.min)) * 100) # convert to screen
        this.invert = invert
        this.experimental = experimental
    def draw(this):
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        #pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,102,12))#bounding scope
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],100,12))#fore scope
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,this.val + 2,14)) # the slider bound rect
        if (this.experimental):
            for i in range(math.floor(this.val)):
                if (this.invert):
                    pygame.draw.line(panel,(i*2.55,255 - (i*2.55),0),(this.pos[0] + i,this.pos[1]),(this.pos[0] + i,this.pos[1]+12))
                else:
                    pygame.draw.line(panel,(255 - (i*2.55),i*2.55,0),(this.pos[0] + i,this.pos[1]),(this.pos[0] + i,this.pos[1]+12))
        elif (this.invert):
            pygame.draw.rect(panel, (this.val*2.55,255 - (this.val*2.55),0), pygame.Rect(this.pos[0],this.pos[1],this.val,12))#aux scope
        else:
            pygame.draw.rect(panel, (255 - (this.val*2.55),this.val*2.55,0), pygame.Rect(this.pos[0],this.pos[1],this.val,12))#aux scope
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 100 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 12 and c_bool):
            this.val = c_vec[0] - this.pos[0]
        panel.blit(ui_font_scale_3.render(str(math.floor(((this.val / 100) * (this.max - this.min)) + this.min)), True, vgui_aux_text_external),(this.pos[0]+102,this.pos[1]))#overlap scope
        txt = ui_font_scale_3.render(this.label, True, vgui_aux_text_external)
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 50,this.pos[1] + 13))#overlap scope
        return math.floor(((this.val / 100) * (this.max - this.min)) + this.min) # convert to value 
class check_box: #this looks nice 
    def __init__(this,position_vec,label_str,state):
        this.pos = position_vec
        this.label = label_str
        this.state = state
        this.c_state = False
        this.hovered = False
    def draw(this):
        this.hovered = False
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        #pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,12,12))#bounding scope
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],14,14))#fore scope
        pygame.draw.rect(panel, vgui_color_OFF, pygame.Rect(this.pos[0] + 3,this.pos[1] + 3,8,8))#aux scope
        if (this.state):
            pygame.draw.rect(panel, vgui_color_ON, pygame.Rect(this.pos[0] + 3,this.pos[1] + 3,8,8))#aux scope
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 10 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10):
            this.hovered = True
            if (c_bool != this.c_state and c_bool):
                this.state = not this.state
            #elif(this.state):
             #   pygame.draw.rect(panel, vgui_state_1, pygame.Rect(this.pos[0] + 3,this.pos[1] + 3,8,8))#overlap scope
            #else:
             #   pygame.draw.rect(panel, vgui_state_2, pygame.Rect(this.pos[0] + 3,this.pos[1] + 3,8,8))#overlap scope
        this.c_state = c_bool
        panel.blit(ui_font_scale_3.render(this.label, True, vgui_aux_text_external),(this.pos[0]+15,this.pos[1] + 2))#overlap scope
        return this.state
def draw_visual_bar(value,minim,maxim,pos,label,color = vgui_state_1):
        #pygame.draw.rect(panel, vgui_bounding, pygame.Rect(pos[0] - 1,pos[1] - 1,102,12))#bounding scope
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(pos[0],pos[1],100,10))#fore scope
        pygame.draw.rect(panel, color, pygame.Rect(pos[0],pos[1],((value / (maxim-minim)) * 100),10))#fore scope
        panel.blit(ui_font_scale_3.render(str(math.floor(((value / 100) * (maxim - minim)) + minim)), True, vgui_aux_text_external),(pos[0]+102,pos[1]))#overlap scope
        txt = ui_font_scale_3.render(label, True, vgui_aux_text_external)
        panel.blit(txt,(pos[0] - (txt.get_width() / 2) + 50,pos[1] + 11))#overlap scope
class color_selector: #this also looks nice
    def __init__(this,position_vec,current_col_vec,label_str):
        this.pos = position_vec
        this.col = current_col_vec
        this.state = False
        this.c_state = False
        this.label = label_str
        #this.invert = check_box((position_vec[0] + 51,position_vec[1]+40),"flip blue",False)
        #this.remove = check_box((position_vec[0] + 51,position_vec[1]+30),"no blue",False)
        this.extras = selection_interface_s((position_vec[0] + 51,position_vec[1]),["default","flip blue","no blue"],0)
    def draw(this):
        c_vec = pygame.mouse.get_pos() #mouse pos
        c_bool = pygame.mouse.get_pressed()[0]# L mouse pos
        if (this.state):
            pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52,52))#bounding scope
            for red in range(50):
                for green in range(50):
                    if (this.extras.selected == 1): # different settings for different color spectrums
                        blue = (red + green) // 2
                    elif (this.extras.selected == 2):
                        blue = 0
                    else:
                        blue = (50 - ((red + green) // 2))
                    pygame.draw.rect(panel, (red * 5,green * 5,blue * 5), pygame.Rect(this.pos[0] + red,this.pos[1] + green,1,1))#aux scope
                    #pygame.draw.rect(panel, (red * 5,green * 5,blue * 5), pygame.Rect(this.pos[0] + red +2,this.pos[1] + green + 2,2,2))#aux scope
            if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 50 and c_bool and c_bool != this.c_state): # if hovered, clicked and not double pressed
                if (this.extras.selected == 1): # convert the col on the pressed cursor 
                    this.col = ((c_vec[0] - this.pos[0]) * 5,(c_vec[1] - this.pos[1]) * 5, (((c_vec[0] - this.pos[0])+(c_vec[1] - this.pos[1])) // 2) * 5)
                elif (this.extras.selected == 2):
                    this.col = ((c_vec[0] - this.pos[0]) * 5,(c_vec[1] - this.pos[1]) * 5,0)
                else:
                    this.col = ((c_vec[0] - this.pos[0]) * 5,(c_vec[1] - this.pos[1]) * 5,(50 - (((c_vec[0] - this.pos[0]) + (c_vec[1] - this.pos[1])) // 2)) * 5)
            elif (c_bool and c_bool != this.c_state and not this.extras.hovered):
                this.state = not this.state
            pygame.draw.rect(panel, vgui_important, pygame.Rect(this.c2s()[0] - 1,this.c2s()[1] - 1,4,4))#overlay scope
            pygame.draw.rect(panel, this.col, pygame.Rect(this.c2s()[0],this.c2s()[1],2,2))#overlay scope
            #pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] + 50,this.pos[1] - 1,12,12))#overlay scope
            #pygame.draw.rect(panel, this.col, pygame.Rect(this.pos[0] + 51,this.pos[1],10,10))#overlay scope
            #this.invert.draw()
            #this.remove.draw()
            this.extras.draw()
        else:
            pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,32,12))#bounding scope
            pygame.draw.rect(panel, this.col, pygame.Rect(this.pos[0],this.pos[1],30,10))#aux scope
            if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 30 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10 and c_bool and c_bool != this.c_state):
                this.state = not this.state
            this.c_state = c_bool
            panel.blit(ui_font_scale_3.render(this.label, True, vgui_aux_text_external),(this.pos[0]+31,this.pos[1]))#overlap scope
        this.c_state = c_bool
    def c2s(this): #color to screen
        reversed_red = (this.col[0] / 5) + this.pos[0]
        reversed_green = (this.col[1] / 5) + this.pos[1]
        return (reversed_red,reversed_green)
class selection_interface_s: #meh
    def __init__(this,position_vec,selections_array,selected_pointer):
        this.pos = position_vec
        this.selections = selections_array
        this.selected = selected_pointer
        this.state = False
        this.c_state = False
        this.hovered = False
    def draw(this):
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52,12))#bounding scope
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],50,10))#fore scope
        txt = ui_font_scale_3.render(this.selections[this.selected], True, vgui_aux_text_internal)
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1]))#overlap scope
        this.hovered = False
        if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10):
            this.hovered = True
            if (c_bool and c_bool != this.c_state):
                this.state = not this.state
                this.c_state = this.state
        if (this.state):
            for selection in range(len(this.selections)):
                pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1 + 10 + (selection * 10),52,12))#bounding scope
                pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1] + 10 + (selection * 10),50,10))#fore scope
                txt = ui_font_scale_3.render(this.selections[selection], True, vgui_aux_text_internal)
                panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1] + 10 + (selection * 10)))#overlap scope
                if (selection == this.selected):
                    pygame.draw.rect(panel, vgui_state_1, pygame.Rect(this.pos[0],this.pos[1] + 10 + (selection * 10),50,10))#fore scope
                    txt = ui_font_scale_3.render(this.selections[selection], True, vgui_fore,)
                    panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1] + 10 + (selection * 10)))#overlap scope
                if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] + 10 + (selection * 10) and c_vec[1] < this.pos[1] + 20 + (selection * 10)):
                    this.hovered = True
                    if (c_bool and c_bool != this.c_state):
                        this.selected = selection
                        this.state = not this.state
        this.c_state = c_bool
class selection_interface_m: #better but still meh
    def __init__(this,position_vec,selections_array,selected_array,label_str):
        this.pos = position_vec
        this.selections = selections_array
        this.selected = selected_array
        this.state = False
        this.c_state = False
        this.label = label_str
    def draw(this):
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,52,12))#bounding scope
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],50,10))#fore scope
        txt = ui_font_scale_3.render(this.label, True, vgui_aux_text_internal)
        panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1]))#overlap scope
        if (this.state):
            for selection in range(len(this.selections)):
                pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1 + 10 + (selection * 10),52,12))#bounding scope
                pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1] + 10 +(selection * 10),50,10))#fore scope
                txt = ui_font_scale_3.render(this.selections[selection], True, vgui_aux_text_internal)
                panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1] + 10 +(selection * 10)))#overlap scope
                if (this.selected[selection]):
                    pygame.draw.rect(panel, vgui_state_4, pygame.Rect(this.pos[0],this.pos[1] + 10 + (selection * 10),50,10))#fore scope
                    txt = ui_font_scale_3.render(this.selections[selection], True, vgui_aux_text_internal)
                    panel.blit(txt,(this.pos[0] - (txt.get_width() / 2) + 25,this.pos[1] + 10 + (selection * 10)))#overlap scope
                if (c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] + 10 + (selection * 10) and c_vec[1] < this.pos[1] + 20 + (selection * 10) and c_bool and c_bool != this.c_state):
                    this.selected[selection] = not this.selected[selection]
        if ((c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 50 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + 10 and c_bool and c_bool != this.c_state)):
            this.state = not this.state
        this.c_state = c_bool
class warning:
    def __init__(this,pos,label,label2 = "",label3 = ""):
        this.label = label
        this.label2 = label2
        this.label3 = label3
        this.pos = pos
        this.button = button([this.pos[0] + 50 ,this.pos[1] + 40],"ok")
    def draw(this):
        pygame.draw.rect(panel, vgui_bounding, pygame.Rect(this.pos[0] - 1,this.pos[1] - 1,102,52))#bounding scope
        pygame.draw.rect(panel, vgui_warning_1, pygame.Rect(this.pos[0],this.pos[1],100,50))#fore scope
        panel.blit(ui_font_scale_3.render(this.label, True, vgui_aux_text_internal, vgui_warning_1),(this.pos[0],this.pos[1] + 5))#overlap scope
        panel.blit(ui_font_scale_3.render(this.label2, True, vgui_aux_text_internal, vgui_warning_1),(this.pos[0],this.pos[1] + 15))#overlap scope
        panel.blit(ui_font_scale_3.render(this.label3, True, vgui_aux_text_internal, vgui_warning_1),(this.pos[0],this.pos[1] + 25))#overlap scope
        if (this.button.draw()):
            return True
        return False
class verticle_slider:
    def __init__(this,pos,mini,maxi,val,length):
            this.pos = pos
            this.min = mini
            this.max = maxi
            this.val = length - abs((val / (this.max-this.min)) * length)
            this.len = length
    def draw(this):
        pygame.draw.rect(panel, vgui_fore, pygame.Rect(this.pos[0],this.pos[1],13,this.len))
        pygame.draw.rect(panel, vgui_aux_text_internal, pygame.Rect(this.pos[0],this.val-20,13,20))
        #pygame.draw.line(panel,foreground,(this.pos[0],this.val - 10),(this.pos[0] + 13,this.val - 10))
        c_vec = pygame.mouse.get_pos()
        c_bool = pygame.mouse.get_pressed()[0]
        if ((c_vec[0] > this.pos[0] and c_vec[0] < this.pos[0] + 13 and c_vec[1] > this.pos[1] and c_vec[1] < this.pos[1] + this.len)):
            pygame.draw.rect(panel, (144,144,144), pygame.Rect(this.pos[0],this.val - 20,13,20))
            if c_bool:
                this.val = c_vec[1] + this.pos[1]
        return this.max - math.floor(((this.val / this.len) * (this.max - this.min)) + this.min)
class group_box:
    def __init__(this,pos,label,base,height):
        this.pos = pos
        this.label = ui_font_scale_3.render(label, True, vgui_aux_text_external,foreground)
        #this.label.set_alpha(127)
        this.b = base
        this.h = height
    def draw(this):
        #pygame.draw.rect(panel, vgui_group_fore, pygame.Rect(this.pos[0],this.pos[1],this.b,this.h))#fore scope
        pygame.draw.line(panel,vgui_bounding,this.pos,(this.pos[0] + this.b,this.pos[1]))
        pygame.draw.line(panel,vgui_bounding,this.pos,(this.pos[0],this.pos[1] + this.h))
        pygame.draw.line(panel,vgui_bounding,(this.pos[0] + this.b,this.pos[1]),(this.pos[0] + this.b,this.pos[1] + this.h))
        pygame.draw.line(panel,vgui_bounding,(this.pos[0] + this.b,this.pos[1] + this.h),(this.pos[0],this.pos[1] + this.h))
        panel.blit(this.label,(this.pos[0] + (this.b // 5),this.pos[1] - 5))

def handle_metrics():
    global NPP_SAMPLES
    #handle all graphs
    pygame.draw.rect(panel, vgui_fore, pygame.Rect(1350,10,300,300))#fore scope
    panel.blit(ui_font_scale_3.render("NPP TREND - RED", True, vgui_aux_text_external),(1350,310))
    #pygame.draw.rect(panel, vgui_bounding, pygame.Rect(1350,350,300,300))#fore scope
    panel.blit(ui_font_scale_3.render("TSC TREND - BLUE", True, vgui_aux_text_external),(1560,310))
    try:
        NPP_HEIGHT = max(NPP_SAMPLES) # find the heights of all data to find, if there is no data their is an error when calling max(), so there is a catch statement
        TSC_HEIGHT = max(TSC_SAMPLES)
        #sight_height = max(sight_average)
    except:
        return
    if len(NPP_SAMPLES) > 300: # recess the graph scroll when it goes off screen
        for data_entry in NPP_SAMPLES:
            if NPP_SAMPLES.index(data_entry) % 2 == 0:
                del NPP_SAMPLES[NPP_SAMPLES.index(data_entry)]
    if len(TSC_SAMPLES) > 300:
        for data_entry in TSC_SAMPLES:
            if TSC_SAMPLES.index(data_entry) % 2 == 0:
                del TSC_SAMPLES[TSC_SAMPLES.index(data_entry)]
    for data_point in NPP_SAMPLES:
        pygame.draw.rect(panel, (255,0,0), pygame.Rect(1350 + NPP_SAMPLES.index(data_point),310 - math.ceil((data_point / NPP_HEIGHT) * 300),1,1))#bounding scope
        #adds a dot for each point
        try:
            pygame.draw.line(panel,(255,0,0),(1350 + NPP_SAMPLES.index(data_point),310 - math.ceil((data_point / NPP_HEIGHT) * 300)),(1350 + NPP_SAMPLES.index(data_point) + 1,310 - math.ceil((NPP_SAMPLES[NPP_SAMPLES.index(data_point) + 1] / NPP_HEIGHT) * 300)))
            #draw a line from data point to data point
        except:
            continue
    for data_point in TSC_SAMPLES:
        pygame.draw.rect(panel, (0,0,255), pygame.Rect(1350 + TSC_SAMPLES.index(data_point),310 - math.ceil((data_point / TSC_HEIGHT) * 300),1,1))#bounding scope
        try:
            pygame.draw.line(panel,(0,0,255),(1350 + TSC_SAMPLES.index(data_point),310 - math.ceil((data_point / TSC_HEIGHT) * 300)),(1350 + TSC_SAMPLES.index(data_point) + 1,310 - math.ceil((TSC_SAMPLES[TSC_SAMPLES.index(data_point) + 1] / TSC_HEIGHT) * 300)))
        except:
            continue
    #for data_point in sight_average:
      #  pygame.draw.rect(panel, (255,0,0), pygame.Rect(1350 + sight_average.index(data_point),650 - math.ceil((data_point / sight_height) * 300),2,2))#bounding scope
        #try:
          #  pygame.draw.line(panel,(255,0,0),(1350 + sight_average.index(data_point),650 - math.ceil((data_point / sight_height) * 300)),(1350 + sight_average.index(data_point) + 1,650 - math.ceil((sight_average[sight_average.index(data_point) + 1] / sight_height) * 300)))
        #except:
            #continue
vgui_button_back = button((1,589),"<- back")
vgui_button_exit = button((749,1)," quit ", (255,0,0),(180,0,0),(20,20,20))
vgui_button_start = button((375,300),"start")
vgui_button_options = button((375,315),"options")
vgui_button_theme = button((375,330),"theme")
vgui_button_entity_list_manager = button((375,345),"edit ents")

vgui_slider_food = slider((100,75),"food amount",0,5000,Config["layer-1"]["food"])
xspeed = slider((20,75),"change logo speed x ",0,10,x_speed,True,True)
yspeed = slider((20,100),"change logo speed y ",0,10,y_speed,True,True)
vgui_slider_herb = slider((100,100),"herbivore amount",0,100,Config["layer-1"]["herbivores"])
vgui_slider_carn = slider((100,125),"carnivore amount",0,20,Config["layer-1"]["carnivores"],True)

#vgui_slider_muta = slider((100,150),"mutation chance per 10 seconds",0,100,40)

vgui_slider_ray_lazy = slider((500,75),"lazy tracing",0,400,20)
vgui_slider_ray_mult = slider((500,100),"speed multiplier",1,10,1)
vgui_slider_ray_add = slider((500,125),"drunk ray",1,10,5)
vgui_slider_photosynth = slider((660,50),"GPP",1,1000,500)
vgui_slider_birth_muta_chance = slider((660,250),"mutation chance birth %",0,100,50,True)
vgui_slider_random_muta_chance = slider((660,200),"mutation chance random %",0,100,10,True)
vgui_slider_sim_slow_val = slider((36,100),"slow amount",1,100,5,True)

vgui_checkbox_sim_slow_bool = check_box((1,100),"slow",False)
vgui_checkbox_sim_lag_comp = check_box((1,150),"lag comp",True)

vgui_checkbox_ray_visualise = check_box((500,160),"visualise",False)
vgui_checkbox_visualise_math = check_box((100,180),"visualise math",False)
vgui_checkbox_ray_master = check_box((100,195),"ray tracing",False)
#vgui_checkbox_ray_ehhh = check_box((100,210),"ehhh",False)
vgui_color_ray_visualise_1 = color_selector((570,160),vgui_ray_beam,"beam")
vgui_color_ray_visualise_2 = color_selector((570,212),vgui_ray_broken,"broken")

vgui_color_state_0 = color_selector((50,50),vgui_state_0,"vgui_state_0")
vgui_color_state_1 = color_selector((50,105),vgui_state_1,"vgui_state_1")
vgui_color_state_2 = color_selector((50,160),vgui_state_2,"vgui_state_2")
vgui_color_state_3 = color_selector((50,215),vgui_state_3,"vgui_state_3")
vgui_color_state_4 = color_selector((50,270),vgui_state_4,"vgui_state_4")
vgui_color_state_5 = color_selector((50,325),vgui_state_5,"vgui_state_5")
vgui_color_bounding = color_selector((50,380),vgui_bounding,"vgui_bounding")
foreground_color = color_selector((50,435),foreground,"foreground")
vgui_fore_color = color_selector((50,490),vgui_fore,"vgui_fore")
vgui_herbivore_color = color_selector((150,50),vgui_entity_herbivore,"vgui_entity_herbivore")
vgui_carnivore_color = color_selector((150,105),vgui_entity_carnivore,"vgui_entity_carnivore")
vgui_text_internal_color = color_selector((150,215),vgui_aux_text_internal,"vgui_aux_text_internal")
vgui_text_external_color = color_selector((150,270),vgui_aux_text_external,"vgui_aux_text_external")
vgui_egg_color = color_selector((150,325),vgui_herbivore_egg,"vgui_herbivore_egg")
vgui_nose_color = color_selector((150,160),vgui_entity_nose,"vgui_entity_nose")
vgui_color_dead = color_selector((150,380),vgui_entity_dead,"vgui_entity_dead")
vgui_slc_ray_ignore = selection_interface_m((500,212),["food","creatures"],[False,False],"ignore")
vgui_color_ON_state = color_selector((150,500),vgui_color_ON,"vgui_color_ON")
vgui_color_OFF_state = color_selector((150,560),vgui_color_OFF,"vgui_color_OFF")
vgui_color_blindness = selection_interface_s((250,50),["normal","deutera","protano","tritano"],0)

vgui_warning_conf = warning([300,250],"first time setup", "because didnt find","config")
environment = group_box([60,60],"environment",180,200)
raytracing = group_box([460,60],"ray tracing",180,200)

log_box = group_box([799,25],"",400,550)
mut_reasons = ["radiation","protein misfold","mitosis error"]
def sim_thread():
    global balance
    global NPP_SAMPLES
    global NPP
    global TSC
    global sight_average
    NPP = 0
    TSC = 0
    for food_obj in food_object_array:
        food_obj.draw()
        NPP += food_obj.carbs + food_obj.protein
    for egg_obj in egg_object_array:
        egg_obj.draw()
        egg_obj.tick()
    for herbivore in entity_object_array:
        herbivore.draw()
        if (herbivore.dead):
            herbivore.decay()
            continue
        if ((tick % 2000 * lag_comp) == 0) and random.randint(0,100) < vgui_slider_random_muta_chance.val: # random mutation 
                index_to_patch = herbivore.genes.index(random.choice(herbivore.genes))
                mutated = create_mutation(herbivore.genes[index_to_patch])
                try:
                    mutated[1]
                except:
                    mutated = [mutated]
                    mutated.append("UNEDITABLE") # stop empty dna 
                old_strand = herbivore.genes[index_to_patch]
                log_index.append(log_entry("a mutation has occured due to " + random.choice(mut_reasons) + " type: " + mutated[1]," details",str(str(old_strand) + "  ->  " +  str(mutated[0])) + " -> " + str(read_dna_binary(old_strand)) + " -> " + str(read_dna_binary(mutated[0]))))
                herbivore.refold()
                herbivore.genes[index_to_patch] = mutated[0]
        TSC += herbivore.stomach
        if (herbivore.wait_for > 0):
            herbivore.wait_for -= 1 / lag_comp
            continue
        if (herbivore.stomach <= 0):
            herbivore.dead = True
            log_index.append(log_entry("herbivore starved"," genes",str(herbivore.introgenic_dna)))
            continue
        if herbivore.epinephrine > 0:
            herbivore.epinephrine -= 0.1 / lag_comp
            herbivore.cns_depressant += 0.01
        elif (herbivore.cns_depressant > 0):
            herbivore.cns_depressant -= 0.03
        if (herbivore.egg_progress > (900 / balance)):
            for i in range(herbivore.litter_size):
                egg_object_array.append(egg([herbivore.pos[0] + random.randint(1,3),herbivore.pos[1] + random.randint(1,3)],herbivore.genes,herbivore.introgenic_dna))
                herbivore.stomach -= herbivore.stomach_max * 0.2
                herbivore.egg_progress = -200 / balance
        elif herbivore.stomach > (herbivore.stomach_max * 0.9):
            herbivore.egg_progress += (1 / lag_comp) * balance
        if (herbivore.target != None):
            herbivore.create_move()
        else:
            if (herbivore.nose[0] > herbivore.pos[0]):
                radian = 0
            else:
                radian = 1
            for food in food_object_array:
                if (radian == 0 and food.pos[0] < herbivore.pos[0]):
                    continue
                if (radian == 1 and food.pos[0] > herbivore.pos[0]):
                    continue
                if abs(food.pos[0] - herbivore.pos[0]) > herbivore.sight:
                    continue
                if abs(food.pos[1] - herbivore.pos[1]) > (herbivore.sight // 2):
                    continue
                if (not herbivore.sight_check(food.pos)):
                    continue
                herbivore.target = food
                break
            herbivore.wander()
        herbivore.stomach -= (herbivore.bmr / (100 * lag_comp))
        herbivore.stomach = clamp(herbivore.stomach,herbivore.stomach_max,0)
        herbivore.cns_depressant = clamp(herbivore.cns_depressant,1,0)
    for carnivore in hunter_object_array:
        carnivore.draw()
        if (carnivore.dead):
            carnivore.decay()
            continue
        if (carnivore.wait_for > 0):
            carnivore.wait_for -= 1 / lag_comp
            continue
        #if (carnivore.stomach <= 0):
            #carnivore.kill()
            #continue
        if (carnivore.target != None):
            carnivore.create_move()
        else:
            if (carnivore.nose[0] > carnivore.pos[0]):
                radian = 0
            else:
                radian = 1
            for prey in entity_object_array:
                if (prey.dead):
                    continue
                if (radian == 0 and prey.pos[0] < carnivore.pos[0]):
                    continue
                if (radian == 1 and prey.pos[0] > carnivore.pos[0]):
                    continue
                if abs(prey.pos[0] - carnivore.pos[0]) > carnivore.sight:
                    continue
                if abs(prey.pos[1] - carnivore.pos[1]) > (carnivore.sight // 2):
                    continue
                if (not carnivore.sight_check(prey.pos)):
                    continue
                carnivore.target = prey
                break
            carnivore.wander()
        carnivore.stomach -= (carnivore.bmr / (100 * lag_comp))
        carnivore.stomach = clamp(carnivore.stomach,carnivore.stomach_max,0)
    if tick % 15 == 0:
        NPP_SAMPLES.append(NPP)
        TSC_SAMPLES.append(TSC)
        total = 0
        for gene_holder in entity_object_array:
            total+=gene_holder.sight
        an_average = total / len(entity_object_array)
        sight_average.append(an_average)
        
    
def vgui_thread():
    global NPP
    global balance
    if (vgui_checkbox_sim_slow_bool.draw()):
        time.sleep(0.1 * (vgui_slider_sim_slow_val.draw() / 100))
    vgui_checkbox_sim_lag_comp.draw()
    vgui_slider_photosynth.draw()
    vgui_slider_birth_muta_chance.draw()
    vgui_slider_random_muta_chance.draw()
    txt = ui_font_scale_3.render("warning! really crazy stuff could happen at high mutation rates ", True, vgui_aux_text_internal)
    panel.blit(txt,(400 - ((txt.get_width() + txt.get_width()) / 2),600)) #display main text
    draw_visual_bar(balance * 100,1,500,(660,150),"balance",(255,255,0))
    
def simulation():
    global tab
    global tick 
    if (random.randint(1,math.ceil(1000 * lag_comp)) < vgui_slider_photosynth.val):
        food_object_array.append(food())
    pygame.draw.rect(panel, (90,90,90), pygame.Rect(150,50,500,500))#sim area
    if (vgui_button_back.draw()):
        tab = 0
    sim_thread()
    vgui_thread()
    tick+=1
def options():
    global tab
    global vgui_ray_beam
    global vgui_ray_broken
    if (vgui_button_back.draw()):
        tab = 0
    environment.draw()
    raytracing.draw()
    Config["layer-1"]["food"] = vgui_slider_food.draw()
    Config["layer-1"]["herbivores"] = vgui_slider_herb.draw()
    Config["layer-1"]["carnivores"] = vgui_slider_carn.draw()
    #vgui_slider_muta.draw()
    #vgui_checkbox_visualise_math.draw()
    vgui_checkbox_ray_master.draw()
    vgui_slider_ray_lazy.draw()
    vgui_slider_ray_mult.draw()
    vgui_slider_ray_add.draw()
    vgui_checkbox_ray_visualise.draw()
    vgui_color_ray_visualise_1.draw()
    vgui_color_ray_visualise_2.draw()
    vgui_slc_ray_ignore.draw()
    vgui_ray_beam = vgui_color_ray_visualise_1.col 
    vgui_ray_broken = vgui_color_ray_visualise_2.col
def theme():
    global tab
    global vgui_state_0
    global vgui_state_1
    global vgui_state_2
    global vgui_state_3
    global vgui_state_4
    global vgui_state_5
    global vgui_fore
    global foreground
    global vgui_bounding
    global vgui_entity_herbivore
    global vgui_entity_carnivore
    global vgui_aux_text_internal
    global vgui_aux_text_external
    global vgui_entity_nose
    global vgui_herbivore_egg
    global vgui_entity_dead
    if (vgui_button_back.draw()):
        tab = 0
    vgui_color_state_0.draw()
    vgui_color_state_1.draw()
    vgui_color_state_2.draw()
    vgui_color_state_3.draw()
    vgui_color_state_4.draw()
    vgui_color_state_5.draw()
    vgui_color_dead.draw()
    vgui_color_bounding.draw()
    foreground_color.draw()
    vgui_fore_color.draw()
    vgui_herbivore_color.draw()
    vgui_carnivore_color.draw()
    vgui_nose_color.draw()
    vgui_text_internal_color.draw()
    vgui_text_external_color.draw()
    vgui_egg_color.draw()
    vgui_color_ON_state.draw()
    vgui_color_OFF_state.draw()
    vgui_state_0 = vgui_color_state_0.col
    vgui_state_1 = vgui_color_state_1.col
    vgui_state_2 = vgui_color_state_2.col
    vgui_state_3 = vgui_color_state_3.col
    vgui_state_4 = vgui_color_state_4.col
    vgui_state_5 = vgui_color_state_5.col
    vgui_herbivore_egg = vgui_egg_color.col
    vgui_bounding = vgui_color_bounding.col
    foreground = foreground_color.col
    vgui_fore = vgui_fore_color.col
    vgui_color_blindness.draw()
    vgui_entity_herbivore = vgui_herbivore_color.col
    vgui_entity_carnivore = vgui_carnivore_color.col
    vgui_entity_nose = vgui_nose_color.col
    vgui_aux_text_internal = vgui_text_internal_color.col
    vgui_aux_text_external = vgui_text_external_color.col
    vgui_entity_dead = vgui_color_dead.col
def main_menu():
    global tab
    global x
    global y
    global img_size
    global x_speed
    global y_speed
    if vgui_button_theme.draw():
        tab = 3
    if vgui_button_start.draw():
        tab = 2
    if vgui_button_options.draw():
        tab = 1
    if (x + img_size[0] >= 1700) or (x <= 0):
        x_speed = -x_speed
    if (y + img_size[1] >= 800) or (y <= 0):
        y_speed = -y_speed
    x += x_speed / lag_comp
    y += y_speed / lag_comp
    if x_speed <  0:
        x_speed = -xspeed.draw()
    else:
        x_speed = xspeed.draw()
    if y_speed < 0:
        y_speed = -yspeed.draw()
    else:
        y_speed = yspeed.draw()
    panel.blit(dvd,(x,y))
def log_manager():
    global log_var
    pygame.draw.rect(panel,vgui_fore,pygame.Rect(810,25,380,750))
    txt = font_alt.render("simulation log (hover over yellow text for extra information)", True, (255,255,255))
    panel.blit(txt,(1000 - (txt.get_width() / 2),10))
    if (len(log_index) > 51):
        vgui_slider_scroll = verticle_slider([1200,25],0,len(log_index) - 51,log_var,750)
        #vgui_slider_temporary = slider((1200,125),"temporary log scroller",0,len(log_index) - 51,log_var,True)
        log_var = abs(vgui_slider_scroll.draw())
    for pointer in range(len(log_index)):
        log_index[len(log_index) - pointer - 1].handle_hover() #read backwards to fix overdrawing issue
def main():
    global lag_comp
    lag_comp = clamp(lag_comp,3,0.01)
    sample_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            json.dump(Config,open("config.json","w"))
            pygame.quit()
            sys. exit()
    panel.fill(foreground)
    handle_metrics()
    log_manager()
    if (tab == 0):
        main_menu()
    elif (tab == 1):
        options()
    elif (tab == 2):
        simulation()
    elif (tab == 3):
        theme()
    if (vgui_button_exit.draw()):
        json.dump(Config,open("config.json","w"))
        pygame.quit()
        sys. exit()
    #master.draw()
    #log.draw()
    #og_box.draw()
    pygame.display.flip()
    if ((time.time() - sample_time) != 0):
        lag_comp = ((math.ceil(1 / (time.time() - sample_time))) / 100) #based off 100 ticks,
#for i in range(100):
        #log_index.append(log_entry("test" + str(100 - i),"wefweufgweifisfdfds","why are you reading this"))
log_index.append(log_entry("a project made by henry frodsham"," read ","please familiarise yourself with the ui elements in options before starting the simulation"))
while True:
    summ = 0
    for i in entity_object_array:
        if i.dead:
            continue
        summ += 1
    balance = (len(hunter_object_array) / (((summ + (len(egg_object_array) // 2))) * 4) + 1)
    screen_size = panel.get_size()
    vgui_button_back = button((1,screen_size[1]-14),"<- back")
    master = group_box((0,0),"",screen_size[0] - 401,screen_size[1] - 1)
    log = group_box((0,0),"",1299,599)
    while vgui_warning_config:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                json.dump(Config,open("config.json","w"))
                pygame.quit()
                sys. exit()
        panel.fill(foreground)
        if (vgui_warning_conf.draw()):
            vgui_warning_config = False
        pygame.display.flip()
    main()
