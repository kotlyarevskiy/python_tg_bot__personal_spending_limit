import asyncio
import config, logging, re, datetime, json
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
import markups as nav
from users import User
from transactions import Transaction
from aiogram.utils import markdown


logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
user = User()
transaction = Transaction()

class TransactionState(StatesGroup):
    TRANSACTION = State()
    CREATE_TRANSACTION = State()
    SET_TRANSACTION_DATE = State()
    SET_SUM = State()
    SET_TYPE = State()
    SET_COMMENT = State()
    CONFIRM = State()

class TestState(StatesGroup):
    CREATE_TRANSACTION = State()
    SET_TRANSACTION_DATE = State()
    SET_SUM = State()
    SET_TYPE = State()
    SET_COMMENT = State()
    CONFIRM = State()
    

def get_main_menu(user_info):
    main_menu = nav.mainMenu_adm if user_info["admin"] else nav.mainMenu
    return main_menu

@dp.message_handler(commands=['test'])
async def test(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    sent_message = await bot.send_message(user_id, "test")
    await state.update_data(first_message_id=sent_message.message_id)

    
    #await state.update_data(chat_id=sent_message.chat.id)
    
    await state.set_state(TestState.CREATE_TRANSACTION)

@dp.message_handler(state=TestState.CREATE_TRANSACTION)
async def testCREATE_TRANSACTION(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text=f"CREATE_TRANSACTION")    
    await state.set_state(TestState.SET_TRANSACTION_DATE)

    await bot.send_chat_action(chat_id=chat_id, action=types.ChatActions.TYPING)
    await asyncio.sleep(1)
      
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

@dp.message_handler(state=TestState.SET_TRANSACTION_DATE)
async def testSET_TRANSACTION_DATE(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await bot.edit_message_text(chat_id=message.chat.id, message_id=first_message_id, text=f"SET_TRANSACTION_DATE")
    await state.set_state(TestState.SET_SUM)


@dp.message_handler(state=TestState.SET_SUM)
async def testSET_SUM(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await bot.edit_message_text(chat_id=message.chat.id, message_id=first_message_id, text=f"SET_SUM")
    await state.set_state(TestState.SET_TYPE)


@dp.message_handler(state=TestState.SET_TYPE)
async def testSET_TYPE(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await bot.edit_message_text(chat_id=message.chat.id, message_id=first_message_id, text=f"SET_TYPE")
    await state.set_state(TestState.SET_COMMENT)


@dp.message_handler(state=TestState.SET_COMMENT)
async def testSET_COMMENT(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await bot.edit_message_text(chat_id=message.chat.id, message_id=first_message_id, text=f"SET_COMMENT")
    await state.set_state(TestState.CONFIRM)

@dp.message_handler(state=TestState.CONFIRM)
async def testCONFIRM(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await bot.edit_message_text(chat_id=message.chat.id, message_id=first_message_id, text=f"CONFIRM")
    await state.finish()




@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await bot.set_my_commands(nav.defaultCommands)

    user_id = message.from_user.id

    if(user.user_exists(user_id)):
      
        user_info = user.get_user_info(user_id)
        main_menu = get_main_menu(user_info)
       
        if user_info["blocked"]:
         
            await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))
            return
        
        await bot.send_message(user_id, "Ви вже зареєстровані!!!", reply_markup=main_menu)

    else:
       
        user.add_user(user_id)
       
        await bot.send_message(user_id, "Тепер вкажіть свій нікнейм.")


@dp.callback_query_handler(lambda c: c.data == 'get_user_list')
async def get_user_list(callback_query: types.CallbackQuery): 
    
    #await bot.delete_message(callback_query.chat.id, callback_query.message_id)  

    user_id = callback_query.from_user.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return
    
    if not user_info["admin"]:
        
        await bot.send_message(user_id, str(User.message_if_not_admin.replace("%s", user_info["nickname"])))   
        return    
 

    data = [
        ["Иванов", 30, "Москва"],
        ["Петров", 25, "Санкт-Петербург"],
        ["Сидоров", 35, "Казань"],
    ]

    table_md = "```\n"
    table_md += "Имя      | Возраст | Город         \n"
    table_md += "---------|---------|--------------\n"
    for row in data:
        table_md += f"{row[0]:<9}| {row[1]:<6}  | {row[2]:<13}\n"
    table_md += "```"

    await bot.send_message(user_id, table_md, parse_mode=types.ParseMode.MARKDOWN, disable_notification=True)


@dp.callback_query_handler(lambda c: c.data == 'get_transaction_list')
async def get_transaction_list(callback_query: types.CallbackQuery): 
    
    #await bot.delete_message(callback_query.chat.id, callback_query.message_id)  

    user_id = callback_query.from_user.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return
    

    await bot.send_message(user_id, "get_transaction_list")

@dp.callback_query_handler(lambda c: c.data == 'transactions_cancelation', state= '*')
async def transactions_cancelation(callback_query: types.CallbackQuery, state: FSMContext): 
    
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return

    transaction_data = await state.get_data()

    if not transaction_data:
        return
    
    first_message_id = transaction_data["first_message_id"]
    group_message_id = transaction_data["group_message_id"]  

    pretty_transaction_data = json.dumps(transaction_data)

    await bot.edit_message_text(chat_id=chat_id, message_id=group_message_id, text="Створення транзакції відхилено." + "\n" + pretty_transaction_data, reply_markup=None)
    await bot.delete_message(chat_id=chat_id, message_id=first_message_id)
    #await bot.delete_message(chat_id=chat_id, message_id=group_message_id)
    await state.finish()

 
    


@dp.callback_query_handler(state=TransactionState.TRANSACTION)
async def group_transaction(callback_query: types.CallbackQuery, state: FSMContext): 
    
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return

    transaction_data = await state.get_data()
    group_message_id = transaction_data["group_message_id"]   

    sent_message = await bot.send_message(user_id, "Створити транзакцію:", reply_markup=nav.inlineMenu_transactions_creation)
    await state.update_data(first_message_id=sent_message.message_id)
    await bot.edit_message_text(chat_id=chat_id, message_id=group_message_id, text="Транзакції:", reply_markup=nav.inlineMenu_transactions_cancelation)
    await state.set_state(TransactionState.CREATE_TRANSACTION)


@dp.callback_query_handler(state=TransactionState.CREATE_TRANSACTION)
async def create_transaction(callback_query: types.CallbackQuery, state: FSMContext): 
    
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)    

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return
    
    mode = callback_query.data.replace("create_transaction_", "")
    promt_text = ""
    
    current_date = datetime.date.today()
    yesterday_date = current_date - datetime.timedelta(days=1)
    
    if mode == "today":

        await state.update_data(transaction_date=current_date.strftime("%Y-%m-%d"))

        promt_text = "Введіть суму для зарахування сьогоднішнім числом:"
        next_state = TransactionState.SET_SUM

    elif  mode == "yesterday":

        await state.update_data(transaction_date=yesterday_date.strftime("%Y-%m-%d"))

        promt_text = "Введіть суму для зарахування вчорашнім числом:"
        next_state = TransactionState.SET_SUM

    elif mode == "date":

        promt_text = "Введіть дату в форматі РРРР ММ ДД:"
        next_state = TransactionState.SET_TRANSACTION_DATE


    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    #await bot.send_chat_action(chat_id=callback_query.message.chat.id, action=types.ChatActions.TYPING)
    #await asyncio.sleep(1)
    #await bot.delete_message(chat_id=chat_id, message_id=callback_query.message_id)

    await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text=promt_text, reply_markup=None)
    #await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=first_message_id, reply_markup=None)
    await state.set_state(next_state)
    

@dp.message_handler(state=TransactionState.SET_TRANSACTION_DATE)
async def process_input_date(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return   
    
    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

   

    try:
        date_obj = datetime.datetime.strptime(message.text, "%Y-%m-%d")
        #unix_timestamp = date_obj.timestamp()
    except ValueError:
        await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text=f"Помилка введення дати: {message.text}. Введіть дату в форматі РРРР ММ ДД:")
        return

    await state.update_data(transaction_date=message.text)

    await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text=f"Введіть суму:")
    await state.set_state(TransactionState.SET_SUM)


@dp.message_handler(state=TransactionState.SET_SUM)
async def process_input_sum(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return   
    
    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await state.update_data(sum=message.text)
    
    await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text="Оберіть тип транзакції:", reply_markup=nav.inlineMenu_transactions_types)
    await state.set_state(TransactionState.SET_TYPE)


@dp.callback_query_handler(state=TransactionState.SET_TYPE)
async def process_input_comment(callback_query: types.CallbackQuery, state: FSMContext):
    
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    #await bot.delete_message(chat_id=chat_id, message_id=callback_query.message_id)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return   

    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    answer = callback_query.data.replace("create_type_", "")

    await state.update_data(type=answer)

    await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text="Додайте коментар:", reply_markup=nav.inlineMenu_transactions_input_cancelation)
    await state.set_state(TransactionState.SET_COMMENT)

@dp.callback_query_handler(lambda c: c.data == 'transactions_input_cancelation', state=TransactionState.SET_COMMENT)
async def process_skip_comment(callback_query: types.CallbackQuery, state: FSMContext):
    
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    #await bot.delete_message(chat_id=chat_id, message_id=callback_query.message_id)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return   
    
    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await state.update_data(comment="")

    await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text="Зберегти транзакцію?", reply_markup=nav.inlineMenu_confirmation)
    await state.set_state(TransactionState.CONFIRM)

@dp.message_handler(state=TransactionState.SET_COMMENT)
async def process_input_comment(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return   
    
    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]

    await state.update_data(comment=message.text)

    await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text="Зберегти транзакцію?", reply_markup=nav.inlineMenu_confirmation)
    await state.set_state(TransactionState.CONFIRM)

@dp.callback_query_handler(state=TransactionState.CONFIRM)
async def process_input_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return   
        
   
    transaction_data = await state.get_data()
    first_message_id = transaction_data["first_message_id"]    
    group_message_id = transaction_data["group_message_id"]   

    answer = callback_query.data.replace("confirmation_", "")
    status_of_transaction = ""
    transaction_data = await state.get_data()

    if answer == "confirm":        

        transaction.add_transaction(user_id, transaction_data)

        status_of_transaction = "Транзакція збережена."

        await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text=status_of_transaction, reply_markup=None)

    elif answer == "cancel":

        status_of_transaction = "Транзакцію не збережено."

        await bot.edit_message_text(chat_id=chat_id, message_id=first_message_id, text=status_of_transaction, reply_markup=None)

    pretty_transaction_data = json.dumps(transaction_data)

    await bot.edit_message_text(chat_id=chat_id, message_id=group_message_id, text=status_of_transaction + "\n" + pretty_transaction_data, reply_markup=None)
        
    await state.finish()

    await asyncio.sleep(3)
    await bot.delete_message(chat_id=chat_id, message_id=first_message_id)
    #await bot.delete_message(chat_id=chat_id, message_id=group_message_id)


@dp.message_handler(filters. Text("💰 Транзакції"))
async def bot_message_administration(message: types.Message, state: FSMContext):
   
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return
     

    sent_message = await bot.send_message(user_id, "Транзакції:", reply_markup=nav.inlineMenu_transactions)
 
    await state.update_data(group_message_id=sent_message.message_id)
    await state.set_state(TransactionState.TRANSACTION)

@dp.message_handler(filters.Text("📐Адміністрування"))
async def bot_message_administration(message: types.Message):
   
    user_id = message.from_user.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return
    
    if not user_info["admin"]:
        
        await bot.send_message(user_id, str(User.message_if_not_admin.replace("%s", user_info["nickname"])))   
        return    
 

    await bot.send_message(user_id, "Адміністрування:", reply_markup=nav.inlineMenu_adm)
    

@dp.message_handler()
async def bot_message(message: types.Message):
   
    user_id = message.from_user.id
    user_info = user.get_user_info(user_id)
    main_menu = get_main_menu(user_info)

    if user_info["blocked"]:
        
        await bot.send_message(user_id, str(User.message_for_blocked_user.replace("%s", user_info["nickname"])))   
        return
   
    if(message.chat.type == 'private'):
        
        if(message.text == '👤 Профіль'):
        
            await bot.send_message(user_id, "yes" if user_info["admin"] else "no")
       
        else:
         
            if user_info["signup"] == "setnickname":
           
                if len(message.text) > 15:
             
                    await bot.send_message(user_id, "Нікнейм має бути не більше 15-ти символів.")
              
                elif "@" in message.text or "/" in message.text:
             
                    await bot.send_message(user_id, "Ви ввели заборонений символ.")
              
                else:
               
                    user.set_nickname(user_id, message.text)
                    user.set_signup(user_id, "DONE")
                   
                    await bot.send_message(user_id, "Реєстрація пройшла успішно.", reply_markup=main_menu)
           
            else:
             
                await bot.send_message(user_id, "аА?", reply_markup=main_menu)


if __name__ == "__main__":
    
    executor.start_polling(dp, skip_updates=True)