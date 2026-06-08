import pygame
import pygame.freetype


class Window:

    def __init__(self,env):
        self.env = env
        self.text_area_scale = 0.4375

        pygame.init()
        pygame.display.init()

        self.window_height = self.env.screen_size
        self.text_area_width = self.env.screen_size * self.text_area_scale
        self.window_width = self.env.screen_size + self.text_area_width

        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption("mabtpg: gridworld")
        self.clock = pygame.time.Clock()

    def render(self, img):

        # draw img
        img_surface = pygame.surfarray.make_surface(img)

        img_size = img_surface.get_size()[0]
        img_text_area_size = img_size * self.text_area_scale

        bg = pygame.Surface((img_text_area_size + img_size, img_size))
        bg.convert()
        bg.fill((255, 255, 255))

        bg.blit(img_surface, (img_text_area_size, 0))

        bg = pygame.transform.smoothscale(bg, (self.window_width, self.window_height))

        # create text area
        font_size = 22
        font = pygame.freetype.SysFont(pygame.font.get_default_font(), font_size)

        def draw_text_lines(text_lines):
            num_lines = len(text_lines)
            line_height = self.window_height // (num_lines + 1)
            y_offset = (self.window_height - line_height * num_lines) // 2

            for i, line in enumerate(text_lines):
                text_rect = font.get_rect(line, size=font_size)
                text_rect.centerx = self.text_area_width // 2
                text_rect.y = y_offset + i * line_height
                font.render_to(bg, text_rect, line, size=font_size, fgcolor=(0, 0, 0))

        # 文本内容
        text_lines = [
            f"Mission: {self.env}",
            f"Grid Size: {self.env.width}",
            f"Agent Position: ({self.env.agents[0].position[0]},{self.env.agents[0].position[1]})"
        ]

        # 绘制文本
        draw_text_lines(text_lines)

        self.window.blit(bg, (0, 0))
        pygame.event.pump()
        self.clock.tick(self.env.metadata["render_fps"])
        pygame.display.flip()

