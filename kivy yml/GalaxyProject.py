from kivy.config import Config
from kivy.core.audio import SoundLoader

Config.set("graphics", "width", "900")
Config.set("graphics", "height", "400")

from kivy.uix.relativelayout import RelativeLayout
import random
from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty


class MenuWidget(RelativeLayout):

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False

        return super(RelativeLayout, self).on_touch_down(touch)


class Appwidget(RelativeLayout):
    from transform import transform_2D, perspective, transform
    perspective_x = NumericProperty(0)
    perspective_y = NumericProperty(0)
    menu_widget = ObjectProperty()
    v_number = 15
    v_spacing = .5  # percentage in width
    vertical_lines = []

    h_number = 10
    h_spacing = .2  # percentage in height
    horizontal_lines = []

    current_offset_y = 0
    current_offset_x = 0
    speed_y = 1
    speed_x = 3
    direction = 0

    tiles = []
    num_tiles = 9
    tile_coordinates = []

    SHIP_WIDTH = .15
    SHIP_HEIGHT = 0.075
    SHIP_BASE = 0.04
    ship_points = [(0, 0), (0, 0), (0, 0)]

    GAME_OVER = False
    game_start = False
    current_y_loop = 0

    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")
    score = StringProperty(f"SCORE >> 0")

    sound_start = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None

    def __init__(self, **kwargs):
        super(Appwidget, self).__init__(**kwargs)

        self.init_audio()
        self.ship = None
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()

        self.reset_game()

        if self.on_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.movingUpdate, 1.0 / 60.0)
        self.sound_galaxy.play()

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.direction -= self.speed_x
        elif keycode[1] == 'right':
            self.direction += self.speed_x

        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.direction = 0
        return True

    def on_desktop(self):
        if platform in ("linux", "win", "macosx"):
            return True
        else:
            return False

    def reset_game(self):
        self.tile_coordinates = []

        self.current_offset_y = 0
        self.current_offset_x = 0
        self.direction = 0
        self.current_y_loop = 0

        self.headStart()  # first
        self.tiles_coordinates()  # second

        self.GAME_OVER = False

    def on_perspective_x(self, widget, value):
        pass

    def on_perspective_y(self, widget, value):
        pass

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def check_collision(self):
        for i in range(0, len(self.tile_coordinates)):
            ti_x, ti_y = self.tile_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.on_collision(ti_x, ti_y):
                return True
        return False

    def on_collision(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
        for i in range(0, 3):
            px, py = self.ship_points[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(.5, .1, .001, .5)
            for i in range(0, self.num_tiles):
                self.tiles.append(Quad())

    def init_audio(self):
        self.sound_start = SoundLoader.load("audio/begin.wav")
        self.sound_galaxy = SoundLoader.load("audio/galaxy.wav")
        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
        self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.wav")
        self.sound_music1 = SoundLoader.load("audio/music1.wav")
        self.sound_restart = SoundLoader.load("audio/restart.wav")

        self.sound_music1.volume = 1
        self.sound_start.volume = 1
        self.sound_restart.volume = .25
        self.sound_galaxy.volume = .25
        self.sound_gameover_impact.volume = .60
        self.sound_gameover_voice.volume = .25

    def headStart(self):
        for i in range(0, 10):
            self.tile_coordinates.append((0, i))
        pass

    def tiles_coordinates(self):
        last_y = 0
        last_x = 0

        for i in range(len(self.tile_coordinates) - 1, -1, -1):
            if self.tile_coordinates[i][1] < self.current_y_loop:
                del self.tile_coordinates[i]

        if len(self.tile_coordinates) > 0:
            last_coordinates = self.tile_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tile_coordinates), self.num_tiles):
            r = random.randint(0, 2)  # changes from left to right
            start_index = -int(self.v_number / 2) + 1
            end_index = start_index + self.v_number - 1

            if last_x <= start_index:
                r = 1

            if last_x >= end_index - 1:
                r = 2

            self.tile_coordinates.append((last_x, last_y))

            if r == 1:
                last_x += 1
                self.tile_coordinates.append((last_x, last_y))
                last_y += 1
                self.tile_coordinates.append((last_x, last_y))

            if r == 2:
                last_x -= 1
                self.tile_coordinates.append((last_x, last_y))
                last_y += 1
                self.tile_coordinates.append((last_x, last_y))

            last_y += 1

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)

            for i in range(0, self.v_number):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        center_x = self.perspective_x
        spacing = self.width * self.v_spacing
        offset = index - 0.5
        line_x = int(offset * spacing + center_x) - self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.h_spacing * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_ship(self):
        center_x = self.width / 2
        base_y = self.SHIP_BASE * self.height
        half_ship_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_points[0] = (center_x - half_ship_width, base_y)
        self.ship_points[1] = (center_x, base_y + ship_height)
        self.ship_points[2] = (center_x + half_ship_width, base_y)

        x1, y1 = self.transform(*self.ship_points[0])
        x2, y2 = self.transform(*self.ship_points[1])
        x3, y3 = self.transform(*self.ship_points[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def update_tile(self):
        for i in range(0, self.num_tiles):
            tile = self.tiles[i]
            tile_points = self.tile_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_points[0], tile_points[1])
            xmax, ymax = self.get_tile_coordinates(tile_points[0] + 1, tile_points[1] + 1)

            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):

        start_index = -int(self.v_number / 2) + 1
        for i in range(start_index, start_index + self.v_number):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)

            for i in range(0, self.h_number):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):

        start_index = -int(self.v_number / 2) + 1
        end_index = start_index + self.v_number - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.h_number):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def on_touch_down(self, touch):
        if not self.GAME_OVER and self.game_start:
            if touch.x > self.width / 2:
                self.direction -= self.speed_x

            else:
                self.direction += self.speed_x

        return super(RelativeLayout, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.direction = 0

    def movingUpdate(self, dt):

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tile()
        self.update_ship()

        time_factor = dt * 60

        if not self.GAME_OVER and self.game_start:
            actual_speed = self.speed_y * self.height / 100
            self.current_offset_y += actual_speed * time_factor  # control forward or back

            spacing_y = self.h_spacing * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score = f" SCORE >> {self.current_y_loop}"

                self.tiles_coordinates()

            actual_side_speed = self.direction * self.width / 100
            self.current_offset_x += actual_side_speed * time_factor

        if not self.check_collision() and not self.GAME_OVER:
            self.GAME_OVER = True
            self.menu_widget.opacity = 1
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.menu_button_title = "RESTART"
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            Clock.schedule_once(self. game_over_sound, 3)

            print("GAME OVER")

    def game_over_sound(self, dt):
        if self.GAME_OVER:
            self.sound_gameover_voice.play()

    def button_click(self):
        if self.GAME_OVER:
            self.sound_restart.play()
        else:
            self.sound_start.play()
        self.sound_music1.play()
        self.game_start = True
        self.reset_game()
        self.menu_widget.opacity = 0


class GalaxyApp(App):
    pass


GalaxyApp().run()
