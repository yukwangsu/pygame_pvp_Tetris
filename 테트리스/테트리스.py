import pygame
import random
import copy
###############################################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 1900    # 가로 크기
screen_height = 1000   # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# FPS
clock = pygame.time.Clock()

# 화면 타이틀 설정
pygame.display.set_caption("Tetris")  # 게임 이름

###############################################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

background = pygame.image.load(".\\bg.png") 

p_1_background = pygame.image.load(".\\pg.png") 
p_2_background = pygame.image.load(".\\pg.png") 

next_ground = pygame.image.load(".\\next_block_ground.png") 

game_start_pic = pygame.image.load(".\\game_start.png") 

win_pic = pygame.image.load(".\\win.png") 
lose_pic = pygame.image.load(".\\lose.png") 

p_1_background_size = p_1_background.get_rect().size
p_2_background_size = p_2_background.get_rect().size

p_1_background_width = p_1_background_size[0]
p_1_background_height = p_1_background_size[1]
p_2_background_width = p_2_background_size[0]
p_2_background_height = p_2_background_size[1]

p_1_background_x_pos = 200
p_1_background_y_pos = 100
p_2_background_x_pos = 1150
p_2_background_y_pos = 100

block_1 = pygame.image.load(".\\block_1.png") 
block_2 = pygame.image.load(".\\block_2.png") 
block_3 = pygame.image.load(".\\block_3.png") 
block_4 = pygame.image.load(".\\block_4.png") 
block_5 = pygame.image.load(".\\block_5.png") 
block_6 = pygame.image.load(".\\block_6.png") 
block_7 = pygame.image.load(".\\block_7.png") 
block_8 = pygame.image.load(".\\block_8.png") 

block_size = 43

p_1_now_block_x_pos = p_1_background_x_pos + block_size * 4
p_1_now_block_y_pos = p_1_background_y_pos - block_size
p_2_now_block_x_pos = p_2_background_x_pos + block_size * 4
p_2_now_block_y_pos = p_2_background_y_pos - block_size

p_1_new = True
p_2_new = True

p_1_ro = 1
p_2_ro = 1

p_1_ro_change = False
p_2_ro_change = False

p_1_left = True
p_1_right = True
p_1_down = True
p_1_down_2 = True
p_1_rot = True
p_2_left = True
p_2_right = True
p_2_down = True
p_2_down_2 = True
p_2_rot = True

p_1_first_land = True
p_2_first_land = True

p_1_land_fin = False
p_2_land_fin = False

p_1_attack = 0
p_2_attack = 0

p_1_skill_erase = False
p_1_skill_erase_stack = 1
p_2_skill_erase = False
p_2_skill_erase_stack = 1

p_1_block_list = [random.randint(1,7)]
p_2_block_list = [random.randint(1,7)]

player_1_win = False
player_2_win = False

game_start = False

p_1_space = [[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]] for _ in range(22)]
p_2_space = [[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]] for _ in range(22)]

check_time = 0

runing = True 
while runing:
    dt = clock.tick(144) 

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            runing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                for i in range(0,4):
                    if p_1_space_loc[i][1] == 0:
                        p_1_left = False
                        break
                for i in range(0,4):
                    if p_1_space_loc[i][1]-1 >= 0 and p_1_space[p_1_space_loc[i][0]][p_1_space_loc[i][1]-1][0] == 1:
                        p_1_left = False
                        break
                if p_1_left == True:
                    p_1_now_block_x_pos -= block_size                    
                    for i in range(0,4):
                        p_1_space_loc[i][1] -= 1
                p_1_left = True

            if event.key == pygame.K_d:
                for i in range(0,4):
                    if p_1_space_loc[i][1] == 9:
                        p_1_right = False
                        break
                for i in range(0,4):
                    if p_1_space_loc[i][1]+1 <= 9 and p_1_space[p_1_space_loc[i][0]][p_1_space_loc[i][1]+1][0] == 1:
                        p_1_right = False
                        break
                if p_1_right == True:
                    p_1_now_block_x_pos += block_size
                    for i in range(0,4):
                        p_1_space_loc[i][1] += 1
                p_1_right = True

            if event.key == pygame.K_s and p_1_space_loc[2][0] >= 2:
                for i in range(0,4):
                    if p_1_space_loc[i][0] == 21:
                        p_1_down = False
                        break
                for i in range(0,4):
                    if p_1_space_loc[i][0]+1 <= 21 and p_1_space[p_1_space_loc[i][0]+1][p_1_space_loc[i][1]][0] == 1 and p_1_space_loc[2][0] > 1:
                        p_1_down = False
                        p_1_land_fin = True
                        break
                for i in range(0,4):
                    if p_1_space_loc[i][0]+2 <= 21 and p_1_space[p_1_space_loc[i][0]+2][p_1_space_loc[i][1]][0] == 1 and p_1_space_loc[2][0] > 1:
                        p_1_down_2 = False
                        break 
                if p_1_down_2 == True and p_1_down == True:
                    p_1_now_block_y_pos += block_size*2
                    for i in range(0,4):
                        p_1_space_loc[i][0] += 2
                elif p_1_down == True:
                    p_1_now_block_y_pos += block_size
                    for i in range(0,4):
                        p_1_space_loc[i][0] += 1
                p_1_down = True
                p_1_down_2 = True

            if event.key == pygame.K_w:
                p_1_ro_change = True
                p_1_pre_ro_num = p_1_ro
                p_1_ro += 1
                if p_1_ro > 4:
                    p_1_ro = 1

            #밑칸 지우기 스킬
            if event.key == pygame.K_r and p_1_skill_erase_stack > 0:
                p_1_skill_erase = True
                p_1_skill_erase_stack -= 1

            if event.key == pygame.K_LEFT:
                for i in range(0,4):
                    if p_2_space_loc[i][1] == 0:
                        p_2_left = False
                        break
                for i in range(0,4):
                    if p_2_space_loc[i][1]-1 >= 0 and p_2_space[p_2_space_loc[i][0]][p_2_space_loc[i][1]-1][0] == 1:
                        p_2_left = False
                        break
                if p_2_left == True:
                    p_2_now_block_x_pos -= block_size                    
                    for i in range(0,4):
                        p_2_space_loc[i][1] -= 1
                p_2_left = True

            if event.key == pygame.K_RIGHT:
                for i in range(0,4):
                    if p_2_space_loc[i][1] == 9:
                        p_2_right = False
                        break
                for i in range(0,4):
                    if p_2_space_loc[i][1]+1 <= 9 and p_2_space[p_2_space_loc[i][0]][p_2_space_loc[i][1]+1][0] == 1:
                        p_2_right = False
                        break
                if p_2_right == True:
                    p_2_now_block_x_pos += block_size
                    for i in range(0,4):
                        p_2_space_loc[i][1] += 1
                p_2_right = True

            if event.key == pygame.K_DOWN:
                for i in range(0,4):
                    if p_2_space_loc[i][0] == 21:
                        p_2_down = False
                        break
                for i in range(0,4):
                    if p_2_space_loc[i][0]+1 <= 21 and p_2_space[p_2_space_loc[i][0]+1][p_2_space_loc[i][1]][0] == 1 and p_2_space_loc[2][0] > 1:
                        p_2_down = False
                        p_2_land_fin = True
                        break
                for i in range(0,4):
                    if p_2_space_loc[i][0]+2 <= 21 and p_2_space[p_2_space_loc[i][0]+2][p_2_space_loc[i][1]][0] == 1 and p_2_space_loc[2][0] > 1:
                        p_2_down_2 = False
                        break 
                if p_2_down_2 == True and p_2_down == True:
                    p_2_now_block_y_pos += block_size*2
                    for i in range(0,4):
                        p_2_space_loc[i][0] += 2
                elif p_2_down == True:
                    p_2_now_block_y_pos += block_size
                    for i in range(0,4):
                        p_2_space_loc[i][0] += 1
                p_2_down = True
                p_2_down_2 = True

            if event.key == pygame.K_UP:
                p_2_ro_change = True
                p_2_pre_ro_num = p_2_ro
                p_2_ro += 1
                if p_2_ro > 4:
                    p_2_ro = 1

            #밑칸 지우기 스킬
            if event.key == pygame.K_RSHIFT and p_2_skill_erase_stack > 0:
                p_2_skill_erase = True
                p_2_skill_erase_stack -= 1

            #게임 시작 버튼
            if event.key == pygame.K_SPACE:
                game_start = True

    # 3. 게임 캐릭터 위치 정의
    
    if p_1_new == True:
        p_1_ro = 1
        while True:
            p_1_next_block_num = random.randint(1,7)
            if p_1_next_block_num != p_1_block_list[0]:
                p_1_block_list.append(p_1_next_block_num)
                break
        p_1_now_block_num = p_1_block_list[0]
        del p_1_block_list[0]

        if p_1_now_block_num == 1:  
            p_1_now_block = block_1
            p_1_space_loc = [[1,3],[1,4],[1,5],[1,6]]
        elif p_1_now_block_num == 2:  
            p_1_now_block = block_2
            p_1_space_loc = [[0,4],[0,5],[1,4],[1,5]]
        elif p_1_now_block_num == 3:  
            p_1_now_block = block_3
            p_1_space_loc = [[0,3],[1,3],[1,4],[1,5]]
        elif p_1_now_block_num == 4:  
            p_1_now_block = block_4
            p_1_space_loc = [[0,5],[1,3],[1,4],[1,5]]
        elif p_1_now_block_num == 5:  
            p_1_now_block = block_5
            p_1_space_loc = [[0,3],[0,4],[1,4],[1,5]]
        elif p_1_now_block_num == 6:  
            p_1_now_block = block_6
            p_1_space_loc = [[0,4],[0,5],[1,3],[1,4]]
        elif p_1_now_block_num == 7:  
            p_1_now_block = block_7
            p_1_space_loc = [[0,4],[1,3],[1,4],[1,5]]
        p_1_new = False

    if p_2_new == True:
        p_2_ro = 1
        while True:
            p_2_next_block_num = random.randint(1,7)
            if p_2_next_block_num != p_2_block_list[0]:
                p_2_block_list.append(p_2_next_block_num)
                break
        p_2_now_block_num = p_2_block_list[0]
        del p_2_block_list[0]

        if p_2_now_block_num == 1:  
            p_2_now_block = block_1
            p_2_space_loc = [[1,3],[1,4],[1,5],[1,6]]
        elif p_2_now_block_num == 2:  
            p_2_now_block = block_2
            p_2_space_loc = [[0,4],[0,5],[1,4],[1,5]]
        elif p_2_now_block_num == 3:  
            p_2_now_block = block_3
            p_2_space_loc = [[0,3],[1,3],[1,4],[1,5]]
        elif p_2_now_block_num == 4:  
            p_2_now_block = block_4
            p_2_space_loc = [[0,5],[1,3],[1,4],[1,5]]
        elif p_2_now_block_num == 5:  
            p_2_now_block = block_5
            p_2_space_loc = [[0,3],[0,4],[1,4],[1,5]]
        elif p_2_now_block_num == 6:  
            p_2_now_block = block_6
            p_2_space_loc = [[0,4],[0,5],[1,3],[1,4]]
        elif p_2_now_block_num == 7:  
            p_2_now_block = block_7
            p_2_space_loc = [[0,4],[1,3],[1,4],[1,5]]
        p_2_new = False


    if p_1_ro_change == True:
        p_1_pre_ro_loc = copy.deepcopy(p_1_space_loc)
        p_1_pre_ro_x_pos = p_1_now_block_x_pos

        if p_1_now_block_num == 1:
            if p_1_ro == 2 or p_1_ro == 4:
                p_1_space_loc[0][1] += 1
                p_1_space_loc[0][0] -= 1
                p_1_space_loc[2][1] -= 1
                p_1_space_loc[2][0] += 1
                p_1_space_loc[3][1] -= 2
                p_1_space_loc[3][0] += 2
            elif p_1_ro == 1 or p_1_ro == 3:
                p_1_space_loc[0][1] -= 1
                p_1_space_loc[0][0] += 1
                p_1_space_loc[2][1] += 1
                p_1_space_loc[2][0] -= 1
                p_1_space_loc[3][1] += 2
                p_1_space_loc[3][0] -= 2

        elif p_1_now_block_num == 3:
            if p_1_ro == 2:
                p_1_space_loc[0][1] += 2
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] += 1
            elif p_1_ro == 3:
                p_1_space_loc[0][0] += 2
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 4:
                p_1_space_loc[0][1] -= 2
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 1:
                p_1_space_loc[0][0] -= 2
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] += 1

        elif p_1_now_block_num == 4:
            if p_1_ro == 2:
                p_1_space_loc[0][0] += 2
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] += 1
            elif p_1_ro == 3:
                p_1_space_loc[0][1] -= 2
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 4:
                p_1_space_loc[0][0] -= 2
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 1:
                p_1_space_loc[0][1] += 2
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] += 1

        elif p_1_now_block_num == 5:
            if p_1_ro == 2:
                p_1_space_loc[0][1] += 2
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] += 1
            elif p_1_ro == 3:
                p_1_space_loc[0][0] += 2
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 4:
                p_1_space_loc[0][1] -= 2
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 1:
                p_1_space_loc[0][0] -= 2
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] += 1

        elif p_1_now_block_num == 6:
            if p_1_ro == 2:
                p_1_space_loc[0][1] += 1
                p_1_space_loc[0][0] += 1
                p_1_space_loc[1][0] += 2
                p_1_space_loc[2][1] += 1
                p_1_space_loc[2][0] -= 1
            elif p_1_ro == 3:
                p_1_space_loc[0][1] -= 1
                p_1_space_loc[0][0] += 1
                p_1_space_loc[1][1] -= 2
                p_1_space_loc[2][1] += 1
                p_1_space_loc[2][0] += 1
            elif p_1_ro == 4:
                p_1_space_loc[0][1] -= 1
                p_1_space_loc[0][0] -= 1
                p_1_space_loc[1][0] -= 2
                p_1_space_loc[2][1] -= 1
                p_1_space_loc[2][0] += 1
            elif p_1_ro == 1:
                p_1_space_loc[0][1] += 1
                p_1_space_loc[0][0] -= 1
                p_1_space_loc[1][1] += 2
                p_1_space_loc[2][1] -= 1
                p_1_space_loc[2][0] -= 1

        elif p_1_now_block_num == 7:
            if p_1_ro == 2:
                p_1_space_loc[0][1] += 1
                p_1_space_loc[0][0] += 1
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] += 1
            elif p_1_ro == 3:
                p_1_space_loc[0][1] -= 1
                p_1_space_loc[0][0] += 1
                p_1_space_loc[1][1] += 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] -= 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 4:
                p_1_space_loc[0][1] -= 1
                p_1_space_loc[0][0] -= 1
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] += 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] -= 1
            elif p_1_ro == 1:
                p_1_space_loc[0][1] += 1
                p_1_space_loc[0][0] -= 1
                p_1_space_loc[1][1] -= 1
                p_1_space_loc[1][0] -= 1
                p_1_space_loc[3][1] += 1
                p_1_space_loc[3][0] += 1
        
        p_1_ro_change = False

        for i in range(0,4):
            if p_1_space_loc[i][1] == -2:
                for j in range(0,4):
                    p_1_space_loc[j][1] += 2
                p_1_now_block_x_pos += block_size*2
            elif p_1_space_loc[i][1] == 11:
                for j in range(0,4):
                    p_1_space_loc[j][1] -= 2  
                p_1_now_block_x_pos -= block_size*2
            elif p_1_space_loc[i][1] == -1:
                for j in range(0,4):
                    p_1_space_loc[j][1] += 1
                p_1_now_block_x_pos += block_size
            elif p_1_space_loc[i][1] == 10:
                for j in range(0,4):
                    p_1_space_loc[j][1] -= 1  
                p_1_now_block_x_pos -= block_size
        
        for i in range(0,4):
            if p_1_space_loc[i][0] > 21 or p_1_space[p_1_space_loc[i][0]][p_1_space_loc[i][1]][0] == 1:
                p_1_space_loc = p_1_pre_ro_loc
                p_1_ro = p_1_pre_ro_num
                p_1_now_block_x_pos = p_1_pre_ro_x_pos
                break


    if p_2_ro_change == True:
        p_2_pre_ro_loc = copy.deepcopy(p_2_space_loc)
        p_2_pre_ro_x_pos = p_2_now_block_x_pos

        if p_2_now_block_num == 1:
            if p_2_ro == 2 or p_2_ro == 4:
                p_2_space_loc[0][1] += 1
                p_2_space_loc[0][0] -= 1
                p_2_space_loc[2][1] -= 1
                p_2_space_loc[2][0] += 1
                p_2_space_loc[3][1] -= 2
                p_2_space_loc[3][0] += 2
            elif p_2_ro == 1 or p_2_ro == 3:
                p_2_space_loc[0][1] -= 1
                p_2_space_loc[0][0] += 1
                p_2_space_loc[2][1] += 1
                p_2_space_loc[2][0] -= 1
                p_2_space_loc[3][1] += 2
                p_2_space_loc[3][0] -= 2

        elif p_2_now_block_num == 3:
            if p_2_ro == 2:
                p_2_space_loc[0][1] += 2
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] += 1
            elif p_2_ro == 3:
                p_2_space_loc[0][0] += 2
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 4:
                p_2_space_loc[0][1] -= 2
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 1:
                p_2_space_loc[0][0] -= 2
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] += 1

        elif p_2_now_block_num == 4:
            if p_2_ro == 2:
                p_2_space_loc[0][0] += 2
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] += 1
            elif p_2_ro == 3:
                p_2_space_loc[0][1] -= 2
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 4:
                p_2_space_loc[0][0] -= 2
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 1:
                p_2_space_loc[0][1] += 2
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] += 1

        elif p_2_now_block_num == 5:
            if p_2_ro == 2:
                p_2_space_loc[0][1] += 2
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] += 1
            elif p_2_ro == 3:
                p_2_space_loc[0][0] += 2
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 4:
                p_2_space_loc[0][1] -= 2
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 1:
                p_2_space_loc[0][0] -= 2
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] += 1

        elif p_2_now_block_num == 6:
            if p_2_ro == 2:
                p_2_space_loc[0][1] += 1
                p_2_space_loc[0][0] += 1
                p_2_space_loc[1][0] += 2
                p_2_space_loc[2][1] += 1
                p_2_space_loc[2][0] -= 1
            elif p_2_ro == 3:
                p_2_space_loc[0][1] -= 1
                p_2_space_loc[0][0] += 1
                p_2_space_loc[1][1] -= 2
                p_2_space_loc[2][1] += 1
                p_2_space_loc[2][0] += 1
            elif p_2_ro == 4:
                p_2_space_loc[0][1] -= 1
                p_2_space_loc[0][0] -= 1
                p_2_space_loc[1][0] -= 2
                p_2_space_loc[2][1] -= 1
                p_2_space_loc[2][0] += 1
            elif p_2_ro == 1:
                p_2_space_loc[0][1] += 1
                p_2_space_loc[0][0] -= 1
                p_2_space_loc[1][1] += 2
                p_2_space_loc[2][1] -= 1
                p_2_space_loc[2][0] -= 1

        elif p_2_now_block_num == 7:
            if p_2_ro == 2:
                p_2_space_loc[0][1] += 1
                p_2_space_loc[0][0] += 1
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] += 1
            elif p_2_ro == 3:
                p_2_space_loc[0][1] -= 1
                p_2_space_loc[0][0] += 1
                p_2_space_loc[1][1] += 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] -= 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 4:
                p_2_space_loc[0][1] -= 1
                p_2_space_loc[0][0] -= 1
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] += 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] -= 1
            elif p_2_ro == 1:
                p_2_space_loc[0][1] += 1
                p_2_space_loc[0][0] -= 1
                p_2_space_loc[1][1] -= 1
                p_2_space_loc[1][0] -= 1
                p_2_space_loc[3][1] += 1
                p_2_space_loc[3][0] += 1

        p_2_ro_change = False
        
        for i in range(0,4):
            if p_2_space_loc[i][1] == -2:
                for j in range(0,4):
                    p_2_space_loc[j][1] += 2
                p_2_now_block_x_pos += block_size*2
            elif p_2_space_loc[i][1] == 11:
                for j in range(0,4):
                    p_2_space_loc[j][1] -= 2  
                p_2_now_block_x_pos -= block_size*2
            elif p_2_space_loc[i][1] == -1:
                for j in range(0,4):
                    p_2_space_loc[j][1] += 1
                p_2_now_block_x_pos += block_size
            elif p_2_space_loc[i][1] == 10:
                for j in range(0,4):
                    p_2_space_loc[j][1] -= 1  
                p_2_now_block_x_pos -= block_size

        for i in range(0,4):
            if p_2_space_loc[i][0] > 21 or p_2_space[p_2_space_loc[i][0]][p_2_space_loc[i][1]][0] == 1:
                p_2_space_loc = p_2_pre_ro_loc
                p_2_ro = p_2_pre_ro_num
                p_2_now_block_x_pos = p_2_pre_ro_x_pos
                break

    # 자연낙하, 게임시작
    if game_start == True:
        now_time = pygame.time.get_ticks()

        if int(now_time/500) != check_time:
            for i in range(0,4):
                if p_1_space_loc[i][0] == 21:
                    p_1_down = False
                    break
            for i in range(0,4):
                if p_1_space_loc[i][0]+1 <= 21 and p_1_space[p_1_space_loc[i][0]+1][p_1_space_loc[i][1]][0] == 1 and p_1_space_loc[2][0] > 1:
                    p_1_down = False
                    p_1_land_fin = True
                    break
            if p_1_down == True:
                p_1_now_block_y_pos += block_size           
                for i in range(0,4):
                    p_1_space_loc[i][0] += 1
            p_1_down = True

            for i in range(0,4):
                if p_2_space_loc[i][0] == 21:
                    p_2_down = False
                    break
            for i in range(0,4):
                if p_2_space_loc[i][0]+1 <= 21 and p_2_space[p_2_space_loc[i][0]+1][p_2_space_loc[i][1]][0] == 1 and p_2_space_loc[2][0] > 1:
                    p_2_down = False
                    p_2_land_fin = True
                    break
            if p_2_down == True:
                p_2_now_block_y_pos += block_size           
                for i in range(0,4):
                    p_2_space_loc[i][0] += 1
            p_2_down = True

        check_time = int(now_time/500)

    # 경계설정
    for i in range(0,4):
        if p_1_space_loc[i][0] == 23:
            for j in range(0,4):
                p_1_space_loc[j][0] -= 2
            p_1_now_block_y_pos -= block_size*2
        elif p_1_space_loc[i][0] == 22:
            for j in range(0,4):
                p_1_space_loc[j][0] -= 1
            p_1_now_block_y_pos -= block_size
        elif p_1_space_loc[i][0] == 21 and p_1_space_loc[2][0] > 1:
            p_1_land_fin = True
    
            
    for i in range(0,4):
        if p_2_space_loc[i][0] == 23:
            for j in range(0,4):
                p_2_space_loc[j][0] -= 2
            p_2_now_block_y_pos -= block_size*2
        elif p_2_space_loc[i][0] == 22:
            for j in range(0,4):
                p_2_space_loc[j][0] -= 1
            p_2_now_block_y_pos -= block_size
        elif p_2_space_loc[i][0] == 21 and p_2_space_loc[2][0] > 1:
            p_2_land_fin = True


    # 바닥에 블록 쌓기 준비
    if p_1_space_loc[2][0] > 1:
        if p_1_land_fin == True:
            for i in range(4):
                p_1_space[p_1_space_loc[i][0]][p_1_space_loc[i][1]][0] = 1
                p_1_space[p_1_space_loc[i][0]][p_1_space_loc[i][1]][1] = p_1_now_block
            p_1_new = True
    else:
        p_1_land_fin = False

    if p_2_space_loc[2][0] > 1:
        if p_2_land_fin == True:
            for i in range(4):
                p_2_space[p_2_space_loc[i][0]][p_2_space_loc[i][1]][0] = 1
                p_2_space[p_2_space_loc[i][0]][p_2_space_loc[i][1]][1] = p_2_now_block
            p_2_new = True
    else:
        p_2_land_fin = False

    

    # 4. 충돌 처리
   
    # 5. 화면에 그리기

    screen.blit(background, (0,0))

    screen.blit(p_1_background, (p_1_background_x_pos,p_1_background_y_pos))
    screen.blit(p_2_background, (p_2_background_x_pos,p_2_background_y_pos))

    screen.blit(next_ground, (p_1_background_x_pos+460,p_1_background_y_pos))
    screen.blit(next_ground, (p_2_background_x_pos+460,p_2_background_y_pos))

    #다음 블록 
    if p_1_next_block_num == 1:
        screen.blit(block_1, (p_1_background_x_pos+460+14, p_1_background_y_pos+28))
        screen.blit(block_1, (p_1_background_x_pos+460+14+block_size, p_1_background_y_pos+28))
        screen.blit(block_1, (p_1_background_x_pos+460+14+block_size*2, p_1_background_y_pos+28))
        screen.blit(block_1, (p_1_background_x_pos+460+14+block_size*3, p_1_background_y_pos+28))
    if p_1_next_block_num == 2:
        screen.blit(block_2, (p_1_background_x_pos+460+57, p_1_background_y_pos+7))
        screen.blit(block_2, (p_1_background_x_pos+460+57+block_size, p_1_background_y_pos+7))
        screen.blit(block_2, (p_1_background_x_pos+460+57, p_1_background_y_pos+7+block_size))
        screen.blit(block_2, (p_1_background_x_pos+460+57+block_size, p_1_background_y_pos+7+block_size))
    if p_1_next_block_num == 3:
        screen.blit(block_3, (p_1_background_x_pos+460+35, p_1_background_y_pos+7))
        screen.blit(block_3, (p_1_background_x_pos+460+35, p_1_background_y_pos+7+block_size))
        screen.blit(block_3, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7+block_size))
        screen.blit(block_3, (p_1_background_x_pos+460+35+block_size*2, p_1_background_y_pos+7+block_size))
    if p_1_next_block_num == 4:
        screen.blit(block_4, (p_1_background_x_pos+460+35+block_size*2, p_1_background_y_pos+7))
        screen.blit(block_4, (p_1_background_x_pos+460+35, p_1_background_y_pos+7+block_size))
        screen.blit(block_4, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7+block_size))
        screen.blit(block_4, (p_1_background_x_pos+460+35+block_size*2, p_1_background_y_pos+7+block_size))
    if p_1_next_block_num == 5:
        screen.blit(block_5, (p_1_background_x_pos+460+35, p_1_background_y_pos+7))
        screen.blit(block_5, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7))
        screen.blit(block_5, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7+block_size))
        screen.blit(block_5, (p_1_background_x_pos+460+35+block_size*2, p_1_background_y_pos+7+block_size))
    if p_1_next_block_num == 6:
        screen.blit(block_6, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7))
        screen.blit(block_6, (p_1_background_x_pos+460+35+block_size*2, p_1_background_y_pos+7))
        screen.blit(block_6, (p_1_background_x_pos+460+35, p_1_background_y_pos+7+block_size))
        screen.blit(block_6, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7+block_size))
    if p_1_next_block_num == 7:
        screen.blit(block_7, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7))
        screen.blit(block_7, (p_1_background_x_pos+460+35, p_1_background_y_pos+7+block_size))
        screen.blit(block_7, (p_1_background_x_pos+460+35+block_size, p_1_background_y_pos+7+block_size))
        screen.blit(block_7, (p_1_background_x_pos+460+35+block_size*2, p_1_background_y_pos+7+block_size))

    if p_2_next_block_num == 1:
        screen.blit(block_1, (p_2_background_x_pos+460+14, p_2_background_y_pos+28))
        screen.blit(block_1, (p_2_background_x_pos+460+14+block_size, p_2_background_y_pos+28))
        screen.blit(block_1, (p_2_background_x_pos+460+14+block_size*2, p_2_background_y_pos+28))
        screen.blit(block_1, (p_2_background_x_pos+460+14+block_size*3, p_2_background_y_pos+28))
    if p_2_next_block_num == 2:
        screen.blit(block_2, (p_2_background_x_pos+460+57, p_2_background_y_pos+7))
        screen.blit(block_2, (p_2_background_x_pos+460+57+block_size, p_2_background_y_pos+7))
        screen.blit(block_2, (p_2_background_x_pos+460+57, p_2_background_y_pos+7+block_size))
        screen.blit(block_2, (p_2_background_x_pos+460+57+block_size, p_2_background_y_pos+7+block_size))
    if p_2_next_block_num == 3:
        screen.blit(block_3, (p_2_background_x_pos+460+35, p_2_background_y_pos+7))
        screen.blit(block_3, (p_2_background_x_pos+460+35, p_2_background_y_pos+7+block_size))
        screen.blit(block_3, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7+block_size))
        screen.blit(block_3, (p_2_background_x_pos+460+35+block_size*2, p_2_background_y_pos+7+block_size))
    if p_2_next_block_num == 4:
        screen.blit(block_4, (p_2_background_x_pos+460+35+block_size*2, p_2_background_y_pos+7))
        screen.blit(block_4, (p_2_background_x_pos+460+35, p_2_background_y_pos+7+block_size))
        screen.blit(block_4, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7+block_size))
        screen.blit(block_4, (p_2_background_x_pos+460+35+block_size*2, p_2_background_y_pos+7+block_size))
    if p_2_next_block_num == 5:
        screen.blit(block_5, (p_2_background_x_pos+460+35, p_2_background_y_pos+7))
        screen.blit(block_5, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7))
        screen.blit(block_5, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7+block_size))
        screen.blit(block_5, (p_2_background_x_pos+460+35+block_size*2, p_2_background_y_pos+7+block_size))
    if p_2_next_block_num == 6:
        screen.blit(block_6, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7))
        screen.blit(block_6, (p_2_background_x_pos+460+35+block_size*2, p_2_background_y_pos+7))
        screen.blit(block_6, (p_2_background_x_pos+460+35, p_2_background_y_pos+7+block_size))
        screen.blit(block_6, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7+block_size))
    if p_2_next_block_num == 7:
        screen.blit(block_7, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7))
        screen.blit(block_7, (p_2_background_x_pos+460+35, p_2_background_y_pos+7+block_size))
        screen.blit(block_7, (p_2_background_x_pos+460+35+block_size, p_2_background_y_pos+7+block_size))
        screen.blit(block_7, (p_2_background_x_pos+460+35+block_size*2, p_2_background_y_pos+7+block_size))


    #떨어지는 블록 그리기
    if p_1_now_block_num == 1:
        if p_1_ro == 1 or p_1_ro == 3:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size , p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size*2 , p_1_now_block_y_pos))
        elif p_1_ro == 2 or p_1_ro == 4:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size*2))

    if p_2_now_block_num == 1:
        if p_2_ro == 1 or p_2_ro == 3:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size , p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size*2 , p_2_now_block_y_pos))
        elif p_2_ro == 2 or p_2_ro == 4:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size*2))

    if p_1_now_block_num == 2:
        screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
        screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
        screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos - block_size))
        screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))

    if p_2_now_block_num == 2:
        screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
        screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
        screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos - block_size))
        screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))

    if p_1_now_block_num == 3:
        if p_1_ro == 1:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
        if p_1_ro == 2:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
        if p_1_ro == 3:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos + block_size))
        if p_1_ro == 4:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos + block_size))

    if p_2_now_block_num == 3:
        if p_2_ro == 1:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
        if p_2_ro == 2:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
        if p_2_ro == 3:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos + block_size))
        if p_2_ro == 4:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos + block_size))
            
    if p_1_now_block_num == 4:
        if p_1_ro == 1:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
        if p_1_ro == 2:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos + block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
        if p_1_ro == 3:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos + block_size))
        if p_1_ro == 4:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos - block_size))

    if p_2_now_block_num == 4:
        if p_2_ro == 1:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
        if p_2_ro == 2:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos + block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
        if p_2_ro == 3:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos + block_size))
        if p_2_ro == 4:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos - block_size))

    if p_1_now_block_num == 5:
        if p_1_ro == 1:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
        if p_1_ro == 2:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
        if p_1_ro == 3:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos + block_size))
        if p_1_ro == 4:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos + block_size))

    if p_2_now_block_num == 5:
        if p_2_ro == 1:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
        if p_2_ro == 2:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
        if p_2_ro == 3:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos + block_size))
        if p_2_ro == 4:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos + block_size))

    if p_1_now_block_num == 6:
        if p_1_ro == 1:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
        if p_1_ro == 2:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos + block_size))
        if p_1_ro == 3:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos + block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
        if p_1_ro == 4:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))

    if p_2_now_block_num == 6:
        if p_2_ro == 1:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
        if p_2_ro == 2:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos + block_size))
        if p_2_ro == 3:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos + block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
        if p_2_ro == 4:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
    
    if p_1_now_block_num == 7:
        if p_1_ro == 1:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
        if p_1_ro == 2:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
        if p_1_ro == 3:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos + block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))
        if p_1_ro == 4:
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos - block_size))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos - block_size, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos))
            screen.blit(p_1_now_block, (p_1_now_block_x_pos, p_1_now_block_y_pos + block_size))

    if p_2_now_block_num == 7:
        if p_2_ro == 1:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
        if p_2_ro == 2:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
        if p_2_ro == 3:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos + block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))
        if p_2_ro == 4:
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos - block_size))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos - block_size, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos))
            screen.blit(p_2_now_block, (p_2_now_block_x_pos, p_2_now_block_y_pos + block_size))

    #스킬 사용
    if p_1_skill_erase == True:
        del p_1_space[-1]
        del p_1_space[-1]
        p_1_space.insert(0,[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]) 
        p_1_space.insert(0,[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]) 
        p_1_skill_erase = False

    if p_2_skill_erase == True:
        del p_2_space[-1]
        del p_2_space[-1]
        p_2_space.insert(0,[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]) 
        p_2_space.insert(0,[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]) 
        p_2_skill_erase = False


    #블록 제거
    for i in range(22):
        p_1_stack = 0
        for j in range(10):
            if p_1_space[i][j][0] == 0:
                break
            else:
                p_1_stack += 1
        if p_1_stack == 10:
            del p_1_space[i]
            p_1_space.insert(0,[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
            p_1_attack += 1
    
    for i in range(22):
        p_2_stack = 0
        for j in range(10):
            if p_2_space[i][j][0] == 0:
                break
            else:
                p_2_stack += 1
        if p_2_stack == 10:
            del p_2_space[i]
            p_2_space.insert(0,[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]) 
            p_2_attack += 1


    #공격
    if p_1_attack > 0:
        if p_2_new == True:
            for i in range(p_1_attack):
                p_2_space.append([[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8]])
                del p_2_space[0]
                p_2_space[-1][random.randint(0,9)] = [0,0]
            p_1_attack = 0

    if p_2_attack > 0:
        if p_1_new == True:
            for i in range(p_2_attack):
                p_1_space.append([[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8],[1,block_8]])
                del p_1_space[0]
                p_1_space[-1][random.randint(0,9)] = [0,0]
            p_2_attack = 0


    #블록 위치 초기화, 쌓인 블록 화면에 그리기
    if p_1_land_fin == True:
        p_1_now_block_x_pos = p_1_background_x_pos + block_size * 4
        p_1_now_block_y_pos = p_1_background_y_pos - block_size
        p_1_land_fin = False

    for i in range(22):
        for j in range(10):
            if p_1_space[i][j][0] == 1:
                screen.blit(p_1_space[i][j][1], (p_1_background_x_pos + block_size*j, p_1_background_y_pos + block_size*(i-2)))

    if p_2_land_fin == True:
        p_2_now_block_x_pos = p_2_background_x_pos + block_size * 4
        p_2_now_block_y_pos = p_2_background_y_pos - block_size
        p_2_land_fin = False

    for i in range(22):
        for j in range(10):
            if p_2_space[i][j][0] == 1:
                screen.blit(p_2_space[i][j][1], (p_2_background_x_pos + block_size*j, p_2_background_y_pos + block_size*(i-2)))

    #게임 종료
    for i in range(9):
        if p_1_space[2][i][0] == 1:
            player_2_win = True

    for i in range(9):
        if p_2_space[2][i][0] == 1:
            player_1_win = True

    if player_1_win == True:
        screen.blit(win_pic, (p_1_background_x_pos+15, p_1_background_y_pos+200))
        screen.blit(lose_pic, (p_2_background_x_pos+15, p_2_background_y_pos+200))
        runing = False
    if player_2_win == True:
        screen.blit(win_pic, (p_2_background_x_pos+15, p_2_background_y_pos+200))
        screen.blit(lose_pic, (p_1_background_x_pos+15, p_1_background_y_pos+200))
        runing = False

    #게임 시작 화면
    if game_start == False:
        screen.blit(game_start_pic, (500, 250))

    pygame.display.update() # 개임화면을 다시 그리기

pygame.time.delay(3500)

pygame.quit()