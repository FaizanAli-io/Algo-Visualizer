import os
import pygame
import random

from config import (
    Font as F,
    Color as C,
    SCREEN_WIDTH,
)


def format_number(number):
    """Format numbers longer than 6 digits in exponential form."""
    return f"{number:.4e}" if len(str(number)) > 6 else str(number)


def karatsuba_visual(x, y, steps):
    """Recursive Karatsuba multiplication with visualization steps."""
    if x < 10 or y < 10:
        steps.append(f"Base case: {x} * {y} = {format_number(x * y)}")
        return x * y

    half_n = max(len(str(x)), len(str(y))) // 2

    a, b = divmod(x, 10**half_n)
    c, d = divmod(y, 10**half_n)

    steps.append(
        f"Split: {format_number(x)} -> ({format_number(a)}, {format_number(b)}), "
        f"{format_number(y)} -> ({format_number(c)}, {format_number(d)})"
    )

    ac = karatsuba_visual(a, c, steps)
    bd = karatsuba_visual(b, d, steps)

    ad_plus_bc = karatsuba_visual(a + b, c + d, steps) - ac - bd

    result = ac * 10 ** (2 * half_n) + ad_plus_bc * 10**half_n + bd
    steps.append(
        f"Combine: {format_number(ac)} * 10^{2 * half_n} + "
        f"{format_number(ad_plus_bc)} * 10^{half_n} + {format_number(bd)} = {format_number(result)}"
    )
    return result


class MultiplyScreen:
    def __init__(self, screen, filename):
        self.screen = screen
        self.pair = self.load_random_pair(filename)
        self.steps = []
        self.current_step = 0
        self.input_active = False
        self.step_input = ""

    def load_random_pair(self, filename):
        """Load a random pair of numbers from the given file."""
        file_path = os.path.join("src", "inputs", "integer_mult", f"{filename}.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()
        if not lines:
            raise ValueError("The file is empty.")
        return random.choice(lines).strip().split(", ")

    def draw_text(self, text, font, color, position):
        """Helper to draw text on the screen."""
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def handle_events(self, total_steps):
        """Handle user input and update the current step or input state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    self.handle_step_input(event, total_steps)
                else:
                    self.handle_navigation(event, total_steps)
        return True

    def handle_navigation(self, event, total_steps):
        """Handle navigation between steps or activate step input."""
        if event.key == pygame.K_RIGHT:
            self.current_step = min(self.current_step + 1, total_steps - 1)
        elif event.key == pygame.K_LEFT:
            self.current_step = max(self.current_step - 1, 0)
        elif event.key == pygame.K_j:  # Activate input for step jump
            self.input_active = True

    def handle_step_input(self, event, total_steps):
        """Handle input for jumping to a specific step."""
        if event.key == pygame.K_RETURN:
            if self.step_input.isdigit():
                step = int(self.step_input) - 1
                self.current_step = max(0, min(step, total_steps - 1))
            self.step_input = ""
            self.input_active = False
        elif event.key == pygame.K_BACKSPACE:
            self.step_input = self.step_input[:-1]
        else:
            self.step_input += event.unicode

    def display_original_numbers(self, int1, int2):
        """Display the two original numbers at the top."""
        formatted_int1 = format_number(int1)
        formatted_int2 = format_number(int2)
        self.draw_text(f"Number 1: {formatted_int1}", F.FONT_MEDIUM, C.YELLOW, (50, 30))
        self.draw_text(f"Number 2: {formatted_int2}", F.FONT_MEDIUM, C.YELLOW, (50, 80))

    def display_final_result(self, result):
        """Display the final result below the numbers."""
        formatted_result = format_number(result)
        self.draw_text(
            f"Final Result: {formatted_result}", F.FONT_MEDIUM, C.GREEN, (50, 130)
        )

    def display_steps(self):
        """Display the list of previous steps and highlight the current step."""
        start_idx = max(0, self.current_step - 4)
        step_colors = [C.LIGHT_GRAY, C.BLUE, C.GREEN, C.RED]

        for i, step_idx in enumerate(range(start_idx, self.current_step)):
            y_pos = 200 + i * 70
            color = step_colors[i % len(step_colors)]
            step_text = f"{step_idx + 1}. {self.steps[step_idx]}"
            self.draw_text(step_text, F.FONT_SMALL, color, (50, y_pos))

        current_text = f"{self.current_step + 1}. {self.steps[self.current_step]}"
        self.draw_text(current_text, F.FONT_LARGE, C.ORANGE, (50, 500))

    def display_step_counter(self, total_steps):
        """Display the current step counter."""
        rect = pygame.Rect(SCREEN_WIDTH - 380, 20, 320, 60)
        pygame.draw.rect(self.screen, C.BLACK, rect, 0, 15)

        step_counter_text = f"Step {self.current_step + 1} of {total_steps}"
        self.draw_text(
            step_counter_text, F.FONT_MEDIUM, C.WHITE, (SCREEN_WIDTH - 370, 30)
        )

    def display_step_input(self):
        """Display the step input field if active."""
        if self.input_active:
            rect = pygame.Rect(SCREEN_WIDTH - 380, 100, 320, 60)
            pygame.draw.rect(self.screen, C.BLACK, rect, 0, 15)

            input_text = f"Jump to step: {self.step_input}"
            self.draw_text(input_text, F.FONT_MEDIUM, C.CYAN, (SCREEN_WIDTH - 370, 110))

    def visualize(self):
        """Main loop to run the visualization."""
        if not self.pair:
            print("No valid pair to display.")
            return

        running = True
        int1, int2 = map(int, self.pair)

        # Perform Karatsuba and log steps
        final_result = karatsuba_visual(int1, int2, self.steps)
        total_steps = len(self.steps)

        while running:
            self.screen.fill(C.BG_COLOR)
            running = self.handle_events(total_steps)

            self.display_original_numbers(int1, int2)

            # Display the final result if at the last step
            if self.current_step == total_steps - 1:
                self.display_final_result(final_result)

            self.display_steps()
            self.display_step_counter(total_steps)
            self.display_step_input()

            pygame.display.flip()

        pygame.quit()
