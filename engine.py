class GameState():
    def __init__(self):
        self.board = [
            ['RB', 'NB', 'BB', 'QB', 'KB', 'BB', 'NB', 'RB'],
            ['PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['PW', 'PW', 'PW', 'PW', 'PW', 'PW', 'PW', 'PW'],
            ['RW', 'NW', 'BW', 'QW', 'KW', 'BW', 'NW', 'RW'],
        ];
        self.whiteToMove = True
        self.moveLog = []
