import pygame
import sys

pygame.init()

WIDTH = 900
HEIGHT = 600
TOOLBAR_HEIGHT = 50
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App - Student Project")
clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, w, h, text, color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.selected = False
    
    def draw(self, surface):
        color = self.color
        if self.selected:
            color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
        
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        font = pygame.font.SysFont("Arial", 16)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class PaintApp:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        
        self.drawing = False
        self.start_pos = None
        self.last_pos = None
        self.tool = "pen"
        self.color = BLACK
        
        self.canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
        self.canvas.fill(WHITE)
        
        self.create_buttons()
        self.running = True
    
    def create_buttons(self):
        btn_w = 60
        btn_h = 35
        y = CANVAS_HEIGHT + 8
        x = 10
        
        self.color_buttons = [
            Button(x, y, btn_w, btn_h, "Black", BLACK, WHITE),
            Button(x + btn_w + 5, y, btn_w, btn_h, "Red", RED),
            Button(x + (btn_w + 5) * 2, y, btn_w, btn_h, "Green", GREEN),
            Button(x + (btn_w + 5) * 3, y, btn_w, btn_h, "Blue", BLUE),
            Button(x + (btn_w + 5) * 4, y, btn_w, btn_h, "Yellow", YELLOW),
        ]
        
        tool_x = x + (btn_w + 5) * 5 + 20
        self.tool_buttons = [
            Button(tool_x, y, btn_w, btn_h, "Pen", GRAY),
            Button(tool_x + btn_w + 5, y, btn_w, btn_h, "Rect", GRAY),
            Button(tool_x + (btn_w + 5) * 2, y, btn_w, btn_h, "Circle", GRAY),
            Button(tool_x + (btn_w + 5) * 3, y, btn_w, btn_h, "Eraser", GRAY),
        ]
        
        self.clear_btn = Button(WIDTH - 70, y, 60, btn_h, "Clear", RED, WHITE)
        self.tool_buttons[0].selected = True
    
    def draw_toolbar(self):
        pygame.draw.rect(self.screen, GRAY, (0, CANVAS_HEIGHT, WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(self.screen, BLACK, (0, CANVAS_HEIGHT), (WIDTH, CANVAS_HEIGHT), 3)
        
        for btn in self.color_buttons:
            btn.draw(self.screen)
        for btn in self.tool_buttons:
            btn.draw(self.screen)
        self.clear_btn.draw(self.screen)
        
        font = pygame.font.SysFont("Arial", 16)
        info_bg = pygame.Rect(WIDTH - 200, CANVAS_HEIGHT + 5, 190, 40)
        pygame.draw.rect(self.screen, DARK_GRAY, info_bg)
        pygame.draw.rect(self.screen, BLACK, info_bg, 2)
        
        tool_text = font.render(f"Tool: {self.tool}", True, WHITE)
        color_text = font.render(f"Color: {self.get_color_name()}", True, self.color)
        
        self.screen.blit(tool_text, (WIDTH - 195, CANVAS_HEIGHT + 10))
        self.screen.blit(color_text, (WIDTH - 195, CANVAS_HEIGHT + 28))
    
    def get_color_name(self):
        colors = {BLACK: "Black", RED: "Red", GREEN: "Green", BLUE: "Blue", YELLOW: "Yellow"}
        return colors.get(self.color, "Color")
    
    def draw_on_canvas(self, pos):
        if self.tool == "pen":
            pygame.draw.circle(self.canvas, self.color, pos, 5)
        elif self.tool == "eraser":
            pygame.draw.circle(self.canvas, WHITE, pos, 10)
    
    def draw_line(self, start, end):
        if self.tool == "pen":
            pygame.draw.line(self.canvas, self.color, start, end, 10)
        elif self.tool == "eraser":
            pygame.draw.line(self.canvas, WHITE, start, end, 20)
    
    def draw_shape(self, start, end):
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        
        if self.tool == "rect":
            pygame.draw.rect(self.canvas, self.color, rect, 3)
        elif self.tool == "circle":
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            pygame.draw.circle(self.canvas, self.color, start, radius, 3)
    
    def draw_shape_preview(self, start, end):
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        
        if self.tool == "rect":
            pygame.draw.rect(self.screen, self.color, rect, 3)
        elif self.tool == "circle":
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            pygame.draw.circle(self.screen, self.color, start, radius, 3)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                
                for btn in self.color_buttons:
                    if btn.check_click(pos):
                        color_map = {"Black": BLACK, "Red": RED, "Green": GREEN,
                                    "Blue": BLUE, "Yellow": YELLOW}
                        self.color = color_map.get(btn.text, BLACK)
                
                for i, btn in enumerate(self.tool_buttons):
                    if btn.check_click(pos):
                        for b in self.tool_buttons:
                            b.selected = False
                        btn.selected = True
                        tools = ["pen", "rect", "circle", "eraser"]
                        self.tool = tools[i]
                
                if self.clear_btn.check_click(pos):
                    self.canvas.fill(WHITE)
                
                if pos[1] < CANVAS_HEIGHT:
                    self.drawing = True
                    self.start_pos = pos
                    self.last_pos = pos
                    if self.tool not in ["rect", "circle"]:
                        self.draw_on_canvas(pos)
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.drawing and self.start_pos:
                    if self.tool in ["rect", "circle"]:
                        self.draw_shape(self.start_pos, event.pos)
                self.drawing = False
                self.start_pos = None
                self.last_pos = None
            
            elif event.type == pygame.MOUSEMOTION and self.drawing:
                pos = event.pos
                if pos[1] < CANVAS_HEIGHT:
                    if self.tool in ["rect", "circle"]:
                        pass
                    else:
                        if self.last_pos:
                            self.draw_line(self.last_pos, pos)
                        self.draw_on_canvas(pos)
                        self.last_pos = pos
    
    def draw(self):
        self.screen.blit(self.canvas, (0, 0))
        
        if self.drawing and self.start_pos and self.tool in ["rect", "circle"]:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < CANVAS_HEIGHT:
                self.draw_shape_preview(self.start_pos, mouse_pos)
        
        self.draw_toolbar()
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = PaintApp()
    app.run()