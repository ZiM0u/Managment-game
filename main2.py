import pygame
import sys
from structures2 import Usine,Coffee,Serre,Road, PNJ
# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu de Gestion Isométrique")

# Couleurs
BACKGROUND_COLOR = (240, 240, 240)
GRID_COLOR = (200, 200, 255)
BORDER_COLOR = (250, 250, 250)
UI_COLOR = (220, 220, 220)
PNJ_SALARY=50

# Dimensions des tuiles isométriques
tile_width = 75
tile_height = 45
screen_offsetx = 7
screen_offsety = -5

# Informations du joueur
player_money = 1000


# Charger les images des boutons
build_button_img_raw = pygame.image.load('build_button.png').convert_alpha()
build_button_img=pygame.transform.scale(build_button_img_raw,(122,60))
sell_button_img_raw = pygame.image.load('sell_button.png').convert_alpha()
sell_button_img=pygame.transform.scale(sell_button_img_raw,(122,60))
panel_raw = pygame.image.load('pannel2featured.png').convert_alpha()
panel = pygame.transform.scale(panel_raw,(725,665))

menucase_raw = pygame.image.load('casemenu.png').convert_alpha()
menucase = pygame.transform.scale(menucase_raw,(160,115))

panel2 = pygame.image.load("panel.png").convert_alpha()
select_raw = pygame.image.load("select.png").convert_alpha()
select= pygame.transform.scale(select_raw,(80,60))

usine_tileset_raw = pygame.image.load("Design.png").convert_alpha()
usine_tileset =  pygame.transform.scale(usine_tileset_raw,(80,60))
coffee_raw = pygame.image.load("coffee.png").convert_alpha()
coffee =  pygame.transform.scale(coffee_raw,(80,60))

serre_raw = pygame.image.load("serre.png").convert_alpha()
serre =  pygame.transform.scale(serre_raw,(80,60))

sign_raw = pygame.image.load("case.png").convert_alpha()
sign = pygame.transform.scale(sign_raw,(100,100))

sell_cursor_raw = pygame.image.load("sell_cursor.png").convert_alpha()
sell_cursor =  pygame.transform.scale(sell_cursor_raw,(80,60))

road1_raw=pygame.image.load("road1.png").convert_alpha()
road1= pygame.transform.scale(road1_raw,(80,60))
road2_raw=pygame.image.load("road2.png").convert_alpha()
road2= pygame.transform.scale(road2_raw,(80,60))

pnj_icon_raw = pygame.image.load("pnj.png").convert_alpha()
pnj_icon = pygame.transform.scale(pnj_icon_raw,(80,60))

coinsign_raw = pygame.image.load("coinsign.png").convert_alpha()
coinsign = pygame.transform.scale(coinsign_raw,(50,40))

pnj1_raw = pygame.image.load("pnj1.png").convert_alpha()
pnj2_raw = pygame.image.load("pnj2.png").convert_alpha()
pnj1= pygame.transform.scale(pnj1_raw,(80,60))
pnj2=pygame.transform.scale(pnj2_raw,(80,60))
pnj_animation = [pnj1,pnj2]

pnj_go_icon_raw = pygame.image.load("pnj_go.png").convert_alpha()
pnj_go_icon =pygame.transform.scale(pnj_go_icon_raw,(80,60))

bigbox_raw = pygame.image.load("textbox.png").convert_alpha()
bigbox = pygame.transform.scale(bigbox_raw,(200,400))

# Charger la police personnalisée
font = pygame.font.Font('font.ttf', 21)
smallfont = pygame.font.Font('font.ttf', 15)
smallerfont= pygame.font.Font('font.ttf', 11)
middlefont=pygame.font.Font('font.ttf',18)

class Notification:
    def __init__(self, text, position, lifetime=3000, fade_time=1000):
        self.text = text
        self.position = list(position)  # Position on screen (x, y)
        self.lifetime = lifetime  # Total lifetime in milliseconds
        self.fade_time = fade_time  # Time over which it fades
        self.start_time = pygame.time.get_ticks()  # Record the time of creation
        self.alpha = 255  # Fully opaque to start

    def update(self, delta_time):
        current_time = pygame.time.get_ticks()
        time_alive = current_time - self.start_time

        # Calculate fade effect
        if time_alive > self.lifetime:
            self.alpha = 0  # Fully transparent
        elif time_alive > self.lifetime - self.fade_time:
            fade_progress = (self.lifetime - time_alive) / self.fade_time
            self.alpha = int(255 * fade_progress)
        
        # Move the notification upwards gradually
        self.position = (self.position[0],self.position[1]-(1.1 * delta_time))  # Adjust the speed as needed

    def draw(self, screen, font):
        # Create a surface with transparency
        text_surface = font.render(self.text, True, (0, 0, 0))
        sign_surface=pygame.transform.scale(sign_raw,((text_surface.get_width()+70),50))
        sign_surface.set_alpha(self.alpha)
        text_surface.set_alpha(self.alpha)
        screen.blit(sign_surface,self.position)
        screen.blit(text_surface, (self.position[0]+35,self.position[1]+15))

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.max_notifications = 5  # Limit number of visible notifications
        self.start_position = (240, 550)  # Starting position for the bottom notification (adjust as needed)
        self.notification_spacing = 10  # Space between notifications

    def add_notification(self, text):
        # Add the notification at the bottom-right of the panel
        new_position = (self.start_position[0], self.start_position[1] - len(self.notifications) * (50 + self.notification_spacing))  # Example position, adjust as needed
        self.notifications.append(Notification(text, new_position))

        
        # If we exceed the max, remove the oldest notification
        if len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)

    def update(self, delta_time):
        for notification in self.notifications[:]:
            notification.update(delta_time)
            if notification.alpha == 0:
                self.notifications.remove(notification)  # Remove when fully transparent

        # Reposition all notifications to push them upward
        for i, notification in enumerate(self.notifications):
            target_y = self.start_position[1] - i * (50 + self.notification_spacing)
            current_y = notification.position[1]
            
            # Smoothly move towards the target position
            notification.position = (notification.position[0], max(target_y, current_y - delta_time * 100))  # Speed of movement upwards

    def draw(self, screen, font):
        for notification in self.notifications:
            notification.draw(screen, font)

# Fonction de projection isométrique
def iso_projection(x, y):
    screen_x = ((x - y) * (tile_width // 2) + screen_width // 4)#-215
    screen_y = ((x + y) * (tile_height // 2) + screen_height // 4)#-120
    return screen_x, screen_y

# Fonction pour convertir des coordonnées isométriques en coordonnées de tuile
def iso_to_tile(iso_x, iso_y, tile_width, tile_height):
    tile_x = (iso_x // (tile_width // 2) + iso_y // (tile_height // 2)) // 2
    tile_y = (iso_y // (tile_height // 2) - iso_x // (tile_width // 2)) // 2
    return tile_x, tile_y

# Fonction pour dessiner une tuile isométrique avec des bords noirs
def draw_tile(x, y, color):
    x+=screen_offsetx
    y+=screen_offsety
    screen_x, screen_y = tile_to_iso(x, y,tile_width,tile_height)
 #   screen_x+=410
 #   screen_y+=150
    points = [
        (screen_x, screen_y),  # sommet supérieur
        (screen_x + tile_width // 2, screen_y + tile_height // 2),  # sommet droit
        (screen_x, screen_y + tile_height),  # sommet inférieur
        (screen_x - tile_width // 2, screen_y + tile_height // 2)  # sommet gauche
    ]

    # Dessiner le contour noir
    pygame.draw.polygon(screen, BORDER_COLOR, points, 2)

    # Dessiner l'intérieur de la tuile avec la couleur choisie
    pygame.draw.polygon(screen, color, points)
    
def draw_usines(usine_list,mouse_pos):
    for u in usines_list:
        iso_x,iso_y = tile_to_iso(u.position[0]-1,u.position[1],tile_width,tile_height)
        #iso_x, iso_y = iso_projection(u.position[0], u.position[1])
        #iso_x+=70
        #iso_y+=5
        
        usine_rect = usine_tileset.get_rect(topleft=(iso_x, iso_y))
        
        # Facteur de zoom
        scale_factor = 1.0
        if usine_rect.collidepoint(mouse_pos):  # Si la souris est au-dessus de l'usine
            scale_factor = 1.1  # Agrandir l'image à 110%
            #print(u.position)

        # Appliquer le zoom
        scaled_usine = pygame.transform.scale(usine_tileset, 
                                               (int(usine_tileset.get_width() * scale_factor), 
                                                int(usine_tileset.get_height() * scale_factor)))

        screen.blit(scaled_usine, (iso_x, iso_y))

def draw_coffee(coffee_list,mouse_pos):
    for c in coffee_list:
        iso_x,iso_y=tile_to_iso(c.position[0]-1,c.position[1],tile_width,tile_height)

        screen.blit(coffee,(iso_x,iso_y))

def draw_serre(serre_list, mouse_pos):
    for s in serre_list:
        iso_x,iso_y=tile_to_iso(s.position[0]-1,s.position[1],tile_width,tile_height)

        screen.blit(serre,(iso_x,iso_y))

def draw_road(road_list,mouse_pos):
    for r in road_list:
        iso_x,iso_y=tile_to_iso(r.position[0]-1,r.position[1],tile_width,tile_height)
        if r.flip == 1:
            current_road = road1
        else:
            current_road=road2
        screen.blit(current_road,(iso_x,iso_y))

def draw_pnj(pnj_list,mouse_pos):
    for p in pnj_list:
        iso_x,iso_y=tile_to_iso(p.position[0]-1,p.position[1],tile_width,tile_height)
        screen.blit(pnj_animation[p.animation_state],(iso_x,iso_y))
        
# Fonction pour dessiner l'interface utilisateur avec effets de survol
panel_rect = panel.get_rect(topleft=(488,-35))
panel2_rect = panel.get_rect(topleft=(20,0))
clickable_list = [menucase.get_rect(topleft=(772, 300)),
                  menucase.get_rect(topleft=(772, 385)),
                  menucase.get_rect(topleft=(772, 470)),
                  build_button_img.get_rect(topleft=(753, 170)),
                  sell_button_img.get_rect(topleft=(835, 170)),
                  coffee.get_rect(topleft=(50,100)),
                    usine_tileset.get_rect(topleft=(140,100)),
                    serre.get_rect(topleft=(50,220)),
                    road1.get_rect(topleft=(140,220)),
                    pnj_icon.get_rect(topleft=(50,330))]

def draw_ui(selected_usine=None):
    global build_selector
    # Panneau d'information à droite
    #pygame.draw.rect(screen, UI_COLOR, (762, 0, 220, screen_height))    
    
    screen.blit(panel2,panel2_rect)
    screen.blit(panel,panel_rect)
    # Affichage de l'argent
    money_text = font.render(f"{player_money}", True, BORDER_COLOR)
    screen.blit(money_text, (820, 30))
    screen.blit(coinsign,(780,23))
    #affichage de l'herbe à joie
    herb_text = smallfont.render("Herbe à",True,BORDER_COLOR)
    herb_text2 = smallfont.render(f"joie:{herb} kg",True,BORDER_COLOR)
    screen.blit(herb_text,(780,250))
    screen.blit(herb_text2,(770,270))
    screen.blit(sign,(240,5))
    day = middlefont.render(f"Day:{day_counter}",True,(0,0,0))
    screen.blit(day,(255,37))
    


    
    # Obtenir la position de la souris
    mouse_pos = pygame.mouse.get_pos()

    #TRANSFORMER LES REPETITIONS EN UNE BOUCLE AVEC CLICKABLE_ITEMS (necessaire d'associer image/rect à la classe des elements declickable

    #RIGHT PANEL
    #menucase_rect = menucase.get_rect(topleft=(772, 300))
    menucase_rect = clickable_list[0]
    if menucase_rect.collidepoint(mouse_pos):
        # Appliquer un effet de survol (par exemple, légèrement agrandir)
        menucase_hover = pygame.transform.scale(menucase, (int(menucase.get_width()*1.1), int(menucase.get_height()*1.1)))
        menucase_hover_rect = menucase_hover.get_rect(center=menucase_rect.center)
        screen.blit(menucase, menucase_hover_rect)
        screen.blit(bigbox,(520,200))
        
    else:
        screen.blit(menucase, menucase_rect)
        

    #menucase2_rect = menucase.get_rect(topleft=(772, 385))
    menucase2_rect = clickable_list[1]
    if menucase2_rect.collidepoint(mouse_pos):
        # Appliquer un effet de survol (par exemple, légèrement agrandir)
        menucase2_hover = pygame.transform.scale(menucase, (int(menucase.get_width()*1.1), int(menucase.get_height()*1.1)))
        menucase2_hover_rect = menucase2_hover.get_rect(center=menucase2_rect.center)
        screen.blit(menucase, menucase2_hover_rect)
        screen.blit(bigbox,(520,200))
        
    else:
        screen.blit(menucase, menucase2_rect)

    #menucase3_rect = menucase.get_rect(topleft=(772, 470))
    menucase3_rect = clickable_list[2]
    if menucase3_rect.collidepoint(mouse_pos):
        # Appliquer un effet de survol (par exemple, légèrement agrandir)
        menucase3_hover = pygame.transform.scale(menucase, (int(menucase.get_width()*1.1), int(menucase.get_height()*1.1)))
        menucase3_hover_rect = menucase3_hover.get_rect(center=menucase3_rect.center)
        screen.blit(menucase, menucase3_hover_rect)
        screen.blit(bigbox,(520,200))
        
    else:
        screen.blit(menucase, menucase3_rect)

    #LEFT PANEL
    # Bouton Construire
    
    #build_button_rect = build_button_img.get_rect(topleft=(753, 170))
    build_button_rect = clickable_list[3]
    if build_button_rect.collidepoint(mouse_pos):
        # Appliquer un effet de survol (par exemple, légèrement agrandir)
        build_hover = pygame.transform.scale(build_button_img, (int(build_button_img.get_width()*1.1), int(build_button_img.get_height()*1.1)))
        build_hover_rect = build_hover.get_rect(center=build_button_rect.center)
        screen.blit(build_hover, build_hover_rect)
        
    else:
        screen.blit(build_button_img, build_button_rect)
        
    
    # Bouton Vendre
    #sell_button_rect = sell_button_img.get_rect(topleft=(835, 170))
    sell_button_rect= clickable_list[4]
    if sell_button_rect.collidepoint(mouse_pos):
        # Appliquer un effet de survol
        sell_hover = pygame.transform.scale(sell_button_img, (int(sell_button_img.get_width()*1.1), int(sell_button_img.get_height()*1.1)))
        sell_hover_rect = sell_hover.get_rect(center=sell_button_rect.center)
        screen.blit(sell_hover, sell_hover_rect)
    else:
        screen.blit(sell_button_img, sell_button_rect)



    #price_label
    ulabel = font.render("100$",True,BORDER_COLOR)
    ulabel_rect = ulabel.get_rect(topleft=(140,140))
    clabel = font.render("100$",True,BORDER_COLOR)
    clabel_rect = clabel.get_rect(topleft=(50,140))
    slabel = font.render("300$",True,BORDER_COLOR)
    slabel_rect = slabel.get_rect(topleft=(50,260))
    plabel = font.render("50$",True,BORDER_COLOR)
    plabel_rect = plabel.get_rect(topleft=(50,360))
    #SELECTEUR DE BUILD
        
    
    #selecteur_rect=coffee.get_rect(topleft=(50,100))
    selecteur_rect = clickable_list[5]
    if selecteur_rect.collidepoint(mouse_pos):
        coffee_hover = pygame.transform.scale(coffee,(int(coffee.get_width()*1.1),int(coffee.get_height()*1.1)))
        coffee_hover_rect = coffee_hover.get_rect(center=selecteur_rect.center)
        
        screen.blit(coffee_hover,coffee_hover_rect)
    else:
        screen.blit(coffee,selecteur_rect)
        screen.blit(clabel,clabel_rect)
        

    #uselecteur_rect=usine_tileset.get_rect(topleft=(140,100))
    uselecteur_rect = clickable_list[6]
    if uselecteur_rect.collidepoint(mouse_pos):
        usine_hover = pygame.transform.scale(usine_tileset,(int(usine_tileset.get_width()*1.1),int(usine_tileset.get_height()*1.1)))
        usine_hover_rect = usine_hover.get_rect(center=uselecteur_rect.center)
        
        screen.blit(usine_hover,usine_hover_rect)
    else:
        screen.blit(usine_tileset,uselecteur_rect)
        screen.blit(ulabel,ulabel_rect)

    #sselecteur_rect = serre.get_rect(topleft=(50,220))
    sselecteur_rect = clickable_list[7]
    if sselecteur_rect.collidepoint(mouse_pos):
        sselecteur_hover = pygame.transform.scale(serre,(int(serre.get_width()*1.1),int(serre.get_height()*1.1)))
        sselecteur_hover_rect = sselecteur_hover.get_rect(center=sselecteur_rect.center)

        screen.blit(serre,sselecteur_hover_rect)
    else:
        screen.blit(serre,sselecteur_rect)
        screen.blit(slabel,slabel_rect)

    #rselecteur_rect = road1.get_rect(topleft=(140,220))
    rselecteur_rect = clickable_list[8]
    if rselecteur_rect.collidepoint(mouse_pos):
        rselecteur_hover = pygame.transform.scale(road1,(int(road1.get_width()*1.1),int(road1.get_height()*1.1)))
        rselecteur_hover_rect = rselecteur_hover.get_rect(center=rselecteur_rect.center)

        screen.blit(road1,rselecteur_hover_rect)
    else:
        screen.blit(road1,rselecteur_rect)

    #pselecteur_rect = pnj_icon.get_rect(topleft=(50,330))
    pselecteur_rect = clickable_list[9]
    if pselecteur_rect.collidepoint(mouse_pos):
        pselecteur_hover = pygame.transform.scale(pnj_icon,(int(pnj_icon.get_width()*1.1),int(pnj_icon.get_height()*1.1)))
        pselecteur_hover_rect = pselecteur_hover.get_rect(center=pselecteur_rect.center)

        screen.blit(pnj_icon,pselecteur_hover_rect)
    else:
        screen.blit(pnj_icon,pselecteur_rect)
        screen.blit(plabel,plabel_rect)




        
    if build_selector==1:
        #print('SELECTED')
        selected_rect=selecteur_rect
    elif build_selector==2:
        selected_rect=uselecteur_rect
    elif build_selector ==3:
        selected_rect=sselecteur_rect
    elif build_selector==4:
        selected_rect=rselecteur_rect
    elif build_selector==5:
        selected_rect =pselecteur_rect
    else:
        #selected_rect=selected_rect
        pass
    #screen.blit(coffee,(50,230))
    screen.blit(select,selected_rect)   

    
    # Afficher les informations sur l'usine survolée
    if selected_usine is not None:
        usine_info = smallfont.render(f"{selected_usine.name} ({selected_usine.position[0]}, {selected_usine.position[1]})", True, BORDER_COLOR)
        production_info = smallfont.render(f"Prod: {selected_usine.production_rate} kg/sec", True, BORDER_COLOR)
        produced = smallfont.render(f"{selected_usine.produced} produced",True,BORDER_COLOR)
        pnjlabel =smallfont.render(f"{selected_usine.pnj_number} workers",True,BORDER_COLOR)
        if selected_usine.name == "Coffee Shop":
            stocklabel =smallfont.render(f"Sold:{selected_usine.stock}kg",True,BORDER_COLOR)
        else:
            stocklabel=smallfont.render(f"Stock :{selected_usine.stock} kg",True,BORDER_COLOR)
        screen.blit(usine_info, (45, 450))
        screen.blit(production_info, (45, 470))
        screen.blit(produced,(45,490))
        screen.blit(pnjlabel,(45,530))
        screen.blit(stocklabel,(45,550))
    
    return build_button_rect, sell_button_rect, selecteur_rect,uselecteur_rect,sselecteur_rect,rselecteur_rect,pselecteur_rect


# Fonction pour détecter les clics sur les boutons
def handle_button_click(pos, build_rect, sell_rect, coffee_build,usine_build,serre_build,road_build,build_pnj,old_build_selector=1):
    global player_money, is_building,herb, is_selling,build_selector,is_upgrading
    #selector = 1
    build_selector=old_build_selector
    if build_rect.collidepoint(pos):
        
        if player_money >= 100:
            is_building = not is_building  # Activer ou désactiver le mode construction
            if is_building:
                print("Mode construction activé.")  
            else:
                print("Mode construction désactivé.")
            print("Construction réalisée! Argent dépensé.")
        else:
            print("Pas assez d'argent pour construire.")
    elif sell_rect.collidepoint(pos):
        is_selling = not is_selling
        if is_selling:
            print("Mode vente activé")
        else:
            print("Mode vente desactivé")
            
    for i in range(0,len(clickable_list)):
        print(clickable_list[i])
        print(i)
        if clickable_list[i].collidepoint(pos):
            print('test')
            if (i)>3:
                
                build_selector=(i-4)
            elif i<3:
                is_upgrading = not is_upgrading
                
#    elif coffee_build.collidepoint(pos):
  #      build_selector = 1
#    elif usine_build.collidepoint(pos):
#        build_selector=2
#    elif serre_build.collidepoint(pos):
#        build_selector=3
#    elif road_build.collidepoint(pos):
#        build_selector=4
#    elif build_pnj.collidepoint(pos):
#        build_selector=5
    

    return build_selector
        
def is_mouse_over_factory(mouse_pos, usine):
    # Convertir les coordonnées de la souris en coordonnées isométriques
    tile_x, tile_y = iso_to_tile(mouse_pos[0], mouse_pos[1], tile_width, tile_height)
    #print(tile_x == usine.position[0] and tile_y == usine.position[1])
    # Comparer la position de la souris avec la position de l'usine
    return (tile_x == usine.position[0] and tile_y == usine.position[1])


# Dimensions d'une tile (par exemple, 64x64 pixels)
TILE_SIZE = 64

# Fonction pour convertir les coordonnées de la grille en coordonnées pixels
def tile_to_pixel(tile_x, tile_y):
    return tile_x * TILE_SIZE, tile_y * TILE_SIZE

def tile_to_iso(tile_x, tile_y, tile_width, tile_height):
    iso_x = (tile_x - tile_y) * (tile_width // 2)
    iso_y = (tile_x + tile_y) * (tile_height // 2)
    return iso_x, iso_y

# Dessiner un contour autour de la tuile
def draw_tile_outline(x,y,build_selector):
    x-=0
    y-=0
    screen_x, screen_y = tile_to_iso(x, y, tile_width, tile_height)
    #screen_x, screen_y = iso_projection(x, y)
    offsetx = 0 #-215
    offsety =0 #-133
    points = [
        (screen_x+offsetx, screen_y+offsety),
        ((screen_x + tile_width // 2)+offsetx, (screen_y + tile_height // 2)+offsety),
        (screen_x+offsetx, screen_y + tile_height+offsety),
        ((screen_x - tile_width // 2)+offsetx, (screen_y + tile_height // 2)+offsety)
    ]
    #structure en transparence sous le curseur
    if is_building:
        iso_x, iso_y = tile_to_iso(x-1, y, tile_width, tile_height)
        if build_selector==2:
            structure_img=usine_tileset
        elif build_selector==1:
            structure_img=coffee
        elif build_selector==3:
            structure_img = serre
        elif build_selector==4:
            structure_img=road1
        elif build_selector==5:
            structure_img=pnj_icon
        
        
        #iso_x-=257
        #iso_y-=150
        # Afficher l'image de l'usine avec une transparence
        scaled_structure = pygame.transform.scale(structure_img, (80, 60))  # Ajuster si nécessaire
        scaled_structure.set_alpha(128)  # Rendre l'image semi-transparente
        screen.blit(scaled_structure, (iso_x, iso_y))

    if is_selling:
        iso_x,iso_y=tile_to_iso(x-1,y,tile_width,tile_height)
        sell_cursor.set_alpha(128)
        screen.blit(sell_cursor, (iso_x, iso_y))

    if is_choosing:
        iso_x,iso_y=tile_to_iso(x-1,y,tile_width,tile_height)
        structure_img=pnj_go_icon
        scaled_structure = pygame.transform.scale(structure_img, (80, 60))  # Ajuster si nécessaire
        scaled_structure.set_alpha(128)  # Rendre l'image semi-transparente
        screen.blit(scaled_structure, (iso_x, iso_y))
        
    pygame.draw.polygon(screen, (0,0,0), points, 2)  # Dessiner le contour

def interaction_pnj(pnj,amount):
    if pnj.workplace.stock>amount:
        pnj.workplace2.stock += amount
        pnj.workplace.stock-=amount

def month_update(pnj_number):
    fees = pnj_number*PNJ_SALARY
    return fees
    
        

usines_list = []
coffee_list = []
serre_list = []
road_list= []
pnj_list = []
structure_list= []
road_flip =1
#usine = Usine(production_rate=10, production_time=5, position=(1, 2))
#usine2 = Usine(production_rate=10, production_time=5, position=(3, 2))
#usine3 = Usine(production_rate=10, production_time=5, position=(5, 2))
#usine4 = Usine(production_rate=10, production_time=5, position=(7, 2))
#usines_list.append(usine)
#usines_list.append(usine2)
#usines_list.append(usine3)
#usines_list.append(usine4)




# Fonction principale du jeu
def main():
    global player_money, is_building,day_counter, is_selling,build_selector, is_choosing,is_upgrading
    global herb
    is_building = False
    is_selling=False
    is_choosing=False
    is_upgrading =False
    
    build_selector = 1
    old_build_selector = build_selector
        
     
    herb=0
    clock = pygame.time.Clock()

    # Compteur de jours
    day_counter = 1
    time_elapsed = 0
    day_duration = 2  # Une journée dure 10 secondes

    notification_manager = NotificationManager()
    
    while True:
        delta_time = clock.tick(60) / 1000 # Temps en secondes écoulées

        time_elapsed += delta_time

        if day_counter==30:
            player_money -= month_update(len(pnj_list))
            day_counter=1

        # Incrémenter le jour si suffisamment de temps s'est écoulé
        if time_elapsed >= day_duration:
            day_counter += 1
            time_elapsed = 0  # Réinitialiser le temps écoulé
            print(f"Nouveau jour: {day_counter}")
        
        # Obtenir la position actuelle de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Remettre selected_usine à None pour chaque frame
        selected_usine = None
        #print(selected_usine)
        for us in usines_list:
            # Détecter si la souris survole l'usine   
            if is_mouse_over_factory((mouse_x,mouse_y), us):
                selected_usine = us
                #print('SELECTED')
        for co in coffee_list:
            # Détecter si la souris survole l'usine   
            if is_mouse_over_factory((mouse_x,mouse_y), co):
                selected_usine = co
                #print('SELECTED')
        for se in serre_list:
            # Détecter si la souris survole l'usine   
            if is_mouse_over_factory((mouse_x,mouse_y), se):
                selected_usine = se
                #print('SELECTED')

        
        for u in usines_list:
            production = u.produire(delta_time)
            if production > 0 and u.stock>10:
                u.produced +=production
                u.stock-=production
                herb+=production
                notification_manager.add_notification(f"Une usine a produit {production} kg. kilos de herbe à joie: {herb}")

        for c in coffee_list:   
            production = c.produire(delta_time)
            if production<0 and herb >0:
                c.produced+=production
                herb+=production
                c.stock-=production
                player_money+=c.herbprice
                notification_manager.add_notification(f"Un stoned s'est prit 2 kilos !")
                
        for s in serre_list:
            production = s.produire(delta_time)
            if production>0 :
                s.stock+=production
                s.produced+=production
                #herb+=production
                
                notification_manager.add_notification(f"ça pousse !1kg ramassé dans une serre!")
        for p in pnj_list:
            delivery = p.pick_up(delta_time)
            if delivery>0:
                interaction_pnj(p,delivery)

            #p.search_destination(usines_list,serre_list)
            #print(p.destination)
            #p.deplacer(road_list)
            
            
        

        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_building:  # Si on est en mode construction   
                    # Vérifie si on clique sur une tuile
                    if event.button == 1:  # Clic gauche
                        if build_selector==2:
                        # Vérifie si la tuile est valide pour construire
                            if (tile_x, tile_y) not in [(u.position[0], u.position[1]) for u in usines_list]:
                                
                                usines_list.append(Usine(production_rate=10, production_time=3, position=(tile_x, tile_y)))
                                player_money -= 100  # Coût de construction
                                notification_manager.add_notification("Usine construite!")
                                is_building = False  # Désactiver le mode construction
                        elif build_selector==1:
                            if (tile_x, tile_y) not in [(c.position[0], c.position[1]) for c in coffee_list]:
                                
                                coffee_list.append(Coffee(production_rate=(-2), production_time=4, position=(tile_x, tile_y)))
                                player_money -= 100  # Coût de construction
                                notification_manager.add_notification("Coffee Shop construit!")
                                is_building = False  # Désactiver le mode construction
                        elif build_selector==3:
                            if (tile_x, tile_y) not in [(s.position[0], s.position[1]) for s in serre_list]:
                                serre_list.append(Serre(production_rate=1,production_time=1,position=(tile_x,tile_y)))
                                player_money-=300
                                notification_manager.add_notification("Serre construite!")
                                is_building = False
                        elif build_selector==4:
                            if (tile_x, tile_y) not in [(r.position[0], r.position[1]) for r in road_list]:
                                road_list.append(Road(position=(tile_x,tile_y),flip=1))
                                player_money-=30
                                notification_manager.add_notification("Route construite!")
                                is_building = False
                        elif build_selector==5:
                            #if (tile_x, tile_y) not in [(p.position[0], p.position[1]) for p in pnj_list]:
                            just_born_pnj= PNJ(position=(tile_x,tile_y),role=  selected_usine,production_rate=1,production_time=3)  
                            pnj_list.append(just_born_pnj)
                            selected_usine.pnj_number+=1
                            player_money-=50
                            notification_manager.add_notification("PNJ engagé!")
                            is_building = False
                            if selected_usine.name =="Serre" or selected_usine.name=="Usine":
                                is_choosing = True
                    if event.button ==2:
                        is_building=False

                elif is_selling:
                    if event.button == 1:  # Clic gauche
                        # Vérifie s'il y a une usine à la position cliquée
                        for u in usines_list:
                            if u.position == (tile_x, tile_y):
                                usines_list.remove(u)  # Supprime l'usine
                                player_money += 50  # Argent gagné pour la vente
                                notification_manager.add_notification("Usine vendue!")
                                break
                        # Vérifie s'il y a un coffee shop à la position cliquée
                        for c in coffee_list:
                            if c.position == (tile_x, tile_y):
                                coffee_list.remove(c)  # Supprime le coffee shop
                                player_money += 50  # Argent gagné pour la vente
                                notification_manager.add_notification("Coffee shop vendu!")
                                break
                        for s in serre_list:
                            if s.position == (tile_x, tile_y):
                                serre_list.remove(s)   
                                player_money += 50  
                                notification_manager.add_notification("Serre vendu!")
                                break
                        for r in road_list:
                            if r.position == (tile_x, tile_y):
                                road_list.remove(r)   
                                player_money += 10  
                                notification_manager.add_notification("Route vendu!")
                                break
                            
                        is_selling = False
                    if event.button ==2:
                        is_selling = False

                elif is_choosing:
                    if event.button ==1:
                        for u in usines_list:
                            if u.position == (tile_x, tile_y):
                                #print('test')
                                just_born_pnj.workplace2=u
                                print(u)
                                
                                break
                                
                            else:
                                print('No usine here')
                            
                        is_choosing = not is_choosing
                                
                                
                        
                else:
                    build_selector = handle_button_click(mouse_pos, build_button_rect,
                                                         sell_button_rect, selecteur_rect,uselecteur_rect,sselecteur_rect,rselecteur_rect,pselecteur_rect,old_build_selector)
                old_build_selector = build_selector                        

                    

        
        #mx,my = iso_projection(mouse_x, mouse_y)
        tile_x, tile_y = iso_to_tile(mouse_x, mouse_y, tile_width, tile_height)


 


        
        # Remplir l'écran avec la couleur de fond
        screen.fill(BACKGROUND_COLOR)
        
        # Dessiner une grille isométrique
        grid_width = 10
        grid_height = 10
        for x in range(grid_width):
            for y in range(grid_height):
                draw_tile(x, y, GRID_COLOR)  # Dessiner chaque tuile en bleu clair


        draw_usines(usines_list,(mouse_x,mouse_y))
        draw_coffee(coffee_list,(mouse_x,mouse_y))
        draw_serre(serre_list,(mouse_x,mouse_y))
        draw_road(road_list,(mouse_x,mouse_y))
        draw_pnj(pnj_list,(mouse_x,mouse_y))
        # Dessiner la tuile sous la souris
        draw_tile_outline(tile_x, tile_y,build_selector)
        # Dessiner l'interface utilisateur
        build_button_rect, sell_button_rect,selecteur_rect,uselecteur_rect,sselecteur_rect,rselecteur_rect,pselecteur_rect = draw_ui( selected_usine)
        notification_manager.draw(screen, smallerfont)
        # Mettre à jour l'écran
        notification_manager.update(delta_time)
        pygame.display.flip()
        clock.tick(60)  # Limiter à 60 FPS

if __name__ == "__main__":
    main()
    
