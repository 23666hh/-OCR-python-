from screen_selector import ScreenSelector
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener
import mss
import numpy as np
import cv2
import pytesseract
import sys
import time

# 导入tesseract安装路径，如果设置了系统环境，就可以不用设置了
# pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

# 定义一个标志变量来控制主循环的退出
exit_program = False

# 创建区域选取器
selector = ScreenSelector()

# 创建鼠标控制器对象
mouse = Controller()


# 截屏
def capture_region(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        screenshot_bgra_np = np.array(screenshot)
        return screenshot_bgra_np


# 识别
def recognize_numbers(image):
    numbers = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, config='--psm 6')
    print(f"识别结果: {text}")
    # 提取数字
    for i in text.split():
        digits = [char for char in i if char.isdigit()]
        if digits:
            digit = int(''.join(digits))
        else:
            if digits == 0:
                digit = digits
            else:
                continue
        numbers.append(digit)
    print(f"提取出的数字: {numbers}")
    return numbers


# 判断大小
def judge_size(number):
    position = load_draw_position()  # 获取绘画坐标
    x, y = position[0], position[1]
    first, second = number[0], number[-1]
    if first < second:
        print(f"{first} < {second}")
        draw_less_than_sign(x, y)
    elif first > second:
        print(f"{first} > {second}")
        draw_greater_than_sign(x, y)
    else:
        print(f"{first} = {second}")
        draw_equal_sign(x, y)


# 读取绘画坐标
def load_draw_position():
    draw = selector.selection['draw']

    # 如果为空，则录入坐标
    if draw is None:
        selector.get_click_position('draw')
        # 更新数据
        draw = selector.selection['draw']
        if draw is None:
            print("由于没有选中绘画点，程序将退出")
            sys.exit()

    return draw


# 绘制小于符号 <
def draw_less_than_sign(x, y):
    draw_x, draw_y = x, y
    mouse.position = draw_x, draw_y
    mouse.press(Button.left)
    for _ in range(100):
        x -= 1
        y += 1
        mouse.position = (x, y)
        time.sleep(0.000005)  # 每 0.005 毫秒移动一次
    for _ in range(100):
        x += 1
        y += 1
        mouse.position = (x, y)
    mouse.release(Button.left)
    mouse.position = draw_x, draw_y


# 绘制大于符号 >
def draw_greater_than_sign(x, y):
    draw_x, draw_y = x, y
    mouse.position = draw_x, draw_y
    mouse.press(Button.left)
    for _ in range(100):
        x += 1
        y += 1
        mouse.position = (x, y)
        time.sleep(0.000005)  # 每 0.005 毫秒移动一次
    for _ in range(100):
        x -= 1
        y += 1
        mouse.position = (x, y)
    mouse.release(Button.left)
    mouse.position = draw_x, draw_y


# 绘制等于符号 =
def draw_equal_sign(x, y):
    draw_x, draw_y = x, y
    mouse.position = draw_x, draw_y
    mouse.press(Button.left)
    for _ in range(100):
        x += 1
        mouse.position = (x, y)
        time.sleep(0.00001)  # 每 0.01 毫秒移动一次
    for _ in range(100):
        x -= 1
        mouse.position = (x, y)
    mouse.release(Button.left)


# 读取按钮坐标
def load_button_position():
    buttons = selector.selection['buttons']

    # 如果都为空，则录入坐标，至少一个最多三个
    if all(value is None for value in buttons.values()):
        selector.get_click_position('button')

    click_button1 = buttons['button1']
    click_button2 = buttons['button2']
    click_button3 = buttons['button3']

    # 点击按钮
    click_button(click_button1, 1)
    click_button(click_button2, 1)
    click_button(click_button3, 1)


# 移动鼠标并点击
def click_button(button, sleep):
    if button is not None:
        mouse.position = button
        mouse.press(Button.left)
        mouse.release(Button.left)
        print(f"已点击按钮：{button}")
        time.sleep(sleep)


def on_press(key):
    global exit_program
    if key.char == '-':
        print("按下 '-' 键，程序将退出。")
        exit_program = True


def main():
    last_number = 0

    selector.run()

    try:
        start_x = selector.selection['rectangle'][0]
        start_y = selector.selection['rectangle'][1]
        width = selector.selection['rectangle'][2] - selector.selection['rectangle'][0]
        height = selector.selection['rectangle'][3] - selector.selection['rectangle'][1]
    except Exception as e:
        sys.exit(f"强制退出发生错误：{e}")

    # 启动键盘监听器，非阻塞方式
    listener = Listener(on_press=on_press)
    listener.start()

    while not exit_program:
        image = capture_region(start_x, start_y, width, height)  # 截取屏幕区域
        number = recognize_numbers(image)  # 识别数字
        if not number:
            if number != 0:
                print("当前数字为空，跳过本次循环")
                continue
        if number == last_number:
            print("当前数字或与上一次数字相同，跳过本次循环")
            continue
        last_number = number
        judge_size(number)  # 判断大小

        time.sleep(0.008)  # 防止答题太快上一题未消失
    sys.exit()


if __name__ == "__main__":
    main()
