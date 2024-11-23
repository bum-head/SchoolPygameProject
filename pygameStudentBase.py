import pygame, sys
import mysql.connector as sql
from tabulate import tabulate as tbl


pygame.init()

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
FPS = 60
FONT = pygame.font.Font("assets\\DeterminationMonoWebRegular-Z5oq.ttf" , 20)


screen_caption = pygame.display.set_caption("Data Manager")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
w1img = pygame.image.load("assets\\w1.png").convert()
w2img = pygame.image.load("assets\\w2.png").convert()

w1 = False
w2 = False

def terminate():
    pygame.quit()
    sys.exit()

def draw_text(text, color, surface, x, y,font = FONT  ):
    textObj = font.render(text, 0, color)
    textRect = textObj.get_rect()
    textRect.center = (x, y)
    surface.blit(textObj, textRect)
    return textRect

def draw_input_text(text, color, surface, x, y,font = FONT  ):
    textObj = font.render(text, 0, color, (50,50,50))
    textRect = textObj.get_rect()
    textRect.center = (x, y)
    surface.blit(textObj, textRect)
    return textRect


def connector_loop():
    global cursor, datab
    
    input_text = "   "
    active = False  

    while True:
        screen.fill((255, 255, 255))

        draw_text("Enter MySQL Password", "Black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        a = draw_input_text(input_text, "white", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + 50)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx, my)):
                    active = not active 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

                if active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode:  
                        input_text += event.unicode

                    if event.key == pygame.K_RETURN:  
                        try:
                            
                            datab = sql.connect(
                                host="localhost",
                                user="root",
                                password=input_text.strip()  
                            )
                            draw_text("Connection Successful", "green", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + 100)
                            pygame.display.flip()  
                            pygame.time.delay(2000)  
                            cursor = datab.cursor()
                            main_menu_loop()
                        except sql.Error:
                            draw_text(f"`{sql.Error}`", "red", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 - 20)
                            pygame.display.flip()
                            pygame.time.delay(10000)
                            terminate()
        pygame.display.flip()
        clock.tick(FPS)





def main_menu_loop():
    while True:
        
        screen.fill((10,10,10))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        draw_text("Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)

        a = draw_text("1. Data Manager", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+40)
        b = draw_text("2. Options", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+80)
        z = draw_text("# Quit", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+160)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx,my)):
                    dataManager()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b.collidepoint((mx,my)):
                    Options()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if z.collidepoint((mx,my)):
                    terminate()                   
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        
        pygame.display.flip()
        clock.tick(FPS)            


def dataManager():
    while True:
        screen.fill((60,150,60))

        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        draw_text("Data Manager", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-60)

        a = draw_text("1. Enter New Data","white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+30)
        b = draw_text("2. Change Previous Data","white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+60)
        c = draw_text("3. Find From Existing","white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+90)

        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+180)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx,my)):
                    NewData()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b.collidepoint((mx,my)):
                    ChangeData_select_database()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if c.collidepoint((mx,my)):
                    FindData()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if z.collidepoint((mx,my)):
                    main_menu_loop()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        
        pygame.display.flip()
        clock.tick(FPS)            


def Options():
    global w1, w2
    while True:
        screen.fill((0,0,0))

        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        draw_text("Options", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)

        a = draw_text("Wallpaper 1", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+40)
        b = draw_text("Wallpaper 2", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+80)
        c = draw_text("Wallpaper Base", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+120)
        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+300)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx,my)):
                    w1 = True
                    w2 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b.collidepoint((mx,my)):
                    w2 = True
                    w1 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if c.collidepoint((mx,my)):
                    w2 = False
                    w1 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if z.collidepoint((mx,my)):
                    main_menu_loop()                   
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

        pygame.display.flip()
        clock.tick(FPS)  


def NewData():
    while True:
        screen.fill((60,150,60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        draw_text("Data Entry", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-40)

        a = draw_text("1. Create Database", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        b = draw_text("2. Create Table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+40)

        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+160)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx,my)):
                    CreateDatabase()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b.collidepoint((mx,my)):
                    CreateTable() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if z.collidepoint((mx, my)):
                    main_menu_loop()                 
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

        pygame.display.flip()
        clock.tick(FPS)  

def CreateDatabase():
    active = False
    input_text = "   "
    while True:

        screen.fill((60,150,60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        draw_text("Create Database", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-80)
        a = draw_input_text(input_text, "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+80)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx,my)):
                    active = not active

            if event.type == pygame.MOUSEBUTTONDOWN:
                if z.collidepoint((mx,my)):
                    main_menu_loop()  
            
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode:
                        input_text += event.unicode

                    if event.key == pygame.K_RETURN:
                        try:
                            cursor.execute(f"CREATE DATABASE `{input_text.strip()}`")
                            draw_text("Database Succesfully Created!", "White", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100)
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            main_menu_loop()
                        except sql.Error:
                            draw_text("Error", "white", screen , SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100)
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            main_menu_loop()

        pygame.display.flip()
        clock.tick(FPS)        

def CreateTable():
    input_text = "   "
    active = False
    while True:

        screen.fill((60,150,60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))


        draw_text("Create Table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100)
        z = draw_text("# Main Menu", "white",screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+150)
        a = draw_input_text(input_text, "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx, my)):
                    active = not active
                if z.collidepoint((mx, my)):
                    main_menu_loop()            
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode:
                        input_text += event.unicode
                
                if event.key == pygame.K_RETURN:
                    try:
                        cursor.execute(f"create table `{input_text.strip()}` ")
                        draw_text("Operation Succesful!", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+100)
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        main_menu_loop()
                    except sql.Error:
                        draw_text("Please Check your Input!!", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+100)
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        main_menu_loop()

        pygame.display.flip()
        clock.tick(FPS)

def ChangeData_select_database():
    global selectedData, outvar
    cursor.execute("show databases")
    data = cursor.fetchall()
    li = []
    for i in data:
        li.append(i)
    
    selectedData = None

    while True:
        
        screen.fill((60,150,60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        a= draw_text("Select Database", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-70)
        #b = draw_text("")
        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+250)
        mousecli = False
        click = False
 
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if z.collidepoint((mx,my)):
                    main_menu_loop()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousecli = True
        for outvar in range(len(li)):
            input_text = f"`{outvar}`" + li[outvar][0]
            q= draw_input_text(f"`{input_text}`", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+(outvar*30)) 
            if mousecli:
                if q.collidepoint((mx,my)):
                    click = True           
                    if click:                
                        selectedData = li[outvar][0]
                        
                        ChangeData_mid_screen()

        pygame.display.flip()
        clock.tick(FPS)

def ChangeData_mid_screen():

    while True:
        screen.fill((60,150,60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        a = draw_text("1.Change Table Values", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        c = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+150)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if a.collidepoint((mx,my)):
                    ChangeData_select_table()
                if c.collidepoint((mx,my)):
                    main_menu_loop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)



def ChangeData_select_table():
    global selectedData2, j
    li = []
    cursor.execute(f"USE `{selectedData.strip()}`")
    cursor.execute("SHOW TABLES")
    data = cursor.fetchall()
    for i in data:
        li.append(i)

    selectedData2 = None

    while True:
        screen.fill((60, 150, 60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        
        click = False
        Mousecli = False

        a = draw_text("Select Table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100)
        b = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+200)
         
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                Mousecli = True
                if b.collidepoint((mx,my)):
                    main_menu_loop()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        for j in range(len(li)):
            input_text = f"`{j}`" + li[j][0]
            q= draw_input_text(f"`{input_text.strip()}`", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+(j*40))
            if Mousecli:
                if q.collidepoint((mx,my)):
                    click = True
                    if click:
                        selectedData2 = li[j][0]
                        ChangeData_table()
        pygame.display.flip()
        clock.tick(FPS)

def ChangeData_table():
    while True:


        mx, my = pygame.mouse.get_pos()
        click = False

        screen.fill((60, 150, 60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        a = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+250)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if click:
            if a.collidepoint((mx, my)):
                main_menu_loop()

        pygame.display.flip()
        clock.tick(FPS)

def FindData():
    global selectedData3
    cursor.execute("SHOW DATABASES")
    data = cursor.fetchall()
    li = []
    for i in data:
        li.append(i)
    while True:
        click = False

        screen.fill((60, 150, 60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        mx,my = pygame.mouse.get_pos()

        a = draw_text("Select Database", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-150)

        q = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        for j in range(len(li)):
            input_text = f"`{j}`" + li[j][0]
            z = draw_input_text(f"`{input_text}`", "white", screen,SCREEN_WIDTH/2, SCREEN_HEIGHT/3-50+(j*30))


            if click:
                if q.collidepoint((mx,my)):
                    main_menu_loop()
                if z.collidepoint((mx,my)):
                    selectedData3 = li[j][0]
                    FindData_select_database()

        pygame.display.flip()
        clock.tick(FPS)


def FindData_select_database():
    global selectedData3
    cursor.execute(f"USE `{selectedData3}`")
    cursor.execute("SHOW TABLES")
    data = cursor.fetchall()
    li = []
    for i in data:
        li.append(i)


    while True:

        click = False

        screen.fill((60, 150, 60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        mx,my = pygame.mouse.get_pos()


        a = draw_text("Select table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-150)

        q = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+250)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()


            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                if q.collidepoint((mx,my)):
                    main_menu_loop()
        for j in range(len(li)):
            input_text = f"`{j}`" + li[j][0]
            z = draw_input_text(f"`{input_text}`", "white", screen,SCREEN_WIDTH/2, SCREEN_HEIGHT/3-50+(j*30))


            if click:
                if q.collidepoint((mx,my)):
                    main_menu_loop()
                if z.collidepoint((mx,my)):
                    selectedData3 = li[j][0]
                    FindData_select_table()

        pygame.display.flip()
        clock.tick(FPS)


def FindData_select_table():
    while True:

        screen.fill((60, 150, 60))
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        mx,my = pygame.mouse.get_pos()
     

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)
   
if __name__ == "__main__":
    connector_loop()