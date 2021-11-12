import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, MaxNLocator

import numpy as np

menu_def = [
    ['File', ['Open', 'Save', 'Exit']],
    ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
    ['Help', 'About...'],
]

frame_layout_1 = [  # frame layout
    # L_lr - L др - Довжина ділянки ретрансляції

    [sg.InputText(size=(5, 5), k='P_res', background_color='#F5F5F5'),
     sg.Text("P зап - Потужність запасу", background_color='#2b2a33', text_color='#FFF5EE')],

    [sg.Slider(range=(0.01, 0.1),
               resolution=0.001,
               default_value=0.045,
               orientation='h',
               k='atten_connect',
               background_color='#2b2a33'),
     sg.Text("a з бд - затухання з'єднання будівельних довжин", background_color='#2b2a33', text_color='#FFF5EE')],
]

frame_layout_2 = [[sg.Output(size=(80, 10), background_color='#F5F5F5')]]

layout = [  # layout
    [sg.Menu(menu_def)],
    [sg.Frame('Вхідні дані', frame_layout_1, background_color='#2b2a33', title_color='yellow')],  # frame
    [sg.Frame('Вивід розрахункових даних', frame_layout_2, background_color='#2b2a33', title_color='yellow')],
    [sg.Button('Побудувати графік', k='graph'), sg.Button('Вихід', k='Cancel')]  # button
]
window = sg.Window(
    'Довжина ділянки ретрансляції',
    layout,
    background_color='#2b2a33',
    button_color='#708090'
)


def draw_plot():  # draw graph
    L_lr = (P_out - P_in - P_res + (2 * a_atten) + atten_connect) / ((atten_connect / L_bl) + alpha)
    print('30 - P пер - Потужність передачі \n',
          '-45 - P пр min - Мінімальна потужність прийому \n',
          "0.1 - a зс - затухання станйійного з'єднання передачі \n",
          '0.3 - робоче затухання ОВ \n',
          '10 - L бд - Довжина будівельних довжин \n\n',
          L_lr, '- L др - Довжина ділянки ретрансляції')
    # sleep(3)

    x = np.array([i for i in range(int(L_lr))])
    y = np.array([(P_out - P_in - P_res + (2 * a_atten) + i) / ((i / L_bl) + alpha) for i in range(int(L_lr))])

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot()
    ax.plot(x, y)

    ax.set(xlim=(0, 200), ylim=(0, 200))

    fig.suptitle("Затухання сигналу від довжини оптичного волокна")
    ax.set_xlabel('L lr')
    ax.set_ylabel('a attenuation')

    # ax.yaxis.set_major_locator(MaxNLocator(10))
    ax.yaxis.set_major_locator(LogLocator(base=2))

    # ax.minorticks_on()
    # ax.grid(which='major', color='#444', linewidth=1)
    # ax.grid(which='minor', color='#aaa', ls=':')
    ax.grid()
    plt.show(block=False)


while True:  # The Event Loop
    event, values = window.read()

    P_out = 30                                              # P пер - Потужність передачі
    P_in = -45                                              # P пр min - Мінімальна потужність прийому
    a_atten = 0.1                                           # a зс - затухання станйійного з'єднання передачі
    alpha = 0.3                                             # робоче затухання ОВ
    L_bl = 10                                               # L бд - Довжина будівельних довжин
    atten_connect = values['atten_connect']                 # a з бд - затухання з'єднання будівельних довжин

    ###################################################################################

    if event == 'graph':
        if values['P_res'] != '' and values['P_res'] != str:
            P_res = float(values['P_res'])                  # P зап - Потужність запасу
            draw_plot()
        else:
            print('ПОМИЛКА! Не вказано Потужність запасу')
    elif event in (sg.WIN_CLOSED, 'Cancel'):
        window.close()
        break
window.close()
