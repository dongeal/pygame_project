import os
import pygame 

###################################################
# 기본 초기화 부분
pygame.init() # 초기화(반드시 필요)

#화면 크기 설정
screen_width = 640 # 가로
screen_height = 480  #세로
screen = pygame.display.set_mode((screen_width,screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang") #게임 이름

# FPS
clock = pygame.time.Clock()
###################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지,좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) #  현재파일 위치 반환
image_path = os.path.join(current_path, "images") # image 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path,"background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이위에 캐릭터를 두기위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path,"character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height -stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러발 발사 가능
weapons = []

# 무기 이동속도
weapon_speed = 10

# 공만들ㄴ기 (4개크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# 공크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0,1,2,3 에 해당값

# 공들
balls = []


balls =[50,50,0,3,-6,ball_speed_y[0]]
    # "pos_x" : 50, #공의 x 좌표
    # "pos_y" : 50, # 공의 y 좌표
    # "img_idx" : 0, # 공의 이미지 인덱스
    # "to_x" : 3, # x축방향 이동
    # "to_y" : -6, # y 축방향 이동
    # "init_spd_y" : ball_speed_y[0]}) # y  최초속도

print(balls)



running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #캐릭터 왼쪽으로 이동
                character_to_x -= character_speed
            elif  event.key == pygame.K_RIGHT: #캐릭터 오른으로 이동
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width /2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

                    
    # 3. 게임 캐릭터 위치정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #  무기 위치 조정
    # 100,200  --> 180, 160, 120, ...
    # 500,200  --->180, 160, 120 ,...
    weapons = [ [w[0],w[1]- weapon_speed]  for w in weapons ] # 무기위치를 위로
   
    # 천장에 닿은 무기 없애기
    weapons = [ [w[0],w[1]] for w in weapons if w[1] > 0] 
    # temporary = []
    # for w in weapons:
    #     if w[1] >0:
    #         temporary.append(w)
    # weapons = temporary 
    
    # 공의 위치 정의
    #for balls in balls:
    ball_pos_x = balls[0]
    ball_pos_y = balls[1]
    ball_img_idx = balls[2]
    ball_size = ball_images[ball_img_idx].get_rect().size
    ball_width = ball_size[0]
    ball_height = ball_size[1]
    # 가로벽에 닿았을때
    if ball_pos_x < 0 or  ball_pos_x > screen_width - ball_width:
        balls[3] = balls[3] * -1
    
    # 세로 위치
    #스테이지에 튕겨서 올라가는 처리
    if ball_pos_y >= screen_height -stage_height-ball_height:
        balls[4] = balls[5]
    else: # 그외는 속도를 증가
        balls[4] += 0.5
    balls[0] += balls[3]
    balls[1] += balls[4]

    # 4. 충돌처리 
   
    # 5. 화면에 그리기

    screen.blit(background,(0,0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos,weapon_y_pos))


    # for val in balls:
    ball_pos_x = balls[0]
    ball_pos_y = balls[1]
    ball_img_idx = balls[2]
    screen.blit(ball_images[ball_img_idx],(ball_pos_x,ball_pos_y))
   

    screen.blit(stage,(0,screen_height - stage_height))
    screen.blit(character,(character_x_pos, character_y_pos))

  

    pygame.display.update()
   
pygame.quit()