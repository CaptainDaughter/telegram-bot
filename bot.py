#в близжайшем будущем хотим прокачивать бота
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import CommandHandler, Updater, ConversationHandler, MessageHandler, Filters
from random import *

reply_keyboard = [['/close', '/random', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Привет, давай познакомимся!\n"
        "Как тебя я могу называть?"
    )
    return 1


def help(update, context):
    update.message.reply_text(
        "Я умею:\n"
        "1. /costi <кол-во>\n"
        "2. /set_timer <секунд>\n"
        "3. /random <до какого числа>\n"
    )


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def first_response(update, context):
    update.message.reply_text(f"Приветствую, {update.message.text}! Жду указаний!",
                              reply_markup=markup)
    return stop


def stop(update, context):
    return ConversationHandler.END


def costi(update, context):
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return
        update.message.reply_text(f'Кидаю..')
        for i in range(due):
            result = randint(1, 6)
            j = i + 1
            update.message.reply_text(f'Кость номер {j}: {result}')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /costi <кол-во>')


def random_(update, context):
    r = randint(1, 100)
    update.message.reply_text(f'Число: {r}')


def random(update, context):
    mx = int(context.args[0])
    r = randint(1, mx)
    update.message.reply_text(f'Число: {r}')


def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(task, due, context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text(f'Вернусь через {due} секунд')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer <секунд>')


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def main():
    updater = Updater('1731483913:AAFJTkKQ-s4gisn2-Jfiba_FpH7AJhb-jrY', use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [MessageHandler(Filters.text, first_response, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("costi", costi,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("set_timer", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("random_", random_))
    dp.add_handler(CommandHandler("random", random))

    dp.add_handler(CommandHandler("close", close_keyboard))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
