import pygame,sys,random,math

#Distance Formula to check collisions
def collide(x1,y1,x2,y2,d):
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
    if distance<d:
        return True
    else:
        return False
    
#Background stars
class Star:
    def __init__(self,width,height):
        self.radius = random.randint(0,3)
        self.color = random.choice(["white"]*75+["blue","red","lightBlue","orange","yellow","green","purple","gold"])
        self.pos_x = random.randint(0,width)
        self.pos_y = random.randint(0,height)
        self.decrease = True
        
    def show(self,screen):
        t=random.randint(0,100)
        if t==1 :
            if self.decrease and self.radius > 2:
                self.radius -= 1
                self.decrease = False
            else:
                self.radius += 1
                self.decrease = True                
        pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),self.radius)

#Initialization and vars
pygame.init()
clock=pygame.time.Clock()
score=0
high=0
gamespeed=35
enemy_speeds=[2,9,2,2,3,1.5,1.5,1.5,2]
enemy_healths=[2,2,2,2,2,5,4,4,12]
enemy_scores=[10,10,10,10,10,20,20,20,20]


#Background music
pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(loops=-1)
boom = pygame.mixer.Sound("explosion.mp3")
tpsound = pygame.mixer.Sound("tpsound.mp3")

#Display
width=650
height=750
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Wars ")
icon=pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)
star_list=[Star(width,height) for _ in range(200)]


#Loading images
player=pygame.image.load("sp1.png")
playermask=pygame.mask.from_surface(player)
player.set_colorkey("black")
player.convert_alpha()
enemy_images=[]
enemy_masks=[]
for i in range(2,11):
    x=pygame.image.load("sp"+str(i)+".png")
    enemy_images.append(x)
    enemy_masks.append(pygame.mask.from_surface(x))
for i in enemy_images:
    i.set_colorkey("black")
    i.convert_alpha()
bulletimages=[]
for i in range(1,8):
    x=pygame.image.load("bl"+str(i)+".png")
    x.set_colorkey("black")
    x.convert_alpha()
    bulletimages.append(x)
mbulletmask=pygame.mask.from_surface(bulletimages[0])
healthbarimgs=[]
for i in range(5,0,-1):
    x=pygame.image.load("health"+str(i)+".png")
    x.set_colorkey("black")
    x.convert_alpha()
    healthbarimgs.append(x)
boostsimgs=[]
for i in range(1,4):
    x=pygame.image.load("boost"+str(i)+".png")
    x.set_colorkey("black")
    x.convert_alpha()
    boostsimgs.append(x)

#creating recs
player_rect=player.get_rect()
player_rect.center=(width/2,height-70)

move=True
Game=False
while True:
    for event in pygame.event.get():
        #Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Action management
        if Game:            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gameover:
                move = not move
            if move:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    dx = 10
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    dx = -10
                if event.type == pygame.KEYUP and ( event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT ):
                    dx = 0
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    pos=bulletimages[0].get_rect()
                    pos.center=player_rect.center
                    pos.y=player_rect.y-10
                    playerbullets.append(pos)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    move=True
                    Game=False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if score>int(high):
                    file=open("Highscore.txt",'w')
                    file.write(str(score))
                    file.close()
                Game=True
                gameover=False
                shield=False
                score=0
                dx=0
                time=0
                enemy_id=1
                playerhealth=4
                playerbullets=[]
                boosts=[]
                enemydata=[]
                enemybullets=[]
                
    #Background setup and stars movement
    screen.fill("Black")
    for s in star_list:
        s.show(screen)
        if move:
            s.pos_y += 0.5
            if s.pos_y > height :
                s.pos_y = 0
                s.pos_x = random.randint(0,width)
    
    if Game:
        #playeracters bullets
        for bullet in playerbullets:
            screen.blit(bulletimages[0],bullet)
            if move:
                bullet.y -= 5
        
        if move:
            #enemy creation
            if score<=100:
                creationvar=20
                gamespeed=35
            elif 100<score<=400:
                gamespeed=36
                creationvar=18
            elif 400<score:
                creationvar=16
                gamespeed=35+(score/400)
                
            if time%creationvar==0:
                score+=2
                enemy_num=random.choice([1,4]*7+[0,2,3]*3+[5,6,7,8])
                rec=enemy_images[enemy_num].get_rect()
                rec.bottom=0        
                rec.left=random.randint(0,width-(rec.right-rec.left))
                enemydata.append([enemy_num,rec,enemy_healths[enemy_num],enemy_id])
                enemy_id+=1
            
            #boost creation
            if time%300==0 and time!=0 and len(boosts)<1 and not shield:
                num=random.choice([0,0,0,1,1,2])
                rect=boostsimgs[num].get_rect()
                rect.left=random.randint(0,width-(rect.right-rect.left))
                rect.bottom=height-30
                if not rect.colliderect(player_rect):
                    boosts.append([boostsimgs[num],rect,num])

            #Enemy bullet creation
            for enemy in enemydata:
                if enemy[1].top > height:
                    enemydata.remove(enemy)
                    break
                if enemy[0]==0:
                    if time%40==0:
                        pos=bulletimages[1].get_rect()
                        pos.center=enemy[1].center
                        pos.y=enemy[1].y+25
                        enemybullets.append([bulletimages[1],pos,enemy[0],enemy[3]])
                if enemy[0]==2:
                    if time%40==0:
                        pos=bulletimages[2].get_rect()
                        pos.center=enemy[1].center
                        pos.x-=30
                        pos.y=enemy[1].y+25
                        enemybullets.append([bulletimages[2],pos,enemy[0],enemy[3]])
                        pos=bulletimages[2].get_rect()
                        pos.center=enemy[1].center
                        pos.x+=30
                        pos.y=enemy[1].y+25
                        enemybullets.append([bulletimages[2],pos,enemy[0],enemy[3]])
                if enemy[0]==3:
                    if time%50==0:
                        pos=bulletimages[3].get_rect()
                        pos.center=enemy[1].center
                        pos.x-=1
                        pos.y=enemy[1].y+60
                        enemybullets.append([bulletimages[3],pos,enemy[0],enemy[3]])
                if enemy[0]==5:
                    if time%10==0:
                        pos=bulletimages[6].get_rect()
                        pos.center=enemy[1].center
                        pos.y=enemy[1].y+80
                        enemybullets.append([bulletimages[6],pos,enemy[0],enemy[3]])
                if enemy[0]==6:
                    if time%40==0:
                        pos=bulletimages[5].get_rect()
                        pos.center=enemy[1].center
                        pos.x+=1
                        pos.y=enemy[1].y+40
                        enemybullets.append([bulletimages[5],pos,enemy[0],enemy[3]])
                if enemy[0]==7:
                    if time%40==0:
                        pos=bulletimages[4].get_rect()
                        pos.center=enemy[1].center
                        pos.x+=1
                        pos.y=enemy[1].y+40
                        enemybullets.append([bulletimages[4],pos,enemy[0],enemy[3]])
                    
        for bullet in enemybullets:
            screen.blit(bullet[0],bullet[1])
            if move:
                if bullet[2]==2:
                    bullet[1].y += 5
                else:
                    bullet[1].y += 4
                        
        for bullet in enemybullets:
            if bullet[1].top>height:
                enemybullets.remove(bullet)

        #enemy control
        if move:
            if time%25==0:
                dufo=random.choice([-3,0,3])
            if time%20==0:
                dghost=random.choice([-1,0,1])
            if time%50==0:
                for data in enemydata:
                    if data[0]==7 and data[1].bottom in range(100,height-250):
                        prv=data[1].left
                        data[1].left=random.randint(0,width-(data[1].right-data[1].left))
                        for enemy in enemydata:
                            if data[1].colliderect(enemy[1]) and data[3]!=enemy[3]:
                                data[1].left=prv
                        for bl in enemybullets:
                            if data[1].colliderect(bl[1]) and data[3]!=bl[3]:
                                data[1].left=prv
                        else:
                            pygame.mixer.Sound.play(tpsound)
        try:
            for data in enemydata:
                screen.blit(enemy_images[data[0]],data[1])
                if move:
                    data[1].y += enemy_speeds[data[0]]
                    if data[0]==4:
                        if data[1].right<width and data[1].left>0:
                            data[1].x += dufo
                    if data[0]==3:
                        if data[1].right<width and data[1].left>0:
                            data[1].x += dghost
        except:
            pass
                
        #Collision Course    
        try:
            #Enemy-Enemy collides
            for i in range(len(enemydata)):
                for j in range(i+1,len(enemydata)):
                    if enemydata[i][1].colliderect(enemydata[j][1]):
                        pygame.mixer.Sound.play(boom)
                        enemydata.pop(j)
                        
            for enemy in enemydata:
                #Enemy-Player collision
                if collide(player_rect.center[0],player_rect.center[1],enemy[1].center[0],enemy[1].center[1],80) and enemy[1].bottom>player_rect.top+40:                
                    pygame.mixer.Sound.play(boom)
                    enemydata.remove(enemy)
                    if not shield:
                        playerhealth-=1
                        if playerhealth<=0:
                            playerhealth=0
                            move=False
                            gameover=True
                    
                #enemy bullet collides enemy
                for bullet in enemybullets:
                    if bullet[1].colliderect(enemy[1]) and bullet[3]!=enemy[3]:
                        pygame.mixer.Sound.play(boom)
                        enemybullets.remove(bullet)
                        enemy[2]-=1
                        if enemy[2] <= 0:
                            enemydata.remove(enemy)
                            
                #playeracter bullet collides enemy            
                for bullet in playerbullets:
                    if mbulletmask.overlap(enemy_masks[enemy[0]],(bullet.right-enemy[1].right,bullet.top-enemy[1].top)):
                        pygame.mixer.Sound.play(boom)
                        playerbullets.remove(bullet)
                        enemy[2]-=1
                        if enemy[2] <= 0:
                            enemydata.remove(enemy)
                            score+=enemy_scores[enemy[0]]
                    if bullet.bottom < 0:
                        playerbullets.remove(bullet)
                        
                    #Bullet-Bullet collides
                    for bull in enemybullets:
                        if bull[1].colliderect(bullet):
                            enemybullets.remove(bull)
                            playerbullets.remove(bullet)
                            
                #enemy boost collision
                for boost in boosts:
                    if enemy[1].colliderect(boost[1]):
                        boosts.remove(boost)
                            
            for bullet in enemybullets:
                if bullet[1].colliderect(player_rect) and bullet[1].bottom>player_rect.top+40:
                    pygame.mixer.Sound.play(boom)
                    enemybullets.remove(bullet)
                    if not shield:
                        playerhealth-=1
                        if playerhealth<=0:
                            playerhealth=0
                            move=False
                            gameover=True

        except:
            pass
        
        #playeracter movement and gameover text
        if move:
            player_rect.x += dx
        else:
            if gameover:
                font = pygame.font.Font('textfont.ttf',80)
                GOtext= font.render("GAME\nOVER",True,"RED","Black")
                GOrect=GOtext.get_rect()
                GOrect.center=(width/2,height/2-60)
                screen.blit(GOtext,GOrect)
                font = pygame.font.Font('textfont.ttf',40)
                entertext= font.render("PRESS ENTER",True,"white","Black")
                enterrect=entertext.get_rect()
                enterrect.center=(width/2,height/2 + 150)
                screen.blit(entertext,enterrect)
                high=0
                file=open("Highscore.txt",'r')
                high=file.read()
                try:
                    x=int(high)
                except:
                    high=00000
                if score>int(high):
                    htext="NEW HIGHSCORE:"+str(score)
                    file.close()
                    file=open("Highscore.txt",'w')
                    file.write(str(score))
                    file.close()
                else:
                    htext="HIGHSCORE:"+high
                    file.close()
                font = pygame.font.Font('textfont.ttf',40)
                highscoretext= font.render(htext,True,"white","Black")
                hrect=highscoretext.get_rect()
                hrect.center=(width/2,height/2 + 80)
                screen.blit(highscoretext,hrect)
            
        if player_rect.right > width:
            player_rect.right = width
        if player_rect.left < 0 :
            player_rect.left = 0
        
        #Healthbar
        Health=healthbarimgs[playerhealth]
        Healthrect=Health.get_rect()
        Healthrect.center=player_rect.center
        Healthrect.y = player_rect.y + 95
        screen.blit(Health,Healthrect)
        
        #Scoreboard
        sc=str(score)
        while len(sc)<5:
            sc="0"+sc
        font = pygame.font.Font('textfont.ttf',30)
        scoretext= font.render(sc,True,"white","Black")
        scorerect=scoretext.get_rect()
        scorerect.top=20
        scorerect.right=width - 20
        screen.blit(scoretext,scorerect)
        
        #boosts blit
        for i in boosts:
            screen.blit(i[0],i[1])
            if player_rect.colliderect(i[1]):
                if i[2]==0:
                    if playerhealth<4:
                        playerhealth+=1
                if i[2]==2:
                    enemydata=[]
                    enemybullets=[]
                    score+=100
                    pygame.mixer.Sound.play(boom)
                    pygame.mixer.Sound.play(boom)
                    pygame.mixer.Sound.play(boom)
                    pygame.mixer.Sound.play(boom)
                if i[2]==1:
                    shield=True
                    stime=time
                boosts.remove(i)
        
        #Shield
        if shield:
            cen=player_rect.center
            cen=list(cen)
            cen[1]+=17
            if time-stime<=350:
                pygame.draw.circle(screen,"white",tuple(cen),67,4)
            else:
                pygame.draw.circle(screen,"red",tuple(cen),67,4)
            if time-stime>=400:
                stime=0
                shield=False
                
        #Updation
        screen.blit(player,player_rect)
        pygame.display.flip()
        time+=1
        clock.tick(gamespeed)
    else:
        #text font
        font = pygame.font.Font('textfont.ttf',100)
        sptext= font.render(" SPACE ",True,"White","Black")
        sprect=sptext.get_rect()
        sprect.center=(width/2,height/2 - 230)
        screen.blit(sptext,sprect)
        
        font = pygame.font.Font('textfont.ttf',80)
        wrtext= font.render(" WARS ",True,"orange","Black")
        wrrect=wrtext.get_rect()
        wrrect.center=(width/2,height/2 - 130)
        screen.blit(wrtext,wrrect)
        
        logo=pygame.image.load("logo.png")
        logo_rect=logo.get_rect()
        logo_rect.center=(width/2,height/2 + 40)
        screen.blit(logo,logo_rect)
        
        font = pygame.font.Font('textfont.ttf',50)
        entertext= font.render("PRESS ENTER",True,"lightgreen","Black")
        enterrect=entertext.get_rect()
        enterrect.center=(width/2+10,height/2 + 215)
        screen.blit(entertext,enterrect)
    
        playtext= font.render("TO PLAY !",True,"White","Black")
        playrect=playtext.get_rect()
        playrect.center=(width/2+10,height/2 + 300)
        screen.blit(playtext,playrect)
        
        clock.tick(100)
        pygame.display.flip()


