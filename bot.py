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
