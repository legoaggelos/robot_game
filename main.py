# Complete your game here
import pygame
import random
class Player:
    
    def __init__(self,height, width):
        self.width=width
        self.height = height
        self.x = 0
        self.y = 300-height
        self.status = "grnd" #can be grnd(not jumping), acc(accelerating up), std(steady at max jump height) or fll(falling, going down)
        self.max_height = self.y-160
        self.up_accel = -self.max_height/4
        self.down_accel = -self.up_accel
        
    def set_status(self, status):
        if status=="acc":
            if self.status=="acc" or self.status=="grnd":
                self.status = "acc"
        elif status=="fll":
            if self.status!="grnd":
                self.status = "fll"
        
    def tick(self):
        if self.status=="acc" and self.y>self.max_height:
            self.y+=self.up_accel
            return (self.x,self.y)
        elif self.status=="acc" and self.y<=self.max_height:
            self.status="fll"
        elif self.status=="fll":
            if self.y>=300-self.height:
                self.status="grnd"
                self.y=300-self.height
                return (self.x,self.y)
            self.y+=self.down_accel
        return (self.x,self.y)
    def get_pos(self):
        return (self.x,self.y)
class Enemy:
    def __init__(self,height,width):
        self.height = height
        self.width = width
        self.y = 300 - height
        if random.randint(1,5)==3:
            self.y-=100
        self.x = 1000-width
        
    def should_remove (self):
        if self.x+self.width<0:
            return "yes"
        elif self.x<0:
            #print('soon')
            return "soon"
        print(self.x)
        return "no"
    def is_colliding(self, image1,x1,y1, image2,x2,y2):
        rect1 = image1.get_rect()
        rect1.topleft=(x1,y1)
        rect2 = image2.get_rect()
        rect2.topleft=(x2,y2)
        return rect1.colliderect(rect2)
    def get_pos(self):
        return (self.x,self.y)
    def tick(self,speed_multiplier):
        remove = self.should_remove()
        if remove=="yes":
            return False
        elif remove=="no":
            self.x-=1*speed_multiplier
            return False
        else: 
            self.x-=1*speed_multiplier
            return True
class GoogleDino:
    def __init__(self):
        pygame.init()
        self.height=300
        self.width=1000
        self.load_images()
        robot=self.images["robot"]
        enemy = self.images["monster"]
        self.player = Player(robot.get_height(),robot.get_width())
        self.window = pygame.display.set_mode((self.width, self.height))
        self.enemies = []
        self.enemies.append(Enemy(enemy.get_height(),enemy.get_width()))
        pygame.display.set_caption("Robot game")
        self.points=0
        self.max_points=0
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.has_lost = False
        self.main_loop()
        
    def load_images(self):
        self.images={}
        for name in ["robot", "monster"]:
            self.images[name]=pygame.image.load(name+".png")
    def main_loop(self):
        #keep adding executions going next level 
        while True:
            self.check_events()
            self.draw_window()
    def show_points(self, add_text=""):
        self.window.blit(self.game_font.render(f"{add_text}{self.points}/{self.max_points}", True, (255, 0, 0)),(500,0))
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    self.player.set_status("acc")
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_SPACE:
                    self.player.set_status("fll")        
                

            if event.type == pygame.QUIT:
                exit()
    def draw_window(self):
        clock = pygame.time.Clock()
        self.window.fill((254, 224, 164))
        player_pos = self.player.tick()
        enemies_pos = list(map(lambda v: v.get_pos(), self.enemies))
        self.window.blit(self.images["robot"],player_pos)
        #print(self.enemies[0].is_colliding(self.images["robot"],player_pos[0]+100,player_pos[1],self.images["monster"],player_pos[0],player_pos[1]))
        new_enemies=[]
        for i in range(len(self.enemies)):
            self.window.blit(self.images["monster"],enemies_pos[i])
            multiplier = 20
            if self.points<=2700:
                multiplier+= self.points//100
            else:
                multiplier+= 2700//100#over 47 multiplier is too fast
            remove = self.enemies[i].tick(multiplier)
            if self.enemies[i].is_colliding(self.images["monster"],enemies_pos[i][0],enemies_pos[i][1],self.images["robot"], player_pos[0],player_pos[1]):
                print("collision")
                self.points=0
                self.has_lost=True
            if remove:
                new_enemies.append(Enemy(self.images["monster"].get_height(),self.images["monster"].get_width()))
                #we dont add the removed enemy, we add a new one
            else:
                new_enemies.append(self.enemies[i])
        if len(new_enemies)==0:
            new_enemies.append(Enemy(self.images["monster"].get_height(),self.images["monster"].get_width()))
        self.enemies=new_enemies
        clock.tick(30)
        self.points+=1
        if self.points>self.max_points:
            self.max_points=self.points
        add_text=""
        if self.has_lost and self.points<75:
            add_text="You lost!  "
        
        self.show_points(add_text)
        pygame.display.flip()
GoogleDino()