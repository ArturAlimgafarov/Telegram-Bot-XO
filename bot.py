from telebot import types
import telebot
import sys

token = ''
bot = telebot.TeleBot(token)

board = [
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['_', '_', '_']
]

ai_char = 'O'
user_char = 'X'
ai_turn = True
user_turn = False
scores = {
    user_char: -1,
    ai_char: 1,
    'draw': 0
}

def is_draw(field):
    count = 0
    for y in range(3):
        count += 1 if '_' in field[y] else 0
    return count == 0
def is_win(char, field):
    opponent_char = 'X' if char == 'O' else 'O'
    for y in range(3):
        if opponent_char not in field[y] and '_' not in field[y]:
            return True
    for x in range(3):
        col = [field[0][x], field[1][x], field[2][x]]
        if opponent_char not in col and '_' not in col:
            return True
    diagonal = [field[0][0], field[1][1], field[2][2]]
    if opponent_char not in diagonal and '_' not in diagonal:
        return True
    diagonal = [field[0][2], field[1][1], field[2][0]]
    if opponent_char not in diagonal and '_' not in diagonal:
        return True
    return False

def minimax(board, depth, is_ai_turn):
    if is_win(ai_char, board):
        return scores[ai_char]
    if is_win(user_char, board):
        return scores[user_char]
    if is_draw(board):
        return scores['draw']
    if is_ai_turn:
        best_score = - sys.maxsize
        for y in range(3):
            for x in range(3):
                if board[y][x] == '_':
                    board[y][x] = ai_char
                    score = minimax(board, depth + 1, user_turn)
                    board[y][x] = '_'
                    best_score = max(best_score, score)
    else:
        best_score = sys.maxsize
        for y in range(3):
            for x in range(3):
                if board[y][x] == '_':
                    board[y][x] = user_char
                    score = minimax(board, depth + 1, ai_turn)
                    board[y][x] = '_'
                    best_score = min(best_score, score)
    return best_score
def get_computer_position(field):
    move = None
    best_score = -sys.maxsize
    board = [field[y].copy() for y in range(3)]
    for y in range(3):
        for x in range(3):
            if board[y][x] == '_':
                board[y][x] = ai_char
                score = minimax(board, 0, user_turn)
                board[y][x] = '_'
                if score > best_score:
                    best_score = score
                    move = (y, x)
    return move

def update_board():
    global board
    board = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']
    ]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id,
                     text=f'Welcome, {message.from_user.username} 🎉\n'
                          f'Click on 👉🏻 /play to starting the game ⚔️')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id,
                     text='1. The game is played on a grid that\'s 3 squares by 3 squares.\n\n'
                          '2. You are ❌, your opponent (BOT) is ⭕️. Players take turns '
                          'putting their marks in empty squares.\n\n'
                          '3. The first player to get 3 of her marks in a row (up, down, across, '
                          'or diagonally) is the winner.\n\n'
                          '4. When all 9 squares are full, the game is over. If no player has 3 '
                          'marks in a row, the game ends in a tie.')

@bot.message_handler(commands=['play'])
def play(message):
    update_board()
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(3):
        for j in range(3):
            btn = types.InlineKeyboardButton(text=str(board[i][j]),
                                             callback_data=(str(i) + str(j)))
            buttons.append(btn)
    markup.add(*buttons)
    bot.send_message(chat_id=message.chat.id,
                     text=f'YOU: ❌\nBOT: ⭕️',
                     reply_markup=markup)