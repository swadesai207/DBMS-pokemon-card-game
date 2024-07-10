import pygame;

class Slider:
    def __init__(self, screen_width, screen_height, total_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.total_height = total_height
        self.slider_width = 20
        self.slider_color = (100, 100, 100)
        self.slider_height = min(screen_height, screen_height * screen_height // total_height)  # Limit slider height
        self.slider_pos = (screen_width - self.slider_width, 0)
        self.slider_handle_pos = 0
        self.slider_handle_height = 50  # Adjust handle height as needed
        self.slider_handle_color = (50, 50, 50)
        self.slider_dragging = False
        self.scroll_position = 0  # Initialize scroll position

    def update_slider(self):
        self.slider_height = min(self.screen_height, self.screen_height * self.screen_height // self.total_height)  # Limit slider height
        self.slider_pos = (self.screen_width - self.slider_width, -self.scroll_position * self.screen_height // self.total_height)

    def draw_slider(self, screen):
        pygame.draw.rect(screen, self.slider_color, pygame.Rect(self.slider_pos, (self.slider_width, self.screen_height)))
        pygame.draw.rect(screen, self.slider_handle_color, pygame.Rect(self.slider_pos[0], self.slider_pos[1] + self.slider_handle_pos,
                                                                      self.slider_width, self.slider_handle_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.slider_pos[0] <= mouse_x <= self.slider_pos[0] + self.slider_width and \
                        self.slider_pos[1] <= mouse_y <= self.slider_pos[1] + self.slider_height:
                    self.slider_dragging = True
                    self.slider_handle_pos = mouse_y - self.slider_pos[1] - (self.slider_handle_height // 2)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.slider_dragging = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.slider_handle_pos -= 10  # Adjust the step size as needed
                self.slider_handle_pos = max(0, self.slider_handle_pos)  # Ensure handle doesn't go above track
            elif event.button == 5:  # Scroll down
                self.slider_handle_pos += 10  # Adjust the step size as needed
                self.slider_handle_pos = min(self.slider_height - self.slider_handle_height, self.slider_handle_pos)  # Ensure handle doesn't go below track
                
        # Adjust scroll position based on slider handle position
        max_scroll = max(0, self.total_height - self.screen_height)
        self.scroll_position = self.slider_handle_pos * max_scroll // (self.slider_height - self.slider_handle_height)