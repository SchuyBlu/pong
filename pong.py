"""-------------------------------------------------
Author: Schuyler Kelly
Date: 12/07/2021
Edited: 12/07/2021
Purpose:
    Play a game of pong.
-------------------------------------------------"""
import pygame
import utils.colors as color
import config as c

pygame.init()

def update_screen(screen: pygame.Surface,
                  player1: pygame.Rect, 
                  player2: pygame.Rect, 
                  ball: pygame.Rect,
                  player1_score: int,
                  player2_score: int):
    """Updates the screen.
    
    Args:
        screen: The main surface of the game.
    """
    # Draw the player and the ball.
    screen.fill(color.DEEP_GREY)

    # Render and draw the name of the game.
    name_text = c.NAME_FONT.render("Pong!", False, color.GREY)
    screen.blit(name_text, (c.WIDTH//2 - name_text.get_width()//2, (c.UPPER_LIMIT - name_text.get_height())//2))

    # Draw player 1's score in.
    score1 = c.SCORE_FONT.render(f"P1: {player1_score}", False, color.GREY)
    screen.blit(score1, (25, (c.UPPER_LIMIT - score1.get_height())//2))

    # Draw player 2's score in.
    score2 = c.SCORE_FONT.render(f"P2: {player2_score}", False, color.GREY)
    screen.blit(score2, (c.WIDTH - score2.get_width() - 25, (c.UPPER_LIMIT - score2.get_height())//2))
    pygame.draw.rect(screen, color.GREY, player1)
    pygame.draw.rect(screen, color.GREY, player2)
    pygame.draw.ellipse(screen, color.GREY, ball)
    pygame.draw.aaline(screen, color.GREY, (c.WIDTH//2, c.UPPER_LIMIT), (c.WIDTH//2, c.HEIGHT))
    pygame.draw.aaline(screen, color.GREY, (0, c.UPPER_LIMIT), (c.WIDTH, c.UPPER_LIMIT))


def bounce_direction(ball: pygame.Rect):
    """Change the ball direction so it can bounce around. 
    
    Args:
        ball: The Rect object representing the ball.
    """
    # Deal with the bottom and top of the screen.
    if ball.bottom >= c.HEIGHT or ball.top <= c.UPPER_LIMIT:
        c.BALL_VEL_Y *= -1

        # In cases where the ball hits the bottom and top,
        # the scored sound effect can be reset.
        c.PLAY_SCORED = True
    
    # Deal with when the ball hits the left side.
    if ball.left <= 0:
        c.BALL_VEL_X *= -1
        pygame.event.post(pygame.event.Event(c.P2_POINT))

    # Deal with when the ball hits the right side.
    if ball.right >= c.WIDTH:
        c.BALL_VEL_X *= -1
        pygame.event.post(pygame.event.Event(c.P1_POINT))


def handle_player1(player1: pygame.Rect, keys_pressed: list):
    """Handle the movement of player 1.
    
    Args:
        player1: The rect object representing player 1.
        keys_pressed: A list of keys pressed.
    """
    # If both keys are pressed, do nothing.
    if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]:
        return
    
    # If top key is pressed, move up. Add 15 to the condition checking
    # if it has hit the upper boundary in order to make sure it will never
    # hit the upper line.
    if keys_pressed[pygame.K_w] and player1.top > c.UPPER_LIMIT + 15:
        player1.y -= c.MOVEMENT

    if keys_pressed[pygame.K_s] and player1.bottom < c.HEIGHT - 15:
        player1.y += c.MOVEMENT
    

def handle_player2(player2: pygame.Rect, keys_pressed: list):
    """Handle the movement of player 2.
    
    Args:
        player2: Rect object representing player 2.
        keys_pressed: List of keys pressed.
    """
    # Handle if both keys are pressed.
    if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_DOWN]:
        return

    # Handle moving up.
    if keys_pressed[pygame.K_UP] and player2.top > c.UPPER_LIMIT + 15:
        player2.y -= c.MOVEMENT

    # Handle moving down.
    if keys_pressed[pygame.K_DOWN] and player2.bottom < c.HEIGHT - 15:
        player2.y += c.MOVEMENT


def handle_collisions(player1: pygame.Rect, player2: pygame.Rect, ball: pygame.Rect, ball_count: int):
    """Handle collisions between the ball and players.
    
    Args:
        player1: Rect object representing player 1.
        player2: Rect object representing player 2.
        ball: Rect object representing the ball.
        ball_count: Allows the ball to speed up.
    """
    # Deal with the ball colliding with player 1.
    if ball.colliderect(player1):

        # Deal with all possible sounds when reflecting.
        # First check the boolean to see if it has been played.
        # Reset the right bool.
        c.PLAY_RIGHT_BLIP = True
        play_left_blip(ball_count)
        
        # Reflect the ball.
        c.BALL_VEL_X *= -1

        # Increase the ball count, and increase speed if allowed.
        ball_count += 1
        if ball_count % 2 == 0:
            c.BALL_VEL_X += 1
            if c.BALL_VEL_Y > 0:
                c.BALL_VEL_Y += 1
            else:
                c.BALL_VEL_Y -= 1
    
    if ball.colliderect(player2):
        
        # Deal with sound effects.
        c.PLAY_LEFT_BLIP = True
        play_right_blip(ball_count)

        # Do the same as the collision on the left.
        c.BALL_VEL_X *= -1

        # Also increase the ball count here. Increase speed if allowed.
        ball_count += 1
        if ball_count % 2 == 0:
            c.BALL_VEL_X += 1
            if c.BALL_VEL_Y > 0:
                c.BALL_VEL_Y += 1
            else:
                c.BALL_VEL_Y -= 1

    # Return the ball count.
    return ball_count


def play_right_blip(ball_count: int):
    """Play the right blip if necessaary.
    
    Args:
        ball_count: Number representing the ball count.
    """
    # Deal with all cases when different blips can play.
    if ball_count < 2 and c.PLAY_RIGHT_BLIP:
        pygame.mixer.Sound.play(c.BLIP1)
        c.PLAY_RIGHT_BLIP = False
    if 2 <= ball_count < 4 and c.PLAY_RIGHT_BLIP:
        pygame.mixer.Sound.play(c.BLIP2)
        c.PLAY_RIGHT_BLIP = False
    if 4 <= ball_count < 6 and c.PLAY_RIGHT_BLIP:
        pygame.mixer.Sound.play(c.BLIP3)
        c.PLAY_RIGHT_BLIP = False
    if ball_count >= 6 and c.PLAY_RIGHT_BLIP:
        pygame.mixer.Sound.play(c.BLIP4)
        c.PLAY_RIGHT_BLIP = False


def play_left_blip(ball_count: int):
    """Plays the left blip if necessary.
    
    Args:
        ball_count: Number representing the ball count.
    """
    # Deal with all cases when different blips can
    # play.
    if ball_count < 2 and c.PLAY_LEFT_BLIP:
        pygame.mixer.Sound.play(c.BLIP1)
        c.PLAY_LEFT_BLIP = False
    if 2 <= ball_count <= 4 and c.PLAY_LEFT_BLIP:
        pygame.mixer.Sound.play(c.BLIP2)
        c.PLAY_LEFT_BLIP = False
    if 4 <= ball_count < 6 and c.PLAY_LEFT_BLIP:
        pygame.mixer.Sound.play(c.BLIP3)
        c.PLAY_LEFT_BLIP = False
    if ball_count >= 6 and c.PLAY_LEFT_BLIP:
        pygame.mixer.Sound.play(c.BLIP4)
        c.PLAY_LEFT_BLIP = False

        
def check_if_winner(player1_score: int, player2_score: int):
    """Checks if there is a winner.
    
    Args:
        player1_score: Player 1's score.
        player2_score: Player 2's score.
    
    Returns:
        A string showing the winner, or None.
    """
    # If either player's score is 20, display a winner.
    if player1_score == 15:
        return "Winner: Player 1"
    if player2_score == 15:
        return "Winner: Player 2"


def display_winner(screen: pygame.Surface, text: str):
    """Displays the winner if one is found.
    
    Args:
        screen: The main surface for the game.
        text: The text to be displayed.
    """
    # Render and display the text.
    winner_text = c.WINNER_FONT.render(text, False, color.WHITE)
    screen.blit(winner_text, (c.WIDTH//2 - winner_text.get_width()//2, c.HEIGHT//2 - winner_text.get_height()//2))


def main():
    """Run the main game loop."""

    # Create the game window.
    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    pygame.display.set_caption("Pong!")

    # Create the clock.
    clock = pygame.time.Clock()

    # Set the scores.
    player1_score = 0
    player2_score = 0
    
    # Create the ball and players.
    ball = pygame.Rect(c.WIDTH//2 - 5, (c.HEIGHT + c.UPPER_LIMIT)//2 - 10, 20, 20)
    player1 = pygame.Rect(3, (c.HEIGHT + c.UPPER_LIMIT)//2 - c.PLAYER_H//2, c.PLAYER_W, c.PLAYER_H)
    player2 = pygame.Rect(c.WIDTH - 3 - c.PLAYER_W, (c.HEIGHT + c.UPPER_LIMIT)//2 - c.PLAYER_H//2, c.PLAYER_W, c.PLAYER_H)

    # Create a ball count that will allow the ball to 
    # speed up.
    ball_count = 0

    # Create the game loop.
    running = True
    while running:
        # Handle the FPS.
        clock.tick(c.FPS)

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # In the event of scoring a point, add the point
            # and reset the ball speed.
            if event.type == c.P1_POINT:

                # Play the scoring sound effect.
                if c.PLAY_SCORED:
                    pygame.mixer.Sound.play(c.SCORED)
                    c.PLAY_SCORED = False

                player1_score += 1
                c.BALL_VEL_X = -1 * c.BALL_VEL_DEFAULT
                if c.BALL_VEL_Y > 0:
                    c.BALL_VEL_Y = c.BALL_VEL_DEFAULT
                else:
                    c.BALL_VEL_Y = -1 * c.BALL_VEL_DEFAULT
                ball_count = 0

                # Reset the sound effects for volleying.
                c.PLAY_LEFT_BLIP, c.PLAY_RIGHT_BLIP = True, True

            # In the event of scoring a point, add the point
            # and reset the ball speed.
            if event.type == c.P2_POINT:

                # Play the sound effect.
                if c.PLAY_SCORED:
                    pygame.mixer.Sound.play(c.SCORED)
                    c.PLAY_SCORED = False

                player2_score += 1
                c.BALL_VEL_X = c.BALL_VEL_DEFAULT
                if c.BALL_VEL_Y > 0:
                    c.BALL_VEL_Y = c.BALL_VEL_DEFAULT
                else:
                    c.BALL_VEL_Y = -1 * c.BALL_VEL_DEFAULT
                ball_count = 0

                # Reset the sound effects for volleying.
                c.PLAY_LEFT_BLIP, c.PLAY_RIGHT_BLIP = True, True

        # Move the ball.
        ball.x += c.BALL_VEL_X
        ball.y += c.BALL_VEL_Y

        # Show the winner if game is over.
        possible_winner = check_if_winner(player1_score, player2_score)
        if possible_winner is not None:

            # Update the display so it shows proper final scores.
            update_screen(screen, player1, player2, ball, player1_score, player2_score)

            # Update to display the winner.
            display_winner(screen, possible_winner)
            pygame.display.flip()

            # Play the sound effect.
            pygame.mixer.Sound.play(c.WINNER)

            # Wait five seconds.
            pygame.time.delay(5000)

            # Reset the game.
            player1_score = 0
            player2_score = 0
            ball = pygame.Rect(c.WIDTH//2 - 5, (c.HEIGHT + c.UPPER_LIMIT)//2 - 10, 20, 20)

        # Move the ball.
        bounce_direction(ball)

        # Get all the pressed keys.
        keys_pressed = pygame.key.get_pressed()

        # Handle player movement.
        handle_player1(player1, keys_pressed)
        handle_player2(player2, keys_pressed)

        # Handle ball collisions with the player, and increase speeed.
        ball_count = handle_collisions(player1, player2, ball, ball_count)

        # Update the screen.
        update_screen(screen, player1, player2, ball, player1_score, player2_score)
        
        # Update the screen.
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()