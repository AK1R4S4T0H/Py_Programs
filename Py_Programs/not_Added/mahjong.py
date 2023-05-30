# JOINT EFFORT WITH ME AND CHATGPT
# WHY NOT LEVERAGE AI TO BUILD AI
# NOT COMPLETE
import pygame
import random
from collections import deque
import math
import matplotlib.pyplot as plt

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Mahjong")

# Game Logic
def generate_tiles():
    # Generate and return a list of shuffled tiles
    tiles = []
    for _ in range(4):
        for i in range(1, 10):
            tiles.append(i)
    random.shuffle(tiles)
    return tiles

def is_valid_move(tile1, tile2):
    # Check if the two selected tiles can be removed

    # Check if the tiles are the same
    if tile1 == tile2:
        return False

    # Check if the tiles belong to the same suit (e.g., same color or symbol)
    if tile1 % 2 != tile2 % 2:
        return False

    # Check if the tiles are adjacent numbers
    if abs(tile1 - tile2) == 1:
        return True

    # Add more custom logic based on your Mahjong game rules
    # ...

    return False


def remove_tiles(tiles, tile1, tile2):
    # Remove the two selected tiles from the list
    tiles.remove(tile1)
    tiles.remove(tile2)

def ai_select_tiles(tiles):
    # AI selects two tiles to remove
    valid_pairs = []

    # Find all valid pairs of tiles
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if is_valid_move(tiles[i], tiles[j]):
                valid_pairs.append((tiles[i], tiles[j]))

    # Select a random pair from the valid pairs
    if valid_pairs:
        return random.choice(valid_pairs)
    else:
        return None, None

# Mahjong Agent
class MahjongAgent:
    def __init__(self, replay_buffer_size=10000, num_iterations=1000):
        self.replay_buffer = deque(maxlen=replay_buffer_size)
        self.num_iterations = num_iterations

    def play(self, tiles):
        # Perform self-play to generate game trajectories
        game_trajectories = self.self_play(tiles)

        # Store game trajectories in replay buffer
        self.replay_buffer.extend(game_trajectories)

        # Train neural network using replay buffer
        # train_neural_network(self.replay_buffer)  # Uncomment this line if you have the training logic

        # Select tiles based on AI's policy
        tile1, tile2 = ai_select_tiles(tiles)

        # Get the reward for the move
        reward = self.get_reward(tiles)

        # Update the reward history
        reward_history.append(reward)

        return tile1, tile2, reward

    def self_play(self, tiles):
        game_trajectories = []

        for _ in range(self.num_iterations):
            # Perform Monte Carlo Tree Search to generate game trajectory
            trajectory = self.monte_carlo_tree_search(tiles)
            game_trajectories.append(trajectory)

        return game_trajectories

    def monte_carlo_tree_search(self, tiles):
        # Initialize game trajectory
        trajectory = []

        # Perform Monte Carlo Tree Search for a single episode
        game_over = False

        while not game_over:
            # Select action based on MCTS algorithm
            action = self.select_action(tiles)

            # Apply action to update game state
            new_tiles = self.apply_action(tiles, action)

            # Evaluate new state using neural network
            value = evaluate_state(new_tiles)

            # Append state and value to game trajectory
            trajectory.append((new_tiles, value))

            # Update current state
            tiles = new_tiles

            # Update the game_over condition based on your game rules
            game_over = self.is_game_over(tiles)

        return trajectory

    def select_action(self, tiles):
        # Implement selection of action based on MCTS algorithm
        # You can use the UCB1 algorithm for action selection in MCTS

        # Define the exploration constant
        exploration_constant = 1.0

        # Perform multiple simulations to estimate action values
        action_values = {}  # Dictionary to store action values
        total_visits = 0  # Total number of visits to actions

        for _ in range(self.num_iterations):
            # Perform a simulation to estimate action values
            tiles, action = self.perform_simulation(tiles)

            # Convert the action list to a tuple
            action = tuple(action)

            # Update action values and visit count
            if action in action_values:
                action_values[action] += 1
            else:
                action_values[action] = 1

            total_visits += 1

        # Calculate UCB1 values for each action
        ucb1_values = {}
        for action, visits in action_values.items():
            action_value = visits / total_visits
            exploration_term = exploration_constant * math.sqrt(math.log(total_visits) / visits)
            ucb1_values[action] = action_value + exploration_term

        # Select the action with the highest UCB1 value
        action = max(ucb1_values, key=ucb1_values.get)

        return action

    def perform_simulation(self, tiles):
        # Implement a single simulation step to estimate action values
        # You can use any strategy or heuristics for the simulation

        # Here's an updated version that handles the case where no valid action is available:
        while not self.is_game_over(tiles):
            # Select a random valid action
            valid_pairs = []

            for i in range(len(tiles)):
                for j in range(i + 1, len(tiles)):
                    if is_valid_move(tiles[i], tiles[j]):
                        valid_pairs.append((tiles[i], tiles[j]))

            if valid_pairs:
                action = random.choice(valid_pairs)
            else:
                action = None  # No valid action available
                break

            # Apply the selected action to the game state
            tiles = self.apply_action(tiles, action)

        # Return the final game state and the last action as a tuple
        return tiles, action


    def apply_action(self, tiles, action):
        # Implement applying the selected action to the game state
        # In Mahjong, the action typically involves removing two tiles from the board
        # Update the game state accordingly and return the updated state

        new_tiles = tiles.copy()
        tile1, tile2 = action

        # Remove the selected tiles from the board
        new_tiles.remove(tile1)
        new_tiles.remove(tile2)

        return new_tiles
        
    def is_game_over(self, tiles):
        # Check if the game is over based on the current game state
        # Implement the game-over conditions specific to Mahjong

        # Here's a simple example assuming the game is over when there are no more valid moves:
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if is_valid_move(tiles[i], tiles[j]):
                    return False

        return True

# Main game loop
def game_loop():
    tiles = generate_tiles()

    # Create an instance of the MahjongAgent class
    agent = MahjongAgent()

    # Deque to store the game state for training the agent
    game_states = deque(maxlen=10000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if the game is over
        if len(tiles) == 0:
            print("Game over!")
            running = False
            break

        # AI selects two tiles to remove
        tile1, tile2, reward = agent.play(tiles)

        # Remove the selected tiles
        if tile1 is not None and tile2 is not None:
            remove_tiles(tiles, tile1, tile2)

        # Append the game state to the deque
        game_states.append(tiles.copy())

        # Render the game
        screen.fill((255, 255, 255))
        render_tiles(tiles)
        pygame.display.update()

        # Limit the frame rate
        pygame.time.Clock().tick(60)

    # Plot the reward history
    plt.plot(reward_history)
    plt.xlabel('Iterations')
    plt.ylabel('Reward')
    plt.title('Reward History')
    plt.show()

    pygame.quit()

# Run the game loop
game_loop()
