import pygame, sys
import mysql.connector as sql



pygame.init()

SCREEN_WIDTH = 1128
SCREEN_HEIGHT = 634
FPS = 60
FONT = pygame.font.Font("assets\\courbd.ttf" , 20)
FONTHEADER = pygame.font.Font("assets\\courbd.ttf" , 25)
reso_modes = pygame.display.list_modes()
SCREEN_WIDTH, SCREEN_HEIGHT = reso_modes[2]


screen_caption = pygame.display.set_caption("Data Manager")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_icon = pygame.image.load("assets\\DataManager.ico")
screen_icon.set_colorkey("black")
pygame.display.set_icon(screen_icon)
clock = pygame.time.Clock()
w1img = pygame.image.load("assets\\w1.png").convert()
w2img = pygame.image.load("assets\\w2.png").convert()
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

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

def validate_headers(headers, data):

    if not data:
        return headers  # If no data, headers are fine as-is.

    # Determine the number of columns in the data
    num_columns = len(data[0])

    # If headers are missing, add placeholder headers
    while len(headers) < num_columns:
        headers.append(f"Field of inquiry ({len(headers) + 1})")

    return headers


def fetch_table_data(table_name):
      
    query = f"SELECT * FROM {table_name} "
    cursor.execute(query)
    return cursor.fetchall()

def get_table_headers(table_name):
    
    cursor.execute(f"DESCRIBE {table_name}")
    return [desc[0] for desc in cursor.fetchall()]

def calculate_column_widths(data, headers):
   
    col_widths = [len(header) for header in headers]
    for row in data:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(value)))
    return [width * 12 for width in col_widths]  # Scale width for rendering

def render_table(data, headers):
   
    screen.fill("darkblue")  

    # Calculate column widths
    col_widths = calculate_column_widths(data, headers)
    total_table_width = sum(col_widths) + 20 * (len(headers) - 1)  # Total width of the table
    total_table_height = 50 + len(data) * 30  # Height of headers + rows

 
    x_offset = (SCREEN_WIDTH - total_table_width) // 2
    y_offset = (SCREEN_HEIGHT - total_table_height) // 2


    # Render table headers
    header_y = y_offset
    for i, header in enumerate(headers):
        header_surface = FONT.render(header, True, (255, 255, 255), "black")
        screen.blit(header_surface, (x_offset, header_y))
        x_offset += col_widths[i] + 20  # Add padding between columns

    # Render table rows
    row_y = header_y + 40  
    for row in data:
        x_offset = (SCREEN_WIDTH - total_table_width) // 2
        for i, value in enumerate(row):
            row_surface = FONT.render(str(value), True, (255, 255, 255), "black")
            screen.blit(row_surface, (x_offset, row_y))
            x_offset += col_widths[i] + 20
        row_y += 30  # Space between rows


def connector_loop():
    global cursor, datab
    
    input_text = "   "
    active = False  

    while True:
        screen.fill((255, 255, 255))

        draw_text("Enter MySQL Password", "Black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3-100, FONTHEADER)
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
        
        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        draw_text("Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)

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
        screen.fill("darkblue")

        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        draw_text("Data Manager", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)

        
        b = draw_text("1. Data Modification","white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+60)
        c = draw_text("2. Search Data","white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+90)

        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():

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
        screen.fill("darkblue")

        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        draw_text("Options", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)

        a = draw_text("Wallpaper 1", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+40)
        b = draw_text("Wallpaper 2", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+80)
        c = draw_text("Wallpaper Base", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+120)
        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)

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






#CHANGE BRANCH




def ChangeData_select_database():
    global selectedData, outvar
    cursor.execute("show databases")
    data = cursor.fetchall()
    li = []
    for i in data:
        li.append(i)
    
    selectedData = None

    while True:
        
        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        a= draw_text("Select Database", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)
      
        z = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
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
            input_text = f"{outvar+1}" + " " + li[outvar][0]
            q= draw_input_text(f"{input_text}", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+(outvar*30)) 
            if mousecli:
                if q.collidepoint((mx,my)):
                    click = True           
                    if click:                
                        selectedData = li[outvar][0]
                        
                        ChangeData_select_table()

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
        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        
        click = False
        Mousecli = False

        a = draw_text("Select Table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)
        b = draw_text("# Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
         
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
            input_text = f"{j+1}" + " " + li[j][0]
            q= draw_input_text(f"{input_text}", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+(j*40))
            if Mousecli:
                if q.collidepoint((mx,my)):
                    click = True
                    if click:
                        selectedData2 = li[j][0]
                        ChangeData_Options()
        pygame.display.flip()
        clock.tick(FPS)

def ChangeData_Options():

    """
    A menu system to select between the options of Data Entry and Changing of Data

    """

    while True:


        mx, my = pygame.mouse.get_pos()
        click = False

        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        e = draw_text("Data Modification", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)
        d = draw_text("1. Data Entry", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-50)
        s = draw_text("2. Change Data", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        a = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
        t = draw_text("<-- Back","white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-90)
    

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if click:
            if t.collidepoint((mx,my)):
                ChangeData_select_database()
            if d.collidepoint((mx,my)):
                DataEntry()
            if s.collidepoint((mx,my)):
                C_Data()
            if a.collidepoint((mx, my)):
                main_menu_loop()

        pygame.display.flip()
        clock.tick(FPS)

def DataEntry():

    """
    Main loop for INSERT command in MySQL

    for entering new data in the table
    """
    
    active = False

    cursor.execute(f"DESCRIBE `{selectedData2}`")
    data = cursor.fetchall()
    
    li = [row[0] for row in data] 
    li_num = len(li)  

    ex_li = ["  "] * li_num  

    while True:
        click = False

        screen.fill("darkblue")  

     
        if w1:
            screen.blit(pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        if w2:
            screen.blit(pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        mx, my = pygame.mouse.get_pos()  

        m = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT-30)
        a = draw_text("Enter Values", "white", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 - 100, FONTHEADER)
        g = draw_text("Enter", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+200)
        t = draw_text("<-- Back", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-90)

        # Dynamically calculate the width of each input box and the gap between them
        box_width = SCREEN_WIDTH // (li_num + 1.5) - 40  
        gap = 20 
        total_width = (box_width * li_num) + (gap * (li_num - 1))  
        start_x = (SCREEN_WIDTH - total_width) // 2  

        
        for k in range(li_num):
            x_position = start_x + k * (box_width + gap)  
            draw_text(li[k], "white", screen, x_position, SCREEN_HEIGHT/3-40)
            q = draw_input_text(ex_li[k], "white", screen, x_position, SCREEN_HEIGHT / 3)
            if q.collidepoint((mx, my)): 
                active = not active
                n = k

       
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                if t.collidepoint((mx,my)):
                    ChangeData_Options()
                if m.collidepoint((mx, my)):
                    main_menu_loop()
                    
                    
                if g.collidepoint((mx,my)):
                    try:

                        for o in range(li_num):
                            if type(ex_li[o]) == int:
                                ex_li[o] = int(ex_li[o].strip())
                            else:
                                ex_li[o] = ex_li[o].strip()
                            
                        
                        placeholders = ", ".join(["%s"] * li_num)  # Create placeholders for all columns
                        query = f"INSERT INTO `{selectedData2}` VALUES ({placeholders})"
                        values = tuple(ex_li)  # Convert list to tuple for SQL execution

                       
                        cursor.execute(query, values)
                        datab.commit()  # Commit the transaction

                        draw_text("Done", "white", screen, SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 3+300)
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        ChangeData_Options()
                        
                    except sql.Error as e:
                        draw_text(f"SQL Error: {e}", "white", screen, SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 3+300)
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        DataEntry()

            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

                if active:  
                    if event.key == pygame.K_BACKSPACE:
                        p =  ex_li[n]
                        ex_li[n] = p[:-1]
                    elif event.unicode:  
                        ex_li[n] += event.unicode


        pygame.display.flip()
        clock.tick(FPS)





def C_Data():

    """
    Main loop for UPDATE command in MySQL

    primarily used for changing of already existing values
    """


    re = 3
    inp = 1
    click3 = False
    click2 = False
    click = False
    
    input_text = "  "
    dash_text = "  "
    where_text = "  "
    input_var = " "
    where_var = " "
    dash_var = " "
   
    cursor.execute(f"DESCRIBE `{selectedData2}`")
    data = cursor.fetchall()
    
    li = [row[0] for row in data] 
    li_num = len(li)  


    while True:
        

        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))


        mx,my = pygame.mouse.get_pos()


        m = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT-30)
        t = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT-90)
        draw_text("Set Conditions", "white", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 - 100, FONTHEADER)

        for i in range(li_num):
            draw_text(f"{li[i]}", "white", screen, SCREEN_WIDTH/2-3*SCREEN_WIDTH/8, 20+SCREEN_HEIGHT/3+i*(30))

        e = draw_input_text(f"{input_text}", "white", screen, SCREEN_WIDTH/2-SCREEN_WIDTH/8, SCREEN_HEIGHT/3)
        draw_text("Column to be updated", "white", screen, SCREEN_WIDTH/2-SCREEN_WIDTH/8, SCREEN_HEIGHT/3+30)

        f = draw_input_text(f"{dash_text}", "white", screen, SCREEN_WIDTH/2-SCREEN_WIDTH/8, SCREEN_HEIGHT/3+90)
        draw_text("Updated Column", "white", screen, SCREEN_WIDTH/2-SCREEN_WIDTH/8, SCREEN_HEIGHT/3+120)

        d = draw_input_text(f"{where_text}", "white", screen, SCREEN_WIDTH/2+SCREEN_WIDTH/4, SCREEN_HEIGHT/3+30)
        draw_text(" Where ", "white", screen, SCREEN_WIDTH/2+SCREEN_WIDTH/4, SCREEN_HEIGHT/3+60)

        p = draw_text("Enter", "white", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + 200)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if click:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode:  
                        input_text += event.unicode
                    inp = int(input_text.strip())

                if click2:
                    if event.key == pygame.K_BACKSPACE:
                        dash_text = dash_text[:-1]
                    elif event.unicode:  
                        dash_text += event.unicode
               
                if click3:
                    if event.key == pygame.K_BACKSPACE:
                        where_text = where_text[:-1]
                    elif event.unicode:  
                        where_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if t.collidepoint((mx,my)):
                    ChangeData_Options()
                if m.collidepoint((mx,my)):
                    main_menu_loop()
                if e.collidepoint((mx,my)):
                    click = True
                    click2 = False
                    click3 = False
                if f.collidepoint((mx,my)):
                    click2 = True
                    click = False
                    click3 = False
                if d.collidepoint((mx,my)):
                    click3 = True
                    click2 = False
                    click = False
                if p.collidepoint((mx,my)):
                    try:
                        input_var = li[inp-1]
                        dash_var = dash_text.strip()
                        where_var = where_text.strip() 
                        if len(where_var) <= re:
                            cursor.execute(f"UPDATE `{selectedData2}` SET `{input_var}` = `{dash_var}` ")
                            datab.commit()  # Commit the transaction

                            draw_text("Done", "white", screen, SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 3+300)
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            main_menu_loop()
                        else:
                            cursor.execute(f"UPDATE `{selectedData2}` SET `{input_var}` = `{dash_var}` WHERE  `{where_var}`")
                            datab.commit()  # Commit the transaction

                            draw_text("Done", "white", screen, SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 3+300)
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            ChangeData_Options()
                    except sql.Error:
                            print(sql.Error)
                            draw_text("Error", "white", screen, SCREEN_WIDTH / 2 + 300, SCREEN_HEIGHT / 3+300)
                            pygame.display.flip()
                            pygame.time.delay(5000)
                            main_menu_loop()


            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)    




#FIND BRANCH



def FindData():



    global selectedData3
    cursor.execute("SHOW DATABASES")
    data = cursor.fetchall()
    li = []
    for i in data:
        li.append(i)
    while True:
        click = False

        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        mx,my = pygame.mouse.get_pos()

        a = draw_text("Select Database", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)

        q = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2,SCREEN_HEIGHT-30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        for j in range(len(li)):
            input_text = f"{j+1}" + " " + li[j][0]
            z = draw_input_text(f"{input_text}", "white", screen,SCREEN_WIDTH/2, SCREEN_HEIGHT/3-50+(j*30))


            if click:
                if q.collidepoint((mx,my)):
                    main_menu_loop()
                if z.collidepoint((mx,my)):
                    selectedData3 = li[j][0]
                    FindData_select_databasetable()

        pygame.display.flip()
        clock.tick(FPS)


def FindData_select_databasetable():
    global selectedData3
    cursor.execute(f"USE `{selectedData3}`")
    cursor.execute("SHOW TABLES")
    data = cursor.fetchall()
    li = []
    for i in data:
        li.append(i)


    while True:

        click = False

        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        mx,my = pygame.mouse.get_pos()


        a = draw_text("Select table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)

        q = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)

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
            input_text = f"{j+1}" + " " + li[j][0]
            z = draw_input_text(f"{input_text}", "white", screen,SCREEN_WIDTH/2, SCREEN_HEIGHT/3-50+(j*30))


            if click:
                if q.collidepoint((mx,my)):
                    main_menu_loop()
                if z.collidepoint((mx,my)):
                    selectedData3 = li[j][0]
                    FindData_select_opiom()

        pygame.display.flip()
        clock.tick(FPS)


def FindData_select_opiom():
    
    """
    A menu system to select between two variants of the SELECT command in MySQL.
    """

    while True:
        click = False

        
        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        mx,my = pygame.mouse.get_pos()

        draw_text("Show Table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3-100, FONTHEADER)
        a = draw_text("1. Show Full Table", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+50 )
        b = draw_text("2. Show Specific ", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/3+100)
        q = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
        t = draw_text("<-- Back", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-90)
    

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()

        
        if click:
            if t.collidepoint((mx,my)):
                FindData()
            if a.collidepoint((mx,my)):
                ShowTable()
            if b.collidepoint((mx,my)):
                ShowTableSpecific()
            if q.collidepoint((mx,my)):
                main_menu_loop()

        pygame.display.flip()
        clock.tick(FPS)
   

def ShowTable():

    """
    First loop for SELECT command in MySQL


    to view the *full table and the values itself
    """

    headers = get_table_headers(f"{selectedData3}")
  
    

    while True:

        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        data = fetch_table_data(f"{selectedData3}")  
        render_table(data, headers)  
        m = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)
        t = draw_text("<-- Back", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-90)
    

        mx,my = pygame.mouse.get_pos()
     
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if t.collidepoint((mx,my)):
                    FindData_select_opiom()
                if m.collidepoint((mx,my)):
                    main_menu_loop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()


        
        pygame.display.flip()
        clock.tick(FPS)
   


def ShowTableSpecific():

    """
    Second loop for SELECT command in MySQL


    to view specific values in a table.
    """
   

    entr = False

    aclick = False
    bclick = False
    cclick = False

    input_text = "  "   
    where_text = "  "
    order_text = "  "

    input_text_const = "  "   
    where_text_const = "  "
    order_text_const = "  "

    cursor.execute(f"DESCRIBE `{selectedData3}`")
    data = cursor.fetchall()
    
    li = [row[0] for row in data] 
    li_num = len(li)  

    headers = []

    while True:

        screen.fill("darkblue")
        if w1 == True:
            screen.blit((pygame.transform.scale(w1img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))
        if w2 == True:
            screen.blit((pygame.transform.scale(w2img, (SCREEN_WIDTH, SCREEN_HEIGHT))), (0,0))

        m = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-30)

        mx,my = pygame.mouse.get_pos()
     
        a = draw_input_text(f"{input_text}", "white", screen, SCREEN_WIDTH/2-SCREEN_WIDTH/8, SCREEN_HEIGHT/3)
        draw_text("Column", "white", screen, SCREEN_WIDTH/2-SCREEN_WIDTH/8, SCREEN_HEIGHT/3+30)

        b = draw_input_text(f"{where_text}", "white", screen, SCREEN_WIDTH/2+SCREEN_WIDTH/8, SCREEN_HEIGHT/3)
        draw_text(" Where ", "white", screen, SCREEN_WIDTH/2+SCREEN_WIDTH/8, SCREEN_HEIGHT/3+40)

        c = draw_input_text(f"{order_text}", "white", screen, SCREEN_WIDTH/2+SCREEN_WIDTH/8, SCREEN_HEIGHT/3+120)
        draw_text(" Order by ", "white", screen, SCREEN_WIDTH/2+SCREEN_WIDTH/8, SCREEN_HEIGHT/3+160)

        e = draw_text("ENTER", "white", screen, SCREEN_WIDTH/2 , SCREEN_HEIGHT-90)

        t = draw_text("<-- Back", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-60)
    

        for i in range(li_num):
            draw_text(f"{li[i]}", "white", screen, SCREEN_WIDTH/2-3*SCREEN_WIDTH/8, SCREEN_HEIGHT/3+i*(20))

        if entr:
            try:
                headers = input_text.split(",")  
                if input_text  == input_text_const and where_text == where_text_const and order_text == order_text_const:
                    headers = [row[0] for row in data]
                    cursor.execute(f"SELECT * FROM {selectedData3} ")
                    
                elif input_text == input_text_const and where_text == where_text_const and order_text != order_text_const: 
                    cursor.execute(f"SELECT * FROM {selectedData3} ORDER BY {order_text.strip()}")
                elif input_text == input_text_const and order_text == order_text_const and where_text != where_text_const:
                    cursor.execute(f"SELECT * FROM {selectedData3} WHERE {where_text.strip()}") 

                elif input_text != input_text_const and  order_text == order_text_const and where_text == where_text_const:      
                    cursor.execute(f"SELECT {input_text} FROM {selectedData3} ")

                elif input_text != input_text_const and  order_text != order_text_const and where_text == where_text_const:      
                    cursor.execute(f"SELECT {input_text} FROM `{selectedData3}` ORDER BY {order_text.strip()}")
                elif input_text != input_text_const and  where_text != where_text_const and order_text == order_text_const:      
                    cursor.execute(f"SELECT {input_text} FROM `{selectedData3}` WHERE {where_text.strip()}") 

                data1 = cursor.fetchall()
                headers = validate_headers([headers[i].strip() for i in range(len(headers))], data1)
                render_table(data1, headers)

                o = draw_text("#Main Menu", "white", screen, SCREEN_WIDTH/2, SCREEN_HEIGHT-20)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if o.collidepoint((mx,my)):
                            main_menu_loop()

            except sql.Error:
                print(sql.Error)
                terminate()


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if aclick:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode:  
                        input_text += event.unicode
                    
                if bclick:
                    if event.key == pygame.K_BACKSPACE:
                        where_text = where_text[:-1]
                    elif event.unicode:  
                        where_text += event.unicode
               
                if cclick:
                    if event.key == pygame.K_BACKSPACE:
                        order_text = order_text[:-1]
                    elif event.unicode:  
                        order_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if t.collidepoint((mx,my)):
                    FindData_select_opiom()
                if m.collidepoint((mx,my)):
                    main_menu_loop()
                if a.collidepoint((mx,my)):
                    aclick = True
                    bclick = False
                    cclick = False
                if b.collidepoint((mx,my)):
                    aclick = False
                    bclick = True 
                    cclick = False
                if c.collidepoint((mx,my)):
                    cclick = True
                    bclick = False
                    aclick = False  
                if e.collidepoint((mx,my)):
                    entr = True

            if event.type == pygame.QUIT:
                terminate()


        
        pygame.display.flip()
        clock.tick(FPS)
     

if __name__ == "__main__":
    connector_loop()
