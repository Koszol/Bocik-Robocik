import random


def get_response(message: str,username: str) -> str:
    p_message = message.lower()
    if p_message == 'hello':
        r_message=str('Hey there '+username)
        return r_message

    if p_message == 'roll':
        return username+' rolled: '+str(random.randint(1, 6))


    if p_message == '!help':
        return '`This is a help message that you can modify.`'