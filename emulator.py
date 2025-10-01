import tkinter as tk
import os
import sys
import locale

if sys.platform.startswith('win'):
    locale.setlocale(locale.LC_ALL, 'rus_rus')

vfs_path = ""
script_path = ""
script_name = ""

def show_text(text):
    output_area.config(state=tk.NORMAL)
    output_area.insert(tk.END, text + "\n")
    output_area.config(state=tk.DISABLED)
    output_area.see(tk.END)

def replace_vars(text):
    words = text.split()
    result = []
    for word in words:
        if word.startswith('$'):
            var_name = word[1:]
            if var_name == "HOME":
                var_value = os.environ.get('USERPROFILE', os.environ.get('HOME', ''))
            else:
                var_value = os.environ.get(var_name, '')
            result.append(var_value)
        else:
            result.append(word)
    return ' '.join(result)

def run_command(command):
    show_text(f"> {command}")
    
    if not command.strip():
        return True 
    
    if command.strip().startswith('$'):
        var_name = command.strip()[1:]
        if var_name == "HOME":
            var_value = os.environ.get('USERPROFILE', os.environ.get('HOME', ''))
        else:
            var_value = os.environ.get(var_name, '')
            
        if var_value:
            show_text(var_value)
        else:
            show_text(f"Переменная окружения '{var_name}' не найдена")
        return True
    
    command_with_vars = replace_vars(command)
    parts = command_with_vars.split()
    if not parts:
        return True

    cmd = parts[0]
    
    if cmd == "exit":
        root.destroy()
        return True
    elif cmd == "ls":
        if len(parts) > 1:
            show_text(f"parameter ls: {parts[1]}")
        else:
            show_text("ls without parameter")
        return True
    elif cmd == "cd":
        if len(parts) > 1:
            show_text(f"parameter cd: {parts[1]}")
        else:
            show_text("cd without parameter")
        return True
    elif cmd == "conf-dump":
        show_text(f"vfs_path = {vfs_path}")
        show_text(f"script_path = {script_path}")
        return True
    else:
        show_text(f"unknown command '{cmd}'")
        return False  

def do_command(event=None):
    command = command_entry.get()
    command_entry.delete(0, tk.END)
    run_command(command)

def run_script(script_file):
    show_text(f"running a script: {script_name}")
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        show_text(f"error, we can not open a script '{script_name}'")
        show_text(f"a reason is: {e}")
        return

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        show_text("")  
        success = run_command(line)
        if not success:
            show_text(f"error in that line {i}: '{line}'")
            break  

def print_startup_info():
    show_text(f"VFS путь: {vfs_path}")
    show_text(f"start script: {script_path}")
    show_text("")

root = tk.Tk()
root.title("vsf")

output_area = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, height=20, width=50)
output_area.pack(padx=10, pady=10)

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5, fill=tk.X)

prompt_label = tk.Label(input_frame, text="> ", font=("Courier", 12))
prompt_label.pack(side=tk.LEFT)

command_entry = tk.Entry(input_frame, font=("Courier", 12))
command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
command_entry.bind("<Return>", do_command)

command_entry.focus()

if len(sys.argv) < 3:
    show_text("you have to write 2 parameters:")
    show_text("  1) path to VFS")
    show_text("  2) path to start script")
    show_text("have to write: python emulator.py /my/vfs /my/script.txt")
else:
    vfs_path = os.path.abspath(sys.argv[1])
    script_path = os.path.abspath(sys.argv[2])

    script_name = os.path.basename(sys.argv[2])
    print_startup_info()
    root.after(500, lambda: run_script(script_path))  

if __name__ == "__main__":
    root.mainloop()
