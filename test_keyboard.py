import keyboard
import time

print("=" * 50)
print("键盘库测试程序")
print("=" * 50)
print("\n测试项目：")
print("1. 按 Ctrl+Shift+T 测试快捷键")
print("2. 按 ESC 退出程序")
print("\n提示：在Windows上需要管理员权限才能全局监听键盘")
print("=" * 50)

# 测试计数器
test_count = 0

def on_test_hotkey():
    global test_count
    test_count += 1
    keyboard.press_and_release('win+shift+s')
    print(f"\n✓ 快捷键触发成功！(第 {test_count} 次)")
    print(f"  时间: {time.strftime('%H:%M:%S')}")

def on_exit():
    print("\n\n程序退出")
    exit(0)

# 注册快捷键
keyboard.add_hotkey('s+c', on_test_hotkey)
keyboard.add_hotkey('esc', on_exit)

print("\n等待快捷键输入...")
keyboard.wait()
