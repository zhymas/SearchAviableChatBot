from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


markup_request_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send own phone number", request_contact=True)]
    ],
    resize_keyboard=True,
    input_field_placeholder="Please share your phone to continue"
)

markup_get_file = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Press for proccesing file")]], 
    resize_keyboard=True,
    input_field_placeholder="Click to proccesing file")