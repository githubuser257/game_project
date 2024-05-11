import pygame
import game

class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self):
        self.state = self.camera_func(self.state, game.player.rect)

    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + game.screen_width / 2, -t + game.screen_height / 2

        l = min(0, l)
        l = max(-(camera.width - game.screen_width), l)
        t = max(-(camera.height - game.screen_height), t)
        t = min(0, t)

        return pygame.Rect(l, t, w, h)
