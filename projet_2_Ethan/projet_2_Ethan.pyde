from random import randint

class Monstre():
    def __init__(self, nom, degats, hp):
        '''
            Propriétés des monstres :
                * self.Nom : nom du monstre
                * self.Degats : degats que le monstre peut infliger au joueur pour lui faire perdre tant d'hp
                * self.Hp : points de vie du monstre
        '''
        self.Nom = nom
        self.Degats = degats
        self.Hp = hp
        
    def est_mort(self):
        """
        Verifie si le monstre n'a plus d'hp ou pas.
            Si oui, renvoie True.
            Sinon, renvoie False.
        """
        if self.Hp <= 0 :
            return True
        else : 
            return False
    
    
class Arbre():
    NomRacine = "Colline"
    
    def __init__(self, nom, monstre, cheminG = None, cheminD = None):     
        '''
            Propriétés de l'arbre :
                * self.Nom : Nom du lieu (noeud)
                * self.Monstre : Monstre habitant en ce lieu
                * self.CheminG : Le chemin de gauche (fils gauche)
                * self.CheminD : le chemin de droite (fils droite)
        '''
        self.Nom = nom
        self.Monstre = monstre
        self.CheminG = cheminG
        self.CheminD = cheminD               

    def ChercherPosition(self, lieu):
        '''
            Paramètres :
                lieu : chaîne de caractère indiquant un lieu
            Résultat :
                Renvoie le noeud de l'arbre correspondant au lieu 
                cherché, en réalisant une recherche récursive partant 
                du noeud courant.
        '''
        if lieu == self.Nom:
            return self
        
        else:
            if self.CheminG != None:
                resultat = self.CheminG.ChercherPosition(lieu)
                if resultat != None:
                    return resultat
                
            if self.CheminD != None:
                resultat = self.CheminD.ChercherPosition(lieu)
                if resultat != None:
                    return resultat
                
        return None      
    
    def ChercherParent(self, lieu):
        '''
            Paramètres :
                lieu : chaîne de caractère indiquant un lieu
            Résultat :
                Renvoie le noeud parent du noeud de l'arbre correspondant 
                au lieu cherché, en réalisant une recherche récursive partant 
                du noeud courant.
        '''
        # S'il n'y a pas de fils gauche ou droit, renvoie None
        if self.CheminG == None or self.CheminD == None:
            return None
        
        # Si le lieu recherché est le fils gauche ou droit, renvoie ce noeud
        if lieu == self.CheminG.Nom or lieu == self.CheminD.Nom:
            return self
        
        else:
            # Appel récursif de la fonction s'il y a un fils gauche
            if self.CheminG != None:
                resultat = self.CheminG.ChercherParent(lieu)
                if resultat != None:
                    return resultat
                
            # Appel récursif de la fonction s'il y a un fils gauche
            if self.CheminD != None:
                resultat = self.CheminD.ChercherParent(lieu)
                if resultat != None:
                    return resultat
        
        
        
class Joueur():
    def __init__(self):
        '''
            Propriétés du joueur :
                * self.Position : chaîne de caractères indiquant le
                lieu actuel du joueur
                
                * self.Hp : nombre de points de vie du joueur
                
                * self.Energie : nombre de points d'energie que le joueur peut utiliser pour activer ses capacités spéciales
                
                * self.Degats : degats que le joueur peut infliger au monstre et ainsi lui faire perdre autant d'hp
        '''
        self.Position = Arbre.NomRacine      
        self.Hp = 125
        self.Energie = 100
        self.Degats = 30
        
            
        
class Jeu():
    def __init__(self):
        '''
            Propriétés du jeu :
                * self.Joueur : le joueur actuel
                
                * self.Arbre : l'arbre sur lequel il évolue
                
                * self.Images : mise en cache des images utilisées dans le projet
                
                * self.Victoire : initialisation du compteur indiquant combien de monstres ont été vaincus permettant 
                d'arrêter le jeu une fois que tous les monstres sont morts
                
                * self.Num_loot : initialisation de la variable qui se verra affecter un entier aléatoire entre 1 et 3 
                et accordera au joueur une fois qu'un monstre est tué soit de l'hp, soit de l'energie, soit rien du tout
                    
                * self.Temps_initial : initialise le temps où le jeu commence 
                afin de proprement afficher le timer
                
                * self.Temps_loot : permet d'afficher le message informant le joueur 
                s'il a obtenu du "loot", à savoir de l'énergie, de l'hp ou rien du tout 
                pendant un temps limité
                
                * self.Temps_final : initialise le temps final obtenu par le joueur lorsqu'il 
                bat tous les monstres 
        '''
        self.Joueur = Joueur()     
        self.Arbre = nouvel_arbre()        
        self.Images = self.ChargerImages()
        self.Victoire = 0
        self.Num_loot = 0
        self.Temps_initial = millis()
        self.Temps_loot = millis()
        self.Temps_final = None

        
    def ChargerImages(self):  
        '''
            Résultat :
                Renvoie un dictionnaire dont les clés sont les noms des images chargées,
                et les valeurs sont les images utilisables pour l'affichage sur Processing.
                Le dictionnaire contient tous les monstres du projet, ainsi que les flèches de
                Droite, de Gauche et du Haut.
                
                Exemple d'utilisation si on affecte le résultat à d :
                    image(d['Albert'], 100, 100)
        '''    
        images = dict()
        # Dossier des images de monstre
        dossier_images = "images/monstres/"
        for nom in ["Albert", "Barnabe", "Richard", "Bernie", "Bob", "Boris", "Celia", "Dolores", "Edgar", "Edith", "Eve", "Georges", "Gina", "Hubert", "Leon", "Lucien", "Milo", "Molly", "Nestor", "Opus", "Peter", "Sam", "Zachary", "Zed"]:
            images[nom] = loadImage(dossier_images + nom + ".png")
            images[nom].resize(200, 243);
            
        # Dossier des flèches
        dossier_images = "images/fleches/"
        for nom in ["droite", "gauche", "haut"]:
            images[nom] = loadImage(dossier_images + nom + ".png")
            images[nom].resize(70, 70);
            
        return images       

    def PositionJoueur(self):
        '''
           Résultat : 
            Renvoie la position du joueur dans l'arbre.
            L'objet renvoyé est de type Arbre.
        '''
        return self.Arbre.ChercherPosition(self.Joueur.Position)
    
    def ArbreParent(self):
        '''
           Résultat : 
            Renvoie le parent de la position du joueur dans l'arbre.
            L'objet renvoyé est de type Arbre.
        '''
        return self.Arbre.ChercherParent(self.Joueur.Position)



def setup():
    global jeu
    size(1024, 768)    # Affiche le fond de l'écran
    background(255)
    jeu = Jeu()        # Crée une instance de la classe Jeu() pour la partie

    
def draw():
    global jeu
    afficher_interface(jeu)    
        

def keyReleased():
    """
    Permet au joueur d'effectuer différentes actions durant la partie, ou après celle-ci
    pour quitter le jeu :
        - Déplacement
        * Haut : Déplace le joueur au noeud parent si il y en a un
        * Gauche : Déplace le joueur au fils gauche s'il y en a un
        * Droite : Déplace le joueur au fils droit s'il y en a un
        
        - Attaques
        * Espace : Attaque basique infligeant des dégâts moyens, mais le monstre riposte avec sa propre attaque
        
        - Capacités (qui coûte chacune des points d'Energie)
        * [S] - Soin (15 Energie) : Récupère une quantité aléatoire d'Hp entre 10 et 30 Hp
        * [B] - Boost de Degats (40 Energie) : Accorde un boost aléatoire aux dégâts de l'Attaque basique (touche Espace) entre 5 et 10 dégâts
        * [L] - Lance du Chaos (10 Energie) : Attaque n'infligeant que 20 points de dégâts, mais le monstre ne peut pas riposter
        * [E] - Explosion du Chaos (30 Energie) : Inflige 50 dégâts à l'ennemi mais le joueur subit 30 dégâts
        
        - Autre
        * Echap : Lorsqu'il y a un Game Over ou que le joueur réussit à finir le jeu, appuyer sur cette touche fermera le jeu
        
    """
    global jeu        
    pos = jeu.PositionJoueur()
    
    
    if keyCode == 38 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # HAUT
        parent = jeu.ArbreParent()
        if parent is not None:
            jeu.Joueur.Position = parent.Nom  # Déplace le joueur au parent   
        
        
    if keyCode == 37 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # GAUCHE
        if pos.CheminG is not None:
            jeu.Joueur.Position = pos.CheminG.Nom  # Déplace le joueur au fils gauche
            
            
    if keyCode == 39 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # DROITE
        if pos.CheminD is not None:
            jeu.Joueur.Position = pos.CheminD.Nom  # Déplace le joueur au fils droit
            
            
    if keyCode == 32 and pos.Monstre.Hp > 0 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # ESPACE -> Attaque de base
        if jeu.Joueur.Hp > pos.Monstre.Degats:
            pos.Monstre.Hp = pos.Monstre.Hp - jeu.Joueur.Degats    # Inflige des dégâts au monstre
            jeu.Joueur.Hp = jeu.Joueur.Hp - pos.Monstre.Degats     # Dégats infligés par le monstre
            
        else:
            pos.Monstre.Hp = pos.Monstre.Hp - jeu.Joueur.Degats
            jeu.Joueur.Hp = jeu.Joueur.Hp - jeu.Joueur.Hp
        
        # Si l'attaque tue le monstre...
        if pos.Monstre.est_mort() == True: 
            jeu.Temps_loot = millis()   # Initilise l'affichage du message indiquant quelle récompense est reçu
            jeu.Num_loot = randint(1, 3)    # ...Accorde une récompense aléatoire au Joueur; il peut ne rien avoir si cette variable tombe sur 1...
            jeu.Victoire = jeu.Victoire + 1   # ...Incrémente la propriété jeu.Victoire afin de se rapprocher de la fin du jeu 
            
            if jeu.Victoire == 15:
                jeu.Temps_final = millis() - jeu.Temps_initial
                
            if jeu.Num_loot == 2:         
                jeu.Joueur.Hp = jeu.Joueur.Hp + 20 # ... 20 Hp de plus accordés au Joueur
                
            if jeu.Num_loot == 3:         
                jeu.Joueur.Energie = jeu.Joueur.Energie + 20 # ... 20 points d'Energie de plus accordés au Joueur
            
        
    if keyCode == 83 and jeu.Joueur.Energie >= 15 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # S -> Soin
        jeu.Joueur.Hp = jeu.Joueur.Hp + randint(10, 30)
        jeu.Joueur.Energie = jeu.Joueur.Energie - 15
    
    
    if keyCode == 66 and jeu.Joueur.Energie >= 40 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # B -> Boost de Dégats
        jeu.Joueur.Degats = jeu.Joueur.Degats + randint(5, 10)
        jeu.Joueur.Energie = jeu.Joueur.Energie - 40
        
        
    if keyCode == 76 and jeu.Joueur.Energie >= 10 and pos.Monstre.Hp > 0 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # L -> Lance du Chaos
        pos.Monstre.Hp = pos.Monstre.Hp - 20
        jeu.Joueur.Energie = jeu.Joueur.Energie - 10
        
        # Si l'attaque tue le monstre...
        if pos.Monstre.est_mort() == True:
            jeu.Temps_loot = millis() # ...Initilise l'affichage du message indiquant quelle récompense est reçu
            jeu.Num_loot = randint(1, 3) # ...Accorde une récompense aléatoire au Joueur; il peut ne rien avoir si cette variable tombe sur 1...
            jeu.Victoire = jeu.Victoire + 1 # ...Incrémente la propriété jeu.Victoire afin de se rapprocher de la fin du jeu 
            
            if jeu.Victoire == 15:
                jeu.Temps_final = millis() - jeu.Temps_initial
            
            if jeu.Num_loot == 2:
                jeu.Joueur.Hp = jeu.Joueur.Hp + 20   # ... 20 Hp de plus accordés au Joueur
                
            if jeu.Num_loot == 3:
                jeu.Joueur.Energie = jeu.Joueur.Energie + 20   # ... 20 points d'Energie de plus accordés au Joueur
    
    
    if keyCode == 69 and jeu.Joueur.Energie >= 20 and pos.Monstre.Hp > 0 and jeu.Joueur.Hp > 0 and jeu.Victoire != 15: # E -> Explosion du Chaos
        jeu.Joueur.Hp = jeu.Joueur.Hp - 50
        pos.Monstre.Hp = pos.Monstre.Hp - 50
        jeu.Joueur.Energie = jeu.Joueur.Energie - 30
        
        # Si l'attaque tue le monstre...
        if pos.Monstre.est_mort() == True:
            jeu.Temps_loot = millis()   # ...Initilise l'affichage du message indiquant quelle récompense est reçu
            jeu.Num_loot = randint(1, 3)   # ...Accorde une récompense aléatoire au Joueur; il peut ne rien avoir si cette variable tombe sur 1...
            jeu.Victoire = jeu.Victoire + 1   # ...Incrémente la propriété jeu.Victoire afin de se rapprocher de la fin du jeu 

            if jeu.Victoire == 15:
                jeu.Temps_final = millis() - jeu.Temps_initial
            
            if jeu.Num_loot == 2:
                jeu.Joueur.Hp = jeu.Joueur.Hp + 20   # ... 20 Hp de plus accordés au Joueur
                
            if jeu.Num_loot == 3:
                jeu.Joueur.Energie = jeu.Joueur.Energie + 20   # ... 20 points d'Energie de plus accordés au Joueur
         
        
    if keyCode == 27 and jeu.Joueur.Hp <= 0: # ECHAP pour quitter le jeu suite à un game over...
        exit()
        
    if keyCode == 27 and jeu.Victoire == 15: # ... ou suite à une victoire
        exit()

def nouvel_arbre():
    '''
        Résultat :
            Renvoie une instance de la classe Arbre
            contenant le monde dans lequel le joueur évoluera.
    '''
    Salle_De_Boss = Arbre("Salle De Boss", Monstre("Bob", 25, 100), None, None)
    Ruine = Arbre("Ruines Mysterieuses", Monstre("Eve", 10, 55), None, None)
    Buisson = Arbre("Buisson", Monstre("Hubert", 5, 60), None, None)
    Mort = Arbre("Arbre Mort" , Monstre("Gina", 10, 50), None, None)
    Foret = Arbre("Foret", Monstre("Bernie", 15, 50), Buisson, Mort)
    Grotte = Arbre("Grotte", Monstre("Boris", 15, 50), Salle_De_Boss, Ruine)
    Vallee = Arbre("Vallee", Monstre("Celia", 20, 35), Foret, Grotte)
    
    Stockage = Arbre("Salle De Stockage", Monstre("Barnabe", 5, 50), None, None)
    Machines = Arbre("Salle Des Machines", Monstre("Richard", 5, 40), None, None)
    Controle = Arbre("Salle de Controle", Monstre("Georges", 20, 30), None, None)
    Armes = Arbre("Salle d'Armement", Monstre("Celia", 15, 65), None, None)
    Laboratoire = Arbre("Laboratoire", Monstre("Dolores", 10, 70), Machines, Stockage)
    Couloir = Arbre("Couloir", Monstre("Edgar", 15, 70), Armes, Controle)
    Usine = Arbre("Usine Chimique", Monstre("Edith", 10, 40), Couloir, Laboratoire)
    
    Colline = Arbre("Colline", Monstre("Albert", 10, 60), Usine, Vallee)
    
    return Colline

    

def player_hp_bar(jeu):
    """
    Affiche la barre d'hp du joueur 
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    # Crée le visuel de la barre et du logo d'Hp
    stroke(0)
    strokeWeight(2)
    fill(255, 51, 178)
    rect(100, 515, 200, 30, 10)
    stroke(0)
    fill(0)
    circle(87, 529, 70)
    rotate(radians(45))
    stroke(255, 51, 178)
    fill(255, 51, 178)
    rect(424, 300, 31.75, 31.75, 10)
    rotate(radians(-45))
    circle(77, 526, 29.5)
    circle(98, 526, 29.5)
    
    fill(0)
    textSize(25)
    text("HP", 71, 592)
    
    # Limite le nombre minimum de vie du joueur à 0 Hp
    if jeu.Joueur.Hp <= 0:
        jeu.Joueur.Hp = 0
    
    # Limite le nombre maximum de vie du joueur à 100 Hp
    if jeu.Joueur.Hp >= 150:
        jeu.Joueur.Hp = 150
    
    # Affiche le nombre d'Hp du joueur
    text(jeu.Joueur.Hp, 130, 540)

def player_energie_bar(jeu):
    """
    Affiche la barre d'energie du joueur
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    # Crée le visuel de la barre et du logo d'Energie
    stroke(0)
    strokeWeight(2)
    fill(51, 252, 255)
    rect(100, 635, 200, 30, 10)
    stroke(0)
    fill(0)
    circle(87, 650, 70)
    fill(51, 252, 255)
    triangle(87, 672, 67, 637, 107, 637)
    
    fill(0)
    textSize(25)
    text("Energie", 45, 713)
    
    # Limite le nombre minimum d'Energie du joueur à 0 Energie
    if jeu.Joueur.Energie <= 0:
        jeu.Joueur.Energie = 0
        
    # Limite le nombre maximum d'Energie du joueur à 100 Energie
    if jeu.Joueur.Energie >= 100:
        jeu.Joueur.Energie = 100
    
    text(jeu.Joueur.Energie, 130, 660)
    
def mob_hp_bar(jeu):
    """
    Affiche la barre d'hp du monstre.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    pos = jeu.PositionJoueur()
    pos = jeu.PositionJoueur()
    if pos.Monstre.est_mort() == False:
        if pos.Monstre:
            # Crée le visuel de la barre et du logo d'Hp
            stroke(0)
            strokeWeight(2)
            fill(255, 0, 0)
            rect(412, 400, 200, 30, 10)
            stroke(0)
            fill(0)
            circle(412, 415, 70)
            fill(255, 0, 0)
            circle(412, 415, 30)
            
            # Affiche le nombre d'Hp du monstre
            fill(0)
            textSize(25)
            text(pos.Monstre.Hp, 455 ,425)
 
def afficher_timer(jeu):
    """
    Affiche le chronomètre.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    # Affiche le logo de chronomètre et la section dans laquelle se trouve le timer
    stroke(255, 178, 51)
    fill(255, 178, 51)
    rect(25, 25, 265, 75, 10)
    stroke(255, 233, 51)
    fill(255, 233, 51)
    strokeWeight(8)
    fill(0)
    rect(20, 20, 250, 65, 10)
    strokeWeight(3)
    fill(255, 233, 51)
    rect(45, 30, 20, 20, 5)
    fill(0)
    circle(55, 55, 40)
    fill(255, 233, 51)
    circle(55, 56, 7)
    rect(53, 55, 2, -12, 10)
    rect(53, 55, 11, 2, 10)
    
    # Gère l'affichage du timer de sorte à ce qu'il soit comme celui d'un chronomètre (minutes:secondes:millisecondes)
    t = millis() - jeu.Temps_initial
    t_secondes = t / 1000 % 60
    t_minutes = t / 1000 / 60
    t_millisecondes = t / 10 % 100
    fill(255, 233, 51)
    textSize(35)
    text("0" + str(t_minutes) + ":" + str(t_secondes) + ":" + str(t_millisecondes), 98, 65)
    
        
    
def afficher_competences():
    """
    Affiche la liste de toutes les compétences auxquelles le joueur a accés
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    # Affiche la section contenant les compétences
    stroke(10, 29, 110)
    strokeWeight(6)
    fill(255)
    rect(360, 500, 610, 175, 10)
    
    # Affiche les différentes compétences
    fill(0)
    textSize(20)
    text("[ESPACE] Attaque basique (30 dgts avec riposte)", 370, 530)
    text(" - 0 Energie", 837, 530)
    
    text("[<, >, ^] Deplacement", 370, 555)
    text(" - 0 Energie", 837, 555)
    
    text("[S] Soin (+ 10~30 hp)", 370, 580)
    text(" - 15 Energie", 837, 580)
    
    text("[B] Boost de Degats (+ 5~10 dgts)", 370, 605)
    text(" - 40 Energie", 837, 605)
    
    text("[L] Lance du Chaos (20 dgts sans riposte)", 370, 630)
    text(" - 10 Energie", 837, 630)
    
    text("[E] Explosion du Chaos (50 dgts pour tous)", 370, 655)
    text(" - 30 Energie", 837, 655)
    
    
def afficher_lieu_actuel(jeu):
    """
    Affiche le lieu où le joueur se trouve actuellement dans l'arbre
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    pos = jeu.PositionJoueur()
    
    stroke(10, 29, 110)
    strokeWeight(3)
    fill(255)
    rect(700, 75, 300, 75, 10)
    fill(0)
    textSize(26)
    text(pos.Nom, 725, 125) 
    textSize(25)
    text("Lieu actuel :", 772, 55) 
    
def afficher_fleches(jeu):
    """
    Vérifie si le joueur se trouve dans un noeud possédant un parent et des fils gauche et droite
    Si oui, affiche la flèche pointant vers ce noeud parent/fils.
    Sinon, n'affiche rien.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    pos = jeu.PositionJoueur()
    textSize(27)
    
    if jeu.Arbre.ChercherParent(pos.Nom) != None:
        image(jeu.Images['haut'], 480, 65) # Affiche les flèches
        text(jeu.Arbre.ChercherParent(pos.Nom).Nom, 440, 50) # Affiche le nom du noeud pointé par la flèche
        
    if pos.CheminG != None:
        image(jeu.Images['gauche'], 230, 300) # Affiche les flèches
        text(pos.CheminG.Nom, 140, 400) # Affiche le nom du noeud pointé par la flèche
        
    if pos.CheminD != None:
        image(jeu.Images['droite'], 700, 300) # Affiche les flèches
        text(pos.CheminD.Nom, 730, 400) # Affiche le nom du noeud pointé par la flèche
    
    
def afficher_monstre(jeu):
    """
    Vérifie si un monstre n'est pas mort dans le noeud où le 
    joueur se trouve actuellement.
    S'il est bien vivant, affiche le monstre existant dans ce noeud-là.
    Sinon, n'affiche rien.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    pos = jeu.PositionJoueur()
    if pos.Monstre.est_mort() == False:
        if pos.Monstre:
            monstre = pos.Monstre
            image(jeu.Images.get(monstre.Nom, jeu.Images[jeu.Arbre.Monstre.Nom]), 412, 135)
   
    
        
def afficher_game_over(jeu):
    """
    Si le joueur n'a plus de vie, affiche l'écran de Game Over
    permettant au joueur de quitter le jeu afin de réessayer.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    if jeu.Joueur.Hp <= 0:
        background(0)
        textSize(50)
        stroke(230, 23, 23)
        fill(0)
        rect(356, 225, 302, 125, 10)
        fill(230, 23, 23)
        text("GAME OVER", 363, 300)
        textSize(20)
        text("Appuyer sur Echap pour quitter", 355, 400)
        
        
     

def afficher_instructions(jeu):
    """
    Affiche le but du jeu à la racine de l'arbre permettant
    au joueur de vite savoir comment finir le jeu.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    pos = jeu.PositionJoueur()
    
    if jeu.Arbre.ChercherParent(pos.Nom) == None and jeu.Victoire != 15: # Affiche le but du jeu à la racine de l'arbre
        stroke(0)
        fill(0)
        rect(345, 55, 320, 55, 10)
        textSize(22)
        fill(93, 250, 33)
        text("Detruisez tous les monstres", 358, 80)
        text("le plus vite possible !", 388, 100)
        
 
        
            
def afficher_loot(jeu):
    """
    Vérifie si un monstre est mort et que le joueur ne l'est pas.
    Si ces conditions sont remplies, vérifie ensuite quelle récompense le joueur
    reçoit affiche le message correspondant.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    pos = jeu.PositionJoueur()
    if pos.Monstre.est_mort() == True and jeu.Joueur.Hp > 0 and jeu.Victoire != 15:
        t_affiche = millis() - jeu.Temps_loot  # Permet d'afficher l'écran d'information de la récompense obtenu pendnat un temps limité
        
        # Gère l'affichage si on n'obtient rien...
        if jeu.Num_loot == 1:
            if t_affiche < 2000:
                stroke(0)
                fill(0)
                rect(420, 230, 150, 50, 10)
                fill(255)
                textSize(22)
                text("Rien...", 461, 262)
        
        # ... Si on obtient de l'extra Hp...
        if jeu.Num_loot == 2:
            if t_affiche < 2000:
                stroke(0)
                fill(0)
                rect(420, 230, 150, 50, 10)
                fill(255, 51, 178)
                textSize(22)
                text("+ 20 HP !", 450, 262)
        
        # ... Ou si on obtient de l'extra Energie    
        if jeu.Num_loot == 3:
            if t_affiche < 2000:
                stroke(0)
                fill(0)
                rect(420, 230, 175, 50, 10)
                fill(51, 252, 255)
                textSize(22)
                text("+ 20 Energie !", 435, 262)

def afficher_victoire(jeu):
    """
    Vérifie si le joueur a réussi à détruire tous les monstres présents
    sur l'arbre.
    Si c'est le cas, affiche l'écran de victoire avec le temps final.
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    if jeu.Victoire == 15:
        background(255)
        
        # Permet l'affichage du temps comme sur un chrononmètre
        t = jeu.Temps_final
        t_secondes_finales = t / 1000 % 60
        t_minutes_finales = t / 1000 / 60
        t_millisecondes_finales = t / 10 % 100
        
         
        # Affiche les ailes derrière l'anneau
        stroke(150, 150, 150)
        fill(206, 206, 206) 
        triangle(400, 55, 200, 55, 400, 150)
        triangle(600, 55, 800, 55, 600, 150)
        
        stroke(170, 170, 170)
        fill(239, 239, 239)
        triangle(425, 110, 250, 110, 425, 195)
        triangle(575, 110, 750, 110, 575, 195)
        
        # Affiche l'anneau
        strokeWeight(12)
        stroke(255, 235, 0)
        fill(254, 254, 226)
        circle(500, 150, 270)
        
        # Affiche le timer avec le temps final
        fill(0)
        stroke(93, 250, 33)
        rect(400, 120, 200, 70, 10) 
        fill(93, 250, 33)
        textSize(35)
        text("0" + str(t_minutes_finales) + ":" + str(t_secondes_finales) + ":" + str(t_millisecondes_finales), 425, 170)
        fill(0)
        textSize(25)
        text("Temps final", 426, 100)
        
        
        
        
        
def afficher_rang(jeu):
    """
    Vérifie si le joueur a fini le jeu en détruisant tous les monstres.
    Si oui, vérifie, le temps final obtenu par le joueur et affiche en conséquence le
    rang correspondantà la vitesse à laquelle le joueur a fini le jeu.
    Plus vite le joueur finit le jeu, plus haut est le rang obtenu (D pour le rang le plus bas, puis C, B, A et enfin S),
    et plus dithyrambique est la remarque. 
    Paramètre:
        jeu: instance de la classe Jeu()
    """
    if jeu.Victoire == 15:
        strokeWeight(5)
        stroke(27, 8, 90)
        fill(255)
        rect(75, 300, 874, 400, 10)
        
        # Affiche le rang et les commentaires si on finit le jeu en-dessous de 1:30...
        if jeu.Temps_final <= 90000:
            stroke(216, 207, 13)
            fill(255)
            strokeWeight(6)
            rect(457, 400, 80, 80, 7)
            fill(216, 207, 13)
            textSize(24)
            text("Vous avez cree le jeu, ou quoi ?!", 315, 600) 
            text("Rang", 468, 390)
             
            textSize(60)
            text("S", 480, 463)
            
            textSize(40)
            text("ABSOLUMENT FANTASTIQUE !!!", 225, 540)
            textSize(18)
            fill(45, 54, 152)
            text("Appuyer sur Echap pour quitter", 360, 650)
            
        # ... Si on le finit en-dessous de 2:00...
        elif jeu.Temps_final <= 120000:
            stroke(186, 198, 198)
            fill(255)
            strokeWeight(6)
            rect(457, 400, 80, 80, 7)
            fill(186, 198, 198)
            textSize(24)
            text("Vous maitrisez presque parfaitement le jeu, encore un effort !", 160, 600) 
            text("Rang", 468, 390) 
            
            textSize(60)
            text("A", 480, 463)
            
            textSize(40)
            text("GENIAL !!!", 410, 540)
            textSize(18)
            fill(45, 54, 152)
            text("Appuyer sur Echap pour quitter", 360, 650)
            
        # ... Si on le finit en-dessous de 2:30...
        elif jeu.Temps_final <= 150000:
            stroke(97, 78, 26)
            fill(255)
            strokeWeight(6)
            rect(457, 400, 80, 80, 7)
            fill(97, 78, 26)
            textSize(24)
            text("Pas mal du tout, mais vous pouvez faire mieux !", 220, 600) 
            text("Rang", 468, 390) 
            
            textSize(60)
            text("B", 480, 463)
            
            textSize(40)
            text("SUPER !!", 430, 540)
            textSize(18)
            fill(45, 54, 152)
            text("Appuyer sur Echap pour quitter", 360, 650)
            
        # ... Si on le finit en-dessous de 3:00...  
        elif jeu.Temps_final <= 180000:
            stroke(166, 132, 173)
            fill(255)
            strokeWeight(6)
            rect(457, 400, 80, 80, 7)
            fill(166, 132, 173)
            textSize(24)
            text("C'est un bon debut, n'abandonnez pas !", 290, 600) 
            text("Rang", 468, 390) 
            
            textSize(60)
            text("C", 480, 463)
            
            textSize(40)
            text("OK !", 460, 540)
            textSize(18)
            fill(45, 54, 152)
            text("Appuyer sur Echap pour quitter", 360, 650)
        
        # ... Ou si on le finit en plus de 3:00...
        elif jeu.Temps_final > 180000:
            stroke(204, 85, 0)
            fill(255)
            strokeWeight(6)
            rect(457, 400, 80, 80, 7)
            fill(204, 85, 0)
            textSize(24)
            text("Allez, on croit en vous, vous pouvez y arriver !", 250, 600) 
            text("Rang", 468, 390) 
            
            textSize(60)
            text("D", 480, 463)
            
            textSize(40)
            text("REESAYEZ !", 400, 540)
            textSize(18)
            fill(45, 54, 152)
            text("Appuyer sur Echap pour quitter", 360, 650)
        
        
        
def afficher_interface(jeu):    
    """
    Permet d'afficher tout ce qui sera visible par le joueur durant une partie
    Paramètre:
        jeu: instance de la classe Jeu()
    """  
    # Fond
    background(255)
    
    # Barre de vie du joueur
    player_hp_bar(jeu)
    
    # Barre d'énergie spéciale du joueur
    player_energie_bar(jeu)
    
    # Affiche le monstre du lieu correspondant
    afficher_monstre(jeu)
    
    # Barre de vie des monstres
    mob_hp_bar(jeu)
    
    # Affiche le Timer
    afficher_timer(jeu)
    
    # Affiche les skills
    afficher_competences()
    
    # Affiche le titre du jeu
    afficher_lieu_actuel(jeu)
    
    # Afficher les flèches SI on peut se déplacer dans la direction indiquée par les flèches
    afficher_fleches(jeu)
    
    # Affiche l'écran de victoire avec le temps final
    afficher_victoire(jeu)
    
    # Affiche le rang obtenu par le joueur
    afficher_rang(jeu)
    
    # Affiche l'écran de game over lorsque le joueur n'a plus d'hp
    afficher_game_over(jeu)
    
    # Affiche le but du jeu à la racine de l'arbre
    afficher_instructions(jeu)
    
    # Affiche le message nous informant si nous recevons du 'loot' ou pas, et si oui, quel type de loot
    afficher_loot(jeu)
