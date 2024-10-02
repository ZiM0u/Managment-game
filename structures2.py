class Building:
    def __init__(self, production_rate, production_time, position, name):
        self.production_rate = production_rate  # Quantité produite par cycle
        self.production_time = production_time  # Temps nécessaire pour un cycle de production
        self.time_since_last_production = 0     # Temps écoulé depuis la dernière production
        self.position = position
        self.produced = 0
        self.name = name  # Nom de la structure
        self.pnj_number = 0  # Nombre de PNJ associés
        self.stock = 0

    def produire(self, delta_time):
        # Mise à jour du temps écoulé
        self.time_since_last_production += delta_time
        
        # Si le temps écoulé dépasse ou atteint le temps de production, produire
        if self.time_since_last_production >= self.production_time:
            self.time_since_last_production -= self.production_time  # Réinitialiser le compteur
            
            return self.production_rate  # Retourner la quantité produite
        
        return 0  # Si ce n'est pas encore le moment de produire

    def pnj_trigger(self):
        if pnj_number>0:
            pass



class Usine(Building):
    def __init__(self, production_rate, production_time, position):
        super().__init__(production_rate, production_time, position, "Usine")


class Coffee(Building):
    def __init__(self, production_rate, production_time, position):
        super().__init__(production_rate, production_time, position, "Coffee Shop")
        self.herbprice = 2 #gain when sell 2kg


class Serre(Building):
    def __init__(self, production_rate, production_time, position):
        super().__init__(production_rate, production_time, position, "Serre")
        


class PNJ:
    def __init__(self, position,role,production_rate,production_time):
        self.production_rate = production_rate  # Quantité produite par cycle
        self.production_time = production_time  # Temps nécessaire pour un cycle de production
        self.time_since_last_production = 0     # Temps écoulé depuis la dernière production
        self.position = position  # Position (x, y) sur la grille
        self.destination = None
        self.animation_state = 0
        self.bag =0
        self.workplace =role
        self.workplace2=None
        self.name = "Roger"
        if role.name=="Serre":
            self.role ="Delivery"
            
        

    def set_destination(self, destination):
        self.destination = destination


    def search_destination(self, usine_list,serre_list):
        if self.destination==None:
             
            if self.bag>0:
                
                if self.workplace2.stock<10:
                    self.destination = self.workplace2
                        
            elif self.bag ==0:
                
                #print(self.workplace.stock)
                if self.workplace.stock>=1:
                    print('test')
                    self.destination=self.workplace 
            else:
                pass
        #print('testsss')
                

    def deplacer(self, routes):
        
        if self.destination:
            print(self.destination)
            
            # Calculer la direction vers la destination
            direction = (self.destination.position[0] - self.position[0], self.destination.position[1] - self.position[1])
            
            # Normaliser la direction pour un mouvement constant
            if direction[0] != 0:
                step_x = 1 if direction[0] > 0 else -1
            else:
                step_x = 0
            
            if direction[1] != 0:
                step_y = 1 if direction[1] > 0 else -1
            else:
                step_y = 0

            # Nouvelle position potentielle
            new_position = (self.position[0] + step_x, self.position[1] + step_y)
            
            # Vérifier si la nouvelle position est sur une route
            for r in routes:
                if new_position == r.position:
                        self.position = new_position  # Déplacer le PNJ

            # Vérifier si le PNJ a atteint sa destination
            if (self.position == self.destination.position):
                print("GOTOSERRE")  
                if self.bag==0:
                    pass
                    #self.destination = self.workplace
                elif self.bag >0:
                    pass
                    #self.destination =self.workplace2
                self.destination = None  # Réinitialiser la destination
        else:
            if self.bag==0:
                self.destination=self.workplace
                
            #print('Undefinied destination')
                
    def bag_action(self, building):
        if building.name == "Usine":
            
            if self.bag>0:
                building.stock+=self.bag
                self.bag=0
                self.destination=self.workplace
                print('Delivery left a kg!')
                
        elif building.name=="Serre":
            if self.bag==0:
                if building!=None:
                    if building.stock>0:
                        building.stock-=1
                        self.bag+=1
                        print('Delivery got a kg')
                        
                self.destination=self.workplace2
                
    def pick_up(self,delta_time):
        # Mise à jour du temps écoulé
        self.time_since_last_production += delta_time
        
        # Si le temps écoulé dépasse ou atteint le temps de production, produire
        if self.time_since_last_production >= self.production_time:
            self.time_since_last_production -= self.production_time  # Réinitialiser le compteur
            
            return self.production_rate  # Retourner la quantité produite
        
        return 0  # Si ce n'est pas encore le moment de produire
                
        

class Road:
    def __init__(self, position, flip):
        self.position = position  # (x, y) coordinates on the map
        self.flip = flip
