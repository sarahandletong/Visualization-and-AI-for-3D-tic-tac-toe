import operator
import random
import time
from collections import defaultdict
import sys
from copy import deepcopy

import pygame
from direction_calculation import DirectionCalculation
from point_conversion import PointConversion
from connect_3d_error import Connect3DError


class Connect3D(object):
    player_symbols = 'XY'
    grid_size_recommended = 4

    def __init__(self, grid_size=grid_size_recommended):

        pygame.init()
        pygame.display.set_caption("Negamax Alpha Beta 剪枝 算法博弈")
        self.my_font = pygame.font.SysFont("arial", 20)
        self.surface = pygame.display.set_mode((582, 582))
        self.clock = pygame.time.Clock()

        self.current_position = ""

        try:
            self.current_player
        except AttributeError:
            self.current_player = random.randint(0, 1)

        self._display_score = False

        try:
            self.grid_size = int(grid_size)
        except TypeError:
            raise TypeError('grid_size must be an integer')
        self.grid_data = ['' for i in range(pow(grid_size, 3))]

        self.grid_size_squared = pow(self.grid_size, 2)

        self.direction_edges = {}
        self.direction_edges['U'] = range(self.grid_size_squared)
        self.direction_edges['D'] = range(self.grid_size_squared * (self.grid_size - 1),
                                          self.grid_size_squared * self.grid_size)
        self.direction_edges['R'] = [i * self.grid_size + self.grid_size - 1 for i in range(self.grid_size_squared)]
        self.direction_edges['L'] = [i * self.grid_size for i in range(self.grid_size_squared)]
        self.direction_edges['F'] = [i * self.grid_size_squared + j + self.grid_size_squared - self.grid_size for i in
                                     range(self.grid_size) for j in range(self.grid_size)]
        self.direction_edges['B'] = [i * self.grid_size_squared + j for i in range(self.grid_size) for j in
                                     range(self.grid_size)]
        self.direction_edges[' '] = []

        self.direction_maths = {}
        self.direction_maths['D'] = self.grid_size_squared
        self.direction_maths['R'] = 1
        self.direction_maths['F'] = self.grid_size
        self.direction_maths['U'] = -self.direction_maths['D']
        self.direction_maths['L'] = -self.direction_maths['R']
        self.direction_maths['B'] = -self.direction_maths['F']
        self.direction_maths[' '] = 0

    def __repr__(self):

        grid_data_joined = ''.join(str(i).ljust(1) for i in self.grid_data)
        return "Connect3D.from_string('{}.{}')".format(grid_data_joined, self.current_player)

    def __str__(self):

        k = 0

        grid_range = range(self.grid_size)
        grid_output = []

        if self._display_score:
            grid_output.append(self.show_score())

        for j in grid_range:

            row_top = ' ' * (self.grid_size * 2 + 1) + '_' * (self.grid_size * 4)
            if j:
                row_top = '|' + row_top[:self.grid_size * 2 - 1] + '|' + '_' * (self.grid_size * 2) + '|' + '_' * (
                        self.grid_size * 2 - 1) + '|'
            grid_output.append(row_top)

            for i in grid_range:
                row_display = ' ' * (self.grid_size * 2 - i * 2) + '/' + ''.join(
                    (' ' + str(self.grid_data[k + x]).ljust(1) + ' /') for x in grid_range)
                k += self.grid_size
                row_bottom = ' ' * (self.grid_size * 2 - i * 2 - 1) + '/' + '___/' * self.grid_size

                if j != grid_range[-1]:
                    row_display += ' ' * (i * 2) + '|'
                    row_bottom += ' ' * (i * 2 + 1) + '|'
                if j:
                    row_display = row_display[:self.grid_size * 4 + 1] + '|' + row_display[self.grid_size * 4 + 2:]
                    row_bottom = row_bottom[:self.grid_size * 4 + 1] + '|' + row_bottom[self.grid_size * 4 + 2:]

                    row_display = '|' + row_display[1:]
                    row_bottom = '|' + row_bottom[1:]

                grid_output += [row_display, row_bottom]

        return '\n'.join(grid_output)

    def _get_winning_player(self):

        self.update_score()
        return get_max_dict_keys(self.current_points)

    @classmethod
    def from_string(cls, raw_data):

        split_data = raw_data.split('.')
        grid_data = [i if i != ' ' else '' for i in split_data[0]]
        new_c3d_instance = cls(calculate_grid_size(grid_data))

        new_c3d_instance.grid_data = grid_data

        if len(split_data) > 1:
            new_c3d_instance.current_player = split_data[1]

        return new_c3d_instance

    @classmethod
    def from_list(cls, grid_data, player=None):

        new_c3d_instance = cls(calculate_grid_size(grid_data))

        new_c3d_instance.grid_data = [i if i != ' ' else '' for i in grid_data]

        if player is not None:
            new_c3d_instance.current_player = player

        return new_c3d_instance

    def play(self, player1=True, player2=False, grid_shuffle_chance=None):

        self.current_player = int(not self.current_player)
        min_time_update = 0.1

        flag_player_symbols = 0
        # print(self.grid_data)
        # threading.Thread(target=self.play_ui).start()
        while True:
            self.current_position = ""
            print(self.grid_data)
            if flag_player_symbols == 4:
                flag_player_symbols = 0

            if flag_player_symbols == 0 or flag_player_symbols == 1:
                self.player_symbols = "XY"

            if flag_player_symbols == 2 or flag_player_symbols == 3:
                self.player_symbols = "OW"

            current_time = time.time()

            self.current_player = int(not self.current_player)

            # was_flipped = self.shuffle(chance=grid_shuffle_chance)

            self.update_score()
            self._display_score = True
            print(self)
            self._display_score = False

            # if was_flipped:
            #     print("Flip the Grid!")

            if '' not in self.grid_data:
                winning_player = self._get_winning_player()
                if len(winning_player) == 1:
                    print('Player {} won!'.format(winning_player[0]))
                else:
                    print('It is a draw!')

                print('Want to play again?')
                play_again = input().lower()
                if any(i in play_again for i in ('y', 'k')):
                    self.reset()
                else:
                    return
                    break

            print("Player {}'s turn...".format(self.player_symbols[self.current_player]))
            if (player1 and not self.current_player) or (player2 and self.current_player):
                while True:

                    if self.current_position == "":
                        # for idx, unit in enumerate(self.grid_data):
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
                        #     pygame.draw.rect(self.surface, grid_color,
                        #                      ((y + 1) * 2 + y * 80, (x + 1) * 2 + x * 40, 80, 40))
                        #     text_surface = self.my_font.render(unit, True, (0, 0, 0), grid_color)
                        #     text_surface_rect = text_surface.get_rect()
                        #     text_surface_rect.center = ((y + 1) * 2 + y * 80 + 40, (x + 1) * 2 + x * 40 + 20)
                        #     self.surface.blit(text_surface, text_surface_rect)
                        for dim in range(4):
                            dim_arr = self.grid_data[dim * 16:dim * 16 + 16]
                            if dim == 0:
                                for idx, unit in enumerate(dim_arr):
                                    x, y = divmod(idx, 4)
                                    pygame.draw.rect(self.surface, (255, 255, 255),
                                                     (y * 2 + y * 60 + 30, x * 2 + x * 60 + 30, 60, 60))
                                    text_surface = self.my_font.render(unit, True, (0, 0, 0), (255, 255, 255))
                                    text_surface_rect = text_surface.get_rect()
                                    text_surface_rect.center = (y * 2 + y * 60 + 30 + 30, x * 2 + x * 60 + 30 + 30)
                                    self.surface.blit(text_surface, text_surface_rect)
                            if dim == 1:
                                for idx, unit in enumerate(dim_arr):
                                    x, y = divmod(idx, 4)
                                    pygame.draw.rect(self.surface, (255, 248, 220), (
                                        y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2, x * 2 + x * 60 + 30, 60, 60))
                                    text_surface = self.my_font.render(unit, True, (0, 0, 0), (255, 248, 220))
                                    text_surface_rect = text_surface.get_rect()
                                    text_surface_rect.center = (
                                        y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2 + 30, x * 2 + x * 60 + 30 + 30)
                                    self.surface.blit(text_surface, text_surface_rect)
                            if dim == 2:
                                for idx, unit in enumerate(dim_arr):
                                    x, y = divmod(idx, 4)
                                    pygame.draw.rect(self.surface, (240, 255, 240), (
                                        y * 2 + y * 60 + 30, x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2, 60, 60))
                                    text_surface = self.my_font.render(unit, True, (0, 0, 0), (240, 255, 240))
                                    text_surface_rect = text_surface.get_rect()
                                    text_surface_rect.center = (
                                        y * 2 + y * 60 + 30 + 30, x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2 + 30)
                                    self.surface.blit(text_surface, text_surface_rect)
                            if dim == 3:
                                for idx, unit in enumerate(dim_arr):
                                    x, y = divmod(idx, 4)
                                    pygame.draw.rect(self.surface, (230, 230, 250), (
                                        y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2, x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2, 60,
                                        60))
                                    text_surface = self.my_font.render(unit, True, (0, 0, 0), (230, 230, 250))
                                    text_surface_rect = text_surface.get_rect()
                                    text_surface_rect.center = (y * 2 + y * 60 + 60 + 60 * 4 + 3 * 2 + 30,
                                                                x * 2 + x * 60 + 60 + 60 * 4 + 3 * 2 + 30)
                                    self.surface.blit(text_surface, text_surface_rect)

                        while True:
                            a = False
                            self.clock.tick(60)
                            for event in pygame.event.get():

                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    # print(mouse_x, mouse_y)
                                    # self.current_position = str(mouse_x // 82 + 1) + " " + str(
                                    #     divmod(mouse_y // 42, 4)[1] + 1) + " " + str(divmod(mouse_y // 42, 4)[0] + 1)
                                    # print(self.current_position)
                                    if 30 <= mouse_x <= 30 + 4 * 60 + 3 * 2 and 30 <= mouse_y <= 30 + 4 * 60 + 3 * 2:
                                        self.current_position = str((mouse_x - 30) // 62 + 1) + " " + str(
                                            divmod((mouse_y - 30) // 62, 4)[
                                                1] + 1) + " 1"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                                        # print(current_position)
                                    if 60 + 4 * 60 + 3 * 2 <= mouse_x <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2 and 30 <= mouse_y <= 30 + 4 * 60 + 3 * 2:
                                        self.current_position = str(
                                            (mouse_x - (60 + 4 * 60 + 3 * 2)) // 62 + 1) + " " + str(
                                            divmod((mouse_y - 30) // 62, 4)[
                                                1] + 1) + " 2"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                                        # print(current_position)
                                    if 30 <= mouse_x <= 30 + 4 * 60 + 3 * 2 and 60 + 4 * 60 + 3 * 2 <= mouse_y <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2:
                                        self.current_position = str((mouse_x - 30) // 62 + 1) + " " + str(
                                            divmod((mouse_y - (60 + 4 * 60 + 3 * 2)) // 62, 4)[
                                                1] + 1) + " 3"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                                        # print(current_position)
                                    if 60 + 4 * 60 + 3 * 2 <= mouse_x <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2 and 60 + 4 * 60 + 3 * 2 <= mouse_y <= 60 + 4 * 60 + 3 * 2 + 4 * 60 + 3 * 2:
                                        self.current_position = str(
                                            (mouse_x - (60 + 4 * 60 + 3 * 2)) // 62 + 1) + " " + str(
                                            divmod((mouse_y - (60 + 4 * 60 + 3 * 2)) // 62, 4)[
                                                1] + 1) + " 4"  # + " " + str(divmod(mouse_y // 62, 4)[0] + 1)
                                        # print(current_position)

                                    a = True

                                pygame.display.update()
                            if a:
                                break
                    else:
                        break
                while not self.algorithm_detect(self.player_symbols[self.current_player],
                                                self.current_position.replace(',', ' ').replace('.', ' ').split()):
                    print("Grid cell unavailable, please try again.")
                # while not self.algorithm_detect(self.player_symbols[self.current_player], "2 2 2"):
                #     print("Grid cell unavailable, please try again.")

            else:
                ai_go = SimpleC3DAI(self, self.current_player).calculate_next_move()
                if not self.algorithm_detect(self.player_symbols[self.current_player], ai_go):
                    raise Connect3DError('Something unknown went wrong with the AI')
                else:
                    print("Computer chooses the cell {}.".format(PointConversion(self.grid_size, ai_go).to_3d()))

                time.sleep(max(0, min_time_update, time.time() - current_time))
            print()
            flag_player_symbols += 1

    def algorithm_detect(self, id, *args):

        if len(args) == 1:
            if not str(args[0]).replace('-', '').isdigit():
                if len(args[0]) == 1:
                    try:
                        i = int(args[0][0])
                    except ValueError:
                        return False
                else:
                    i = PointConversion(self.grid_size, args[0]).to_int()
            else:
                i = int(args[0])
        else:
            i = PointConversion(self.grid_size, tuple(args)).to_int()

        if 0 <= i < len(self.grid_data) and not self.grid_data[i] and i is not None:
            self.grid_data[i] = id
            return True
        else:
            return False

    def shuffle(self, chance=None, second_chance=None, repeats=None, no_shuffle=[]):

        if chance is None:
            chance = 33
        if second_chance is None:
            second_chance = 50
        if repeats is None:
            repeats = 3

        chance = min(100, chance)
        if chance > 0:
            chance = int(round(400 / chance)) - 1

            for i in range(repeats):
                shuffle_num = random.randint(0, chance)
                if shuffle_num in (0, 1, 2, 3) and shuffle_num not in no_shuffle:
                    no_shuffle.append(shuffle_num)
                    if shuffle_num == 0:
                        self.grid_data = SwapGridData(self.grid_data).x()
                    if shuffle_num == 1:
                        self.grid_data = SwapGridData(self.grid_data).y()
                    if shuffle_num == 2:
                        self.grid_data = SwapGridData(self.grid_data).z()
                    if shuffle_num == 3:
                        self.grid_data = SwapGridData(self.grid_data).reverse()
                    if self.shuffle(chance=second_chance, no_shuffle=no_shuffle) or not not no_shuffle:
                        return True

    def update_score(self):

        try:
            self.grid_data_last_updated
        except AttributeError:
            self.grid_data_last_updated = None

        if self.grid_data_last_updated != hash(tuple(self.grid_data)):

            self.grid_data_last_updated = hash(tuple(self.grid_data))

            self.current_points = defaultdict(int)
            all_matches = set()

            for starting_point in range(len(self.grid_data)):

                current_player = self.grid_data[starting_point]

                if current_player:

                    for i in DirectionCalculation().opposite_direction:

                        possible_directions = [list(i)]
                        possible_directions += [[j.replace(i, '') for i in possible_directions[0] for j in
                                                 DirectionCalculation().direction_group.values() if i in j]]
                        direction_movement = sum(self.direction_maths[j] for j in possible_directions[0])

                        invalid_directions = [[self.direction_edges[j] for j in possible_directions[k]] for k in (0, 1)]
                        invalid_directions = [join_list(j) for j in invalid_directions]

                        num_matches = 1
                        list_match = [starting_point]

                        for j in (0, 1):

                            current_point = starting_point

                            while current_point not in invalid_directions[j] and 0 < current_point < len(
                                    self.grid_data):
                                current_point += direction_movement * int('-'[:j] + '1')
                                if self.grid_data[current_point] == current_player:
                                    num_matches += 1
                                    list_match.append(current_point)
                                else:
                                    break

                        if num_matches == self.grid_size:

                            list_match = hash(tuple(sorted(list_match)))
                            if list_match not in all_matches:
                                all_matches.add(list_match)
                                self.current_points[current_player] += 1

    def show_score(self, digits=False, marker='/'):

        self.update_score()
        multiply_value = 1 if digits else marker
        return 'Player X (Human)|| {x}  Player O (Computer)|| {o}'.format(x=multiply_value * (self.current_points['X']),
                                                                          o=multiply_value * self.current_points['O'])

    def reset(self):

        self.grid_data = ['' for i in range(pow(self.grid_size, 3))]


class SwapGridData(object):

    def __init__(self, grid_data):
        self.grid_data = list(grid_data)
        self.grid_size = calculate_grid_size(self.grid_data)

    def x(self):
        return join_list(x[::-1] for x in split_list(self.grid_data, self.grid_size))

    def y(self):
        group_split = split_list(self.grid_data, pow(self.grid_size, 2))
        return join_list(join_list(split_list(x, self.grid_size)[::-1]) for x in group_split)

    def z(self):
        return join_list(split_list(self.grid_data, pow(self.grid_size, 2))[::-1])

    def reverse(self):
        return self.grid_data[::-1]


def calculate_grid_size(grid_data):
    return int(round(pow(len(grid_data), 1.0 / 3.0), 0))


def split_list(x, n):
    n = int(n)
    return [x[i:i + n] for i in range(0, len(x), n)]


def join_list(x):
    return [j for i in x for j in i]


def get_max_dict_keys(x):
    if x:
        sorted_dict = sorted(x.iteritems(), key=operator.itemgetter(1), reverse=True)
        if sorted_dict[0][1]:
            return sorted([k for k, v in x.iteritems() if v == sorted_dict[0][1]])
    return []


class SimpleC3DAI(object):

    def __init__(self, C3DObject, player_num):

        self.C3DObject = C3DObject
        self.player_num = player_num
        self.player = self.C3DObject.player_symbols[self.player_num]
        self.enemy = self.C3DObject.player_symbols[int(not self.player_num)]
        self.gd_len = len(self.C3DObject.grid_data)

    def max_cell_points(self):

        max_points = defaultdict(int)
        filled_grid_data = [i if i else self.player for i in self.C3DObject.grid_data]
        for cell_id in range(self.gd_len):
            if cell_id == self.player:
                max_points[cell_id] += self.check_grid(filled_grid_data, cell_id, self.player)
        return get_max_dict_keys(max_points)

    def check_for_n_minus_one(self, grid_data=None):

        if grid_data is None:
            grid_data = list(self.C3DObject.grid_data)

        matches = defaultdict(list)
        for cell_id in range(len(grid_data)):
            if not grid_data[cell_id]:
                for current_player in (self.player, self.enemy):
                    if self.check_grid(grid_data, cell_id, current_player):
                        matches[current_player].append(cell_id)
        return matches

    def look_ahead(self):

        match = self.check_for_n_minus_one()
        if match:
            return (match, 0)

        grid_data = list(self.C3DObject.grid_data)
        for i in range(self.gd_len):
            if not self.C3DObject.grid_data[i]:
                old_value = grid_data[i]
                for current_player in (self.player, self.enemy):
                    grid_data[i] = current_player
                    match = self.check_for_n_minus_one(grid_data)
                    if match:
                        return (match, 1)
                grid_data[i] = old_value

        return (defaultdict(list), 0)

    def check_grid(self, grid_data, cell_id, player):

        max_points = 0
        for i in DirectionCalculation().opposite_direction:

            possible_directions = [list(i)]
            possible_directions += [[j.replace(i, '') for i in possible_directions[0] for j in
                                     DirectionCalculation().direction_group.values() if i in j]]
            direction_movement = sum(self.C3DObject.direction_maths[j] for j in possible_directions[0])

            invalid_directions = [[self.C3DObject.direction_edges[j] for j in possible_directions[k]] for k in (0, 1)]
            invalid_directions = [join_list(j) for j in invalid_directions]

            num_matches = 1

            for j in (0, 1):

                current_point = cell_id

                while current_point not in invalid_directions[j] and 0 < current_point < len(grid_data):
                    current_point += direction_movement * int('-'[:j] + '1')
                    if grid_data[current_point] == player:
                        num_matches += 1
                    else:
                        break

            if num_matches == self.C3DObject.grid_size:
                max_points += 1

        return max_points

    def negamax(self, Board, maximizingPlayer, depth, count):

        if maximizingPlayer:
            player, opp = Board.player, Board.opp
        else:
            player, opp = Board.opp, Board.player

        moves_list = Board.get_moves_list(player, opp)
        best_move = (-1, -1)

        if (depth == 0 or moves_list == []):
            best_score, parity, mobility, stability = Board.evaluate()
            best_move = (-1, -1)
            return best_score, best_move, count

        best_score = float("-inf")
        for move in moves_list:
            new_board = deepcopy(Board)
            new_board.play_legal_move(move[0], move[1], player, opp, flip=True)
            the_score, the_move, count = -self.negamax(new_board, False, depth - 1, count + 1)
            best_score = max(best_score, the_score)
            if (the_score == best_score):
                best_move = move

        return best_score, best_move, count

    def calculate_next_move(self):

        next_moves = []

        if len(''.join(self.C3DObject.grid_data)) > (self.C3DObject.grid_size - 2) * 2:

            point_based_move, far_away = SimpleC3DAI(self.C3DObject, self.player_num).look_ahead()
            order_of_importance = [self.enemy, self.player][::int('-'[:int(far_away)] + '1')]
            grid_data_len = len(''.join(self.C3DObject.grid_data))

            state = None

            if point_based_move:
                if point_based_move[self.enemy]:
                    next_moves = point_based_move[self.enemy]
                    state = 'Block'

                elif point_based_move[self.player]:
                    next_moves = point_based_move[self.player]
                    state = 'Gain'

            else:
                next_moves = self.max_cell_points()
                state = 'Arbitary'

            if not next_moves:
                next_moves = [i for i in range(self.gd_len) if not self.C3DObject.grid_data[i]]
                if state is None:
                    state = 'Struggle'

        else:
            next_moves = [i for i in range(self.gd_len) if not self.C3DObject.grid_data[i]]
            state = 'Start'

        print('Computer State: ' + state + '.')

        return random.choice(next_moves)


if __name__ == '__main__':
    c3d = Connect3D()
    c3d.play(True, False)
