import pygame
from tetrimino import *
from random import *
from pygame.locals import *

# 상수
block_size = 34 # 블록 크기 34x34
width = 10 # 너비
height = 20 # 높이
framerate = 30

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 720))
pygame.time.set_timer(pygame.USEREVENT, framerate * 10)
pygame.display.set_caption("DEFAULT TETRIS")

class ui_variables:

    font1 = "C:\Windows\Fonts\TCB_____.TTF"

    h1 = pygame.font.Font(font1, 50)
    h2 = pygame.font.Font(font1, 30)
    h4 = pygame.font.Font(font1, 30)
    h5 = pygame.font.Font(font1, 30)
    h6 = pygame.font.Font(font1, 25)

    h1_b = pygame.font.Font(font1, 50)
    h2_b = pygame.font.Font(font1, 30)

    h2_i = pygame.font.Font(font1, 30)
    h5_i = pygame.font.Font(font1, 13)

    # 색깔
    black = (10, 10, 10)
    white = (255, 255, 255)
    grey_1 = (26, 26, 26)
    grey_2 = (35, 35, 35)
    grey_3 = (55, 55, 55)

    # 테트리미노 색깔
    cyan = (69, 206, 204) # I
    blue = (64, 111, 249) # J
    orange = (253, 189, 53) # L
    yellow = (246, 227, 90) # O
    green = (98, 190, 68) # S
    pink = (242, 64, 235) # T
    red = (225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]

# 블록 설정
def draw_block(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )

# 게임 화면 설정
def draw_board(next, hold, score, level, goal):
    screen.fill(ui_variables.grey_1)

    # 옆쪽 UI 화면
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(375, 0, 240, 800)
    )

    # 다음 블록
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = 440 + block_size * j
            dy = 280 + block_size * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(
                    screen,
                    ui_variables.t_color[grid_n[i][j]],
                    Rect(dx, dy, block_size, block_size)
                )

                pygame.draw.rect(
                    screen,
                    ui_variables.black,
                    Rect(430, 250, 120, 120),
                    3
                )

    # 홀드
    grid_h = tetrimino.mino_map[hold - 1][0]

    pygame.draw.rect(
        screen,
        ui_variables.black,
        Rect(430, 70, 120, 120),
        3
    )

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 440 + block_size * j
                dy = 100 + block_size * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(
                        screen,
                        ui_variables.t_color[grid_h[i][j]],
                        Rect(dx, dy, block_size, block_size)
                    )

    # 최대 점수 설정
    if score > 999999:
        score = 999999

    # 텍스트
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)

    # 텍스트 배치
    screen.blit(text_hold, (430, 30))
    screen.blit(text_next, (430, 210))
    screen.blit(text_score, (430, 400))
    screen.blit(score_value, (440, 440))
    screen.blit(text_level, (430, 500))
    screen.blit(level_value, (440, 540))
    screen.blit(text_goal, (430, 600))
    screen.blit(goal_value, (440, 640))

    # 화면 설정
    for x in range(width):
        for y in range(height):
            dx = 17 + block_size * x
            dy = 17 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])

# 테트리미노 설정
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]

# 줄 지우기
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:
                matrix[i][j] = 0

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0

def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False

def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False

def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False

def is_turnable_r(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

def is_turnable_l(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True

# 대표값
blink = False
start = False
pause = False
done = False
game_over = False

score = 0
level = 1
goal = level * 5
bottom_count = 0
hard_drop = False

dx, dy = 3, 0 # 테트라미노 시작지점
rotation = 0 # 테트라미노 기본 모양

mino = randint(1, 7) # 현재 테트라미노
next_mino = randint(1, 7) # 다음 테트라미노

hold = False
hold_mino = -1 # 홀드한 테트라미노

name_location = 0
name = [65, 65, 65]

matrix = [[0 for y in range(height + 1)] for x in range(width)]


while not done:
    # Pause screen
    if pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                draw_board(next_mino, hold_mino, score, level, goal)

                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.white)
                pause_start = ui_variables.h5.render("Press esc to continue", 1, ui_variables.white)

                screen.blit(pause_text, (136, 200))
                if blink:
                    screen.blit(pause_start, (55, 320))
                    blink = False
                else:
                    blink = True
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = False
                    pygame.time.set_timer(pygame.USEREVENT, 1)

    # 게임 화면
    elif start:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:

                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 10)

                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)

                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # 테트라미노 생성
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        draw_board(next_mino, hold_mino, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # 라인 제거
                erase_count = 0
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    score += 50 * level
                elif erase_count == 2:
                    score += 150 * level
                elif erase_count == 3:
                    score += 350 * level
                elif erase_count == 4:
                    score += 1000 * level

                # 레벨 상승
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    pause = True

                # 하드드롭 기능
                elif event.key == K_SPACE:
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                # 홀드
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation):
                        rotation += 1
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        rotation -= 1

                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation):
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation):
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

        pygame.display.update()

    # 게임 오버 화면
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2_b.render("GAME", 2, ui_variables.white)
                over_text_2 = ui_variables.h2_b.render("OVER", 2, ui_variables.white)
                over_start = ui_variables.h6.render("Press return to continue", 2, ui_variables.white)

                draw_board(next_mino, hold_mino, score, level, goal)
                screen.blit(over_text_1, (140, 150))
                screen.blit(over_text_2, (140, 210))

                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.white)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.white)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.white)

                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.white)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.white)



                if blink:
                    screen.blit(over_start, (54, 400))
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, (130, 290))
                    elif name_location == 1:
                        screen.blit(underbar_2, (190, 290))
                    elif name_location == 2:
                        screen.blit(underbar_3, (250, 290))
                    blink = True

                pygame.display.update()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:

                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)

    # 시작 화면 설정
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    start = True

        # 시작 화면 UI
        screen.fill(ui_variables.white)

        title = ui_variables.h1.render("DEFAULT TETRIS", 1, ui_variables.grey_1)
        title_start = ui_variables.h5.render("Press space to start", 1, ui_variables.grey_1)

        if blink:
            screen.blit(title_start, (175, 400))
            blink = False
        else:
            blink = True

        screen.blit(title, (130, 120))

        if not start:
            pygame.display.update()
            clock.tick(3)

pygame.quit()
