        
def show_game_over_screen(self):
    font = pg.font.Font(FontConstants.FONT_NAME, FontConstants.FONT_SIZE * 2)
    game_over_text = font.render("Game Over", True, TextConstants.TEXT_COLOR)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    restart_button = self.entity_manager.get_entity('Static').get_component(RestartButtonComponent)
    restart_button.show()