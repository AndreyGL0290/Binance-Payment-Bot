from aiogram.filters.state import StatesGroup, State
from aiogram import Router

# Environmental variables modules
from os import getenv

# Secret variables module
from dotenv import load_dotenv

# Database module
from sqlite3 import connect

# Loading bot API Key
load_dotenv()

# Router for events handling
router = Router()

# Database connection
conn = connect('DB_logic/Business.db')
cur = conn.cursor()

# Defining states for Finite State Machine
class Form(StatesGroup):
    web_app = State()
    delivery_conditions = State()
    address = State()
    delivery_time = State()
    payment_conditions = State()
    pay_state = State()
    ask_note_to_have_change_for = State()
    get_note_to_have_change_for = State()
    get_contact = State()
    skip_contact = State()
    phone_number = State()
    name = State()
    commit_order = State()
    confirmation = State()
    change_address = State()
    change_number = State()