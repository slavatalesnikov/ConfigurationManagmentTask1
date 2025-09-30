import tkinter as tk
import os

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

def do_command(event=None):
    command = command_entry.get()
    command_entry.delete(0, tk.END)
    
    show_text(f"> {command}")
    
    if not command.strip():
        return
    
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
        return
    
    command_with_vars = replace_vars(command)
    
    parts = command_with_vars.split()
    if not parts:
        return
        
    cmd = parts[0]
    
    if cmd == "exit":
        root.destroy()
    elif cmd == "ls":
        if len(parts) > 1:
            show_text(f"Параметр ls: {parts[1:]}")
        else:
            show_text("ls без параметров")
    elif cmd == "cd":
        if len(parts) > 1:
            show_text(f"Параметр cd: {parts[1:]}")
        else:
            show_text("cd без параметров")
    else:
        show_text(f"Неизвестная команда '{cmd}'")


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


if __name__ == "__main__":
    root.mainloop()
