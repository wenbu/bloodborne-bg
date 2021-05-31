from game import Game


def play():
    game = Game(1)
    while not game.is_game_over():
        game.round()
    print('Game over.')


if __name__ == '__main__':
    play()
