import sys

import pygame

pygame.init()
my_font = pygame.font.SysFont("arial", 20)
surface = pygame.display.set_mode((582, 582))
pygame.display.set_caption("4x4x4 tic-tac-toe AI")
clock = pygame.time.Clock()

arr = ['', '', '', '', 'X', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
       '', 'Y', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
       '', '', '', '', '', '', '', '']

# for idx, unit in enumerate(arr):
#     x, y = divmod(idx, 4)
#     d, p = divmod(x, 4)
#     if d == 0:
#         grid_color = (255, 255, 255)
#     elif d == 1:
#         grid_color = (255, 248, 220)
#     elif d == 2:
#         grid_color = (240, 255, 240)
#     else:
#         grid_color = (230, 230, 250)
#
#     pygame.draw.rect(surface, grid_color, ((y + 1) * 2 + y * 80, (x + 1) * 2 + x * 40, 80, 40))
#     text_surface = my_font.render(unit, True, (0, 0, 0), grid_color)
#     text_surface_rect = text_surface.get_rect()
#     text_surface_rect.center = ((y + 1) * 2 + y * 80 + 40, (x + 1) * 2 + x * 40 + 20)
#     surface.blit(text_surface, text_surface_rect)

for dim in range(4):
    dim_arr = arr[dim * 16:dim * 16 + 16]
    if dim == 0:
        for idx, unit in enumerate(dim_arr):
            x, y = divmod(idx, 4)
            pygame.draw.rect(surface, (255, 255, 255), (y * 2 + y * 60 + 30, x * 2 + x * 60 + 30, 60, 60))
            text_surface = my_font.render(unit, True, (0, 0, 0), (255, 255, 255))
            text_surface_rect = text_surface.get_rect()
            text_surface_rect.center = (y * 2 + y * 60 + 30 + 30, x * 2 + x * 60 + 30 + 30)
            surface.blit(text_surface, text_surface_rect)
    if dim == 1:
        for idx, unit in enumerate(dim_arr):
            x, y = divmod(idx, 4)
            pygame.draw.rect(surface, (255, 248, 220), (y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2, x * 2 + x * 60 + 30, 60, 60))
            text_surface = my_font.render(unit, True, (0, 0, 0), (255, 248, 220))
            text_surface_rect = text_surface.get_rect()
            text_surface_rect.center = (y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2 + 30, x * 2 + x * 60 + 30 + 30)
            surface.blit(text_surface, text_surface_rect)
    if dim == 2:
        for idx, unit in enumerate(dim_arr):
            x, y = divmod(idx, 4)
            pygame.draw.rect(surface, (240, 255, 240), (y * 2 + y * 60 + 30, x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2, 60, 60))
            text_surface = my_font.render(unit, True, (0, 0, 0), (240, 255, 240))
            text_surface_rect = text_surface.get_rect()
            text_surface_rect.center = (y * 2 + y * 60 + 30 + 30, x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2 + 30)
            surface.blit(text_surface, text_surface_rect)
    if dim == 3:
        for idx, unit in enumerate(dim_arr):
            x, y = divmod(idx, 4)
            pygame.draw.rect(surface, (230, 230, 250), (y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2, x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2, 60, 60))
            text_surface = my_font.render(unit, True, (0, 0, 0), (230, 230, 250))
            text_surface_rect = text_surface.get_rect()
            text_surface_rect.center = (y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2 + 30, x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2 + 30)
            surface.blit(text_surface, text_surface_rect)

while True:
    # a = False
    clock.tick(60)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x, mouse_y)
            # row = 4 if divmod(mouse_y // 42 + 1, 4)[1] == 0 else divmod(mouse_y // 42 + 1, 4)[1]
            if 30 <= mouse_x <= 30 + 4 * 60 + 3 * 2 and 30 <= mouse_y <= 30 + 4 * 60 + 3 * 2:
                current_position = str((mouse_x - 30) // 62 + 1) + " " + str(divmod((mouse_y - 30) // 62, 4)[1] + 1) + " 1"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                print(current_position)
            if 60 + 4 * 60 + 3 * 2 <= mouse_x <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2 and 30 <= mouse_y <= 30 + 4 * 60 + 3 * 2:
                current_position = str((mouse_x - (60 + 4 * 60 + 3 * 2)) // 62 + 1) + " " + str(divmod((mouse_y - 30) // 62, 4)[1] + 1) + " 2"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                print(current_position)
            if 30 <= mouse_x <= 30 + 4 * 60 + 3 * 2 and 60 + 4 * 60 + 3 * 2 <= mouse_y <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2:
                current_position = str((mouse_x - 30) // 62 + 1) + " " + str(divmod((mouse_y - (60 + 4 * 60 + 3 * 2)) // 62, 4)[1] + 1) + " 3"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                print(current_position)
            if 60 + 4 * 60 + 3 * 2 <= mouse_x <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2 and 60 + 4 * 60 + 3 * 2 <= mouse_y <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2:
                current_position = str((mouse_x - (60 + 4 * 60 + 3 * 2)) // 62 + 1) + " " + str(divmod((mouse_y - (60 + 4 * 60 + 3 * 2)) // 62, 4)[1] + 1) + " 4"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                print(current_position)
            # a = True

        pygame.display.update()

    # if a:
    #     break
