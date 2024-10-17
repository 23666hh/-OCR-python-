from pynput.mouse import Button, Listener
from pynput.keyboard import Key, Listener as KeyboardListener
from PIL import ImageGrab
import json
import os


class ScreenSelector:
    def __init__(self, config_file='selection_config.json'):
        self.config_file = config_file
        self.selection = {
            'start': None,
            'end': None,
            'rectangle': None,
            'draw': None,
            'buttons': {
                'button1': None,
                'button2': None,
                'button3': None
            }
        }
        self.selecting = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.mouse_position_listener = None
        self.click_count = 0

    def on_click(self, x, y, button, pressed):
        if button == Button.left:
            if pressed:
                # 开始选择区域
                self.selecting = True
                self.selection['start'] = (x, y)
            else:
                # 结束选择区域
                self.selecting = False
                self.selection['end'] = (x, y)
                self.selection['rectangle'] = \
                    [min(self.selection['start'][0], self.selection['end'][0]),
                     min(self.selection['start'][1], self.selection['end'][1]),
                     max(self.selection['start'][0], self.selection['end'][0]),
                     max(self.selection['start'][1], self.selection['end'][1])]
                print(f"选择的区域: {self.selection['rectangle']}")
                # 如果没有选择区域，则重新选择
                if self.selection['start'] == self.selection['end']:
                    self.selection['rectangle'] = None
                    print("没有选择任何区域，请重新选择")
                else:
                    # 停止监听鼠标事件
                    self.mouse_listener.stop()
                    self.keyboard_listener.stop()

    def on_move(self, x, y):
        if self.selecting:
            print(f"当前位置: {x, y}")

    def on_press(self, key):
        if key == Key.esc:
            # 按下 Esc 键退出
            self.mouse_listener.stop()
            self.keyboard_listener.stop()

    def start_listeners(self):
        self.mouse_listener = Listener(on_click=self.on_click, on_move=self.on_move)
        self.keyboard_listener = KeyboardListener(on_press=self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def join_listeners(self):
        self.mouse_listener.join()
        self.keyboard_listener.join()

    def save_selection_to_file(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.selection, f, indent=4)
        print(f"配置文件已保存到 {self.config_file}")

    def load_selection_from_file(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    # 检查数据是否符合预期格式
                    if all(key in data for key in self.selection.keys()):
                        return data
                    else:
                        print("警告: 加载的配置文件格式不正确，忽略该文件。")
            except json.JSONDecodeError:
                print("警告: 配置文件不是有效的 JSON 格式，忽略该文件。")
            except Exception as e:
                print(f"警告: 读取配置文件时发生错误: {e}")
        else:
            print("配置文件不存在")
        return None

    def screenshot(self, rectangle):
        if self.selection[rectangle]:
            if (self.selection[rectangle][0] < self.selection[rectangle][2] and
                    self.selection[rectangle][1] < self.selection[rectangle][3]):
                screenshot = ImageGrab.grab(bbox=self.selection[rectangle])
                screenshot.show()  # 显示截图
                # screenshot.save('selected_area.png')  # 保存截图
                # print(f"截图已保存为 selected_area.png")
            else:
                print("选择区域数据错误，无法进行截图")
        else:
            print("没有选择任何区域，无法进行截图")

    def on_click_draw_position(self, x, y, button, pressed):
        if button == Button.right and pressed:
            self.selection['draw'] = (x, y)
            print(f"鼠标右键点击坐标: {x, y}")
        if button == Button.middle and pressed:
            self.mouse_position_listener.stop()
            self.save_selection_to_file()

    def on_click_button_position(self, x, y, button, pressed):
        if button == Button.right and pressed:
            self.click_count += 1
            if self.click_count <= 3:
                self.selection['buttons'][f'button{self.click_count}'] = (x, y)
                print(f"鼠标右键点击坐标: {x, y}")
            else:
                print("最多保存三个坐标，如需更多请修改 screen_selector.py")
        if button == Button.middle and pressed:
            if self.click_count == 0:
                print("请至少点击一个坐标")
            else:
                self.mouse_position_listener.stop()
                self.save_selection_to_file()

    def get_click_position(self, obj):
        print("请用鼠标右键点击，中键取消操作...")
        if obj == 'draw':
            self.mouse_position_listener = Listener(on_click=self.on_click_draw_position)
        if obj == 'button':
            self.mouse_position_listener = Listener(on_click=self.on_click_button_position)
        self.mouse_position_listener.start()
        self.mouse_position_listener.join()

    def run(self):
        # 尝试从文件中加载选择区域
        saved_selection = self.load_selection_from_file()
        # 如果配置文件正确，则直接使用，否则重新录入
        if saved_selection is not None and saved_selection['rectangle'] is not None:
            self.selection = saved_selection
            print(f"加载的识别区域: {self.selection['rectangle']}")
            print(f"加载的绘画位置: {self.selection['draw']}")
            print(f"加载的按钮位置: {self.selection['buttons']}")
        else:
            print("请移动鼠标到区域的左上角并按住左键拖动以选择区域。按下 Esc 键退出")
            self.start_listeners()  # 启动监听器
            self.join_listeners()  # 等待监听器停止
            # 判断是否没有选中任何区域并退出
            if self.selection['rectangle'] is None:
                print("没有选择任何区域，无法保存配置文件")
                return
            else:
                self.save_selection_to_file()
        # 截图
        # self.screenshot('rectangle')


if __name__ == "__main__":
    selector = ScreenSelector()
    selector.run()
