from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton


btnProfile = KeyboardButton('👤 Профіль')
btnTransactions = KeyboardButton('💰 Транзакції')

btnAdministration = KeyboardButton(text='📐Адміністрування')
btnGetUserList = KeyboardButton(text='Список користувачів')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnTransactions)
mainMenu.add(btnProfile)

mainMenu_adm = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu_adm.add(btnTransactions)
mainMenu_adm.add(btnProfile, btnAdministration)

defaultCommands = [
                    BotCommand("start", "Запуск бота"),
                    BotCommand("help", "Довідка"),
                    ]


btnGetUserList = InlineKeyboardButton(text='Список користувачів', callback_data='get_user_list')

inlineMenu_adm = InlineKeyboardMarkup(row_width=1)
inlineMenu_adm.add(btnGetUserList)


btnGetTransactionList = InlineKeyboardButton(text='Список транзакцій', callback_data='get_transaction_list')
btnCreateTransaction = InlineKeyboardButton(text='Створити транзакцію', callback_data='create_transaction')

inlineMenu_transactions = InlineKeyboardMarkup(row_width=2)
inlineMenu_transactions.add(btnGetTransactionList, btnCreateTransaction)

inlineMenu_transactions_creation = InlineKeyboardMarkup(row_width=3)
inlineMenu_transactions_creation.add(InlineKeyboardButton(text='На сьогодні', callback_data='create_transaction_today'))
inlineMenu_transactions_creation.add(InlineKeyboardButton(text='На вчора', callback_data='create_transaction_yesterday'))
inlineMenu_transactions_creation.add(InlineKeyboardButton(text='На дату', callback_data='create_transaction_date'))

inlineMenu_transactions_types = InlineKeyboardMarkup(row_width=3)
inlineMenu_transactions_types.add(InlineKeyboardButton(text='Таксі', callback_data='create_type_taxi'))
inlineMenu_transactions_types.add(InlineKeyboardButton(text='Обід', callback_data='create_type_lunch'))
inlineMenu_transactions_types.add(InlineKeyboardButton(text='Перекус', callback_data='create_type_snack'))
inlineMenu_transactions_types.add(InlineKeyboardButton(text='Алкоголь', callback_data='create_type_alcohol'))
inlineMenu_transactions_types.add(InlineKeyboardButton(text='Інше', callback_data='create_type_other'))

inlineMenu_confirmation = InlineKeyboardMarkup(row_width=2)
inlineMenu_confirmation.add(InlineKeyboardButton(text='✔ Погодити', callback_data='confirmation_confirm'))
inlineMenu_confirmation.add(InlineKeyboardButton(text='❌ Відхилити', callback_data='confirmation_cancel'))

inlineMenu_transactions_cancelation = InlineKeyboardMarkup(row_width=2)
inlineMenu_transactions_cancelation.add(InlineKeyboardButton(text='❌ Відхилити створення транзакції', callback_data='transactions_cancelation'))

inlineMenu_transactions_input_cancelation = InlineKeyboardMarkup(row_width=2)
inlineMenu_transactions_input_cancelation.add(InlineKeyboardButton(text='Пропустити', callback_data='transactions_input_cancelation'))
