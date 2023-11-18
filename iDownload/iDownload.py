import tkinter as tk
from tkinter import filedialog, messagebox

import os
import re
import shutil
import time
import pyautogui
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webbrowser

def download_books(path, pos1, pos2, pos3, pos4):
    folder_path = path
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    file_lists = []

    def remove_first_line(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(lines[1:])

        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_file_lines(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [line.strip() for line in lines if len(line)>5]

    txt_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]

    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        lines_list = read_file_lines(file_path)
        file_lists.append([txt_file, lines_list])

    count = 0
    current_book = file_lists[count][0]
    current_urls = file_lists[count][1]

    os.mkdir(os.path.join(downloads, current_book.split('.')[0]))

    def standarize_names(current_book, current_urls, count, file_lists):
        def get_file_name():
            md_files = [f for f in os.listdir(downloads) if os.path.isfile(os.path.join(downloads, f)) and f.lower().endswith(".md")]
            if len(md_files) > 0:
                md_files = list(filter(lambda x: len(x)>3, md_files))
                original_file_name = os.path.splitext(os.path.basename(md_files[0]))[0]
            else:
                raise FileNotFoundError("No or multiple .md files found in the directory.")

            file_name_parts = original_file_name.split('-')
            modified_file_name = '-'.join(file_name_parts[:-1]).strip()
            os.rename(os.path.join(downloads, f"{original_file_name}.md"), os.path.join(downloads, f"{modified_file_name}.md"))

            return modified_file_name

        file_name = get_file_name()

        def get_images_in_folder():
            images_folder = os.path.join(downloads, "Images")
            try:
                images = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]

                for image_file in images:
                    image_name, image_ext = os.path.splitext(image_file)
                    new_image_name = f"{file_name} - {image_name}{image_ext}"
                    os.rename(os.path.join(images_folder, image_file), os.path.join(images_folder, new_image_name))

                return sorted(images, key=lambda x: int(re.search(r'\d+', x.split('-')[-1]).group()))
            except:
                return []

        def update_image_links(md_file, images):
            with open(md_file, 'r') as file:
                md_content = file.read()

            for image_file in images:
                image_name, image_ext = os.path.splitext(os.path.basename(image_file))
                new_image_name = f"{file_name} - {image_name}{image_ext}"

                md_content = re.sub(r'!\[(?!.*\binline\b.*\])(.*)\)', f"\n\n![[{os.path.join('Images', new_image_name)}]]", md_content, count=1)

            with open(md_file, 'w') as file:
                file.write(md_content)

        def create_directory_structure():
            os.mkdir(os.path.join(downloads, file_name))
            shutil.move(os.path.join(downloads, f"{file_name}.md"), os.path.join(downloads, file_name, f"{file_name}.md"))
            try:
                shutil.move(os.path.join(downloads, "Images"), os.path.join(downloads, file_name, "Images"))
            except:
                print("No images")


        images = get_images_in_folder()

        md_file = os.path.join(downloads, f"{file_name}.md")

        update_image_links(md_file, images)

        create_directory_structure()

        shutil.move(os.path.join(downloads, file_name), os.path.join(downloads, current_book.split('.')[0]))

        if len(current_urls)==0:
            print("Book finished")
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            shutil.move(os.path.join(downloads, current_book.split('.')[0]), desktop_path)
            print(count)
            count += 1
            print(current_book)
            current_book = file_lists[count][0]
            current_urls = file_lists[count][1]

            if current_book:
                print('Preparing next book  ...')
                os.mkdir(os.path.join(downloads, current_book.split('.')[0]))
                print(current_book.split('.')[0])
                return None
            else:
                print('Stopping script ...')
                print(0/0)
        else:
            print(str(len(current_urls))+" chapters left!")
            return None

    class FileHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.is_directory:
                return
            if os.path.exists(os.path.join(downloads, "DOWNLOAD.txt")):
                first_download = False
                print("Download finished!")
                time.sleep(1)
                os.remove(os.path.join(downloads, "DOWNLOAD.txt"))
                try:
                    print("Chapter created!")

                    standarize_names(current_book, current_urls, count, file_lists)

                    webbrowser.open(current_urls.pop(0))
                    remove_first_line(folder_path+"/"+current_book)

                    time.sleep(4)

                    pyautogui.click(pos1[0], pos1[1])
                    time.sleep(2)
                    pyautogui.click(pos2[0], pos2[1])
                    time.sleep(1)
                    pyautogui.click(pos3[0], pos3[1])
                    time.sleep(1)
                    pyautogui.click(pos4[0], pos4[1])

                    print("Downloading ...")

                except:
                    stop_script()

    def stop_script():
        global observer
        observer.stop()
        print('Stop script!')
        
    def listen_for_changes():
        event_handler = FileHandler()
        global observer
        observer = Observer()
        observer.schedule(event_handler, path=downloads, recursive=False)
        observer.start()

        try:
            while observer.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            stop_script()
            print('Stop script!')
            return None

        observer.join()

    webbrowser.open(current_urls.pop(0))
    print(current_urls)
    remove_first_line(folder_path+"/"+current_book)

    time.sleep(4)

    pyautogui.click(pos1[0], pos1[1])
    time.sleep(2)
    pyautogui.click(pos2[0], pos2[1])
    time.sleep(1)
    pyautogui.click(pos3[0], pos3[1])
    time.sleep(1)
    pyautogui.click(pos4[0], pos4[1])

    print("Downloading ...")

    listen_for_changes()


class LocationSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-alpha', 0.8)
        self.root.title("iDownload")
        self.folder_path = ""
        self.books = "(not selected)"
        self.locations = []
        self.pos1 = "(not selected)"
        self.pos2 = "(not selected)"
        self.pos3 = "(not selected)"
        self.pos4 = "(not selected)"

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Folder", command=self.select_folder)
        file_menu.add_command(label="Exit", command=self.root.quit)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=600, bg="white")
        self.canvas.pack()

        self.folder_label = tk.Label(self.root, text="Selected Folder: " + self.books)
        self.folder_label.pack(side=tk.BOTTOM)

        self.folder_button = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(side=tk.BOTTOM)

        self.select_locations_button = tk.Button(self.root, text="Select Locations", command=self.reset_and_select_locations)
        self.select_locations_button.pack(side=tk.BOTTOM)

        self.run_code_button = tk.Button(self.root, text="Run Code", command=self.run_code)
        self.run_code_button.pack(side=tk.BOTTOM)

        self.pos1_label = tk.Label(self.root, text="Position 1: " + self.pos1)
        self.pos1_label.pack(side=tk.BOTTOM)
        self.pos2_label = tk.Label(self.root, text="Position 2: " + self.pos2)
        self.pos2_label.pack(side=tk.BOTTOM)
        self.pos3_label = tk.Label(self.root, text="Position 3: " + self.pos3)
        self.pos3_label.pack(side=tk.BOTTOM)
        self.pos4_label = tk.Label(self.root, text="Position 4: " + self.pos4)
        self.pos4_label.pack(side=tk.BOTTOM)

    def reset_and_select_locations(self):
        self.locations = []
        self.pos1 = "(not selected)"
        self.pos2 = "(not selected)"
        self.pos3 = "(not selected)"
        self.pos4 = "(not selected)"
        self.update_position_labels()
        self.canvas.delete("all")  # Clear the canvas
        self.select_locations()

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.books = self.folder_path
            self.folder_label.config(text="Selected Folder: " + self.books)

    def select_locations(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        messagebox.showwarning("Warning", "Offset captured!\nNow select 4 points!")
        self.offset = (self.root.winfo_rootx(), self.root.winfo_rooty())

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.locations.append((x, y))
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")

        if len(self.locations) == 4:
            self.canvas.unbind("<Button-1>")
            self.pos1, self.pos2, self.pos3, self.pos4 = self.locations
            self.update_position_labels()
            self.save_locations()

    def update_position_labels(self):
        self.pos1_label.config(text="Position 1: " + str(self.pos1))
        self.pos2_label.config(text="Position 2: " + str(self.pos2))
        self.pos3_label.config(text="Position 3: " + str(self.pos3))
        self.pos4_label.config(text="Position 4: " + str(self.pos4))

    def save_locations(self):
        print("Selected Locations:")
        print("Position 1:", self.pos1)
        print("Position 2:", self.pos2)
        print("Position 3:", self.pos3)
        print("Position 4:", self.pos4)

    def run_code(self):
        if self.books!="(not selected)" and type(self.pos1)==tuple and type(self.pos2)==tuple and type(self.pos3)==tuple and type(self.pos4)==tuple:
            try:
                offset_pos1 = (self.pos1[0] + self.offset[0], self.pos1[1] + self.offset[1])
                offset_pos2 = (self.pos2[0] + self.offset[0], self.pos2[1] + self.offset[1])
                offset_pos3 = (self.pos3[0] + self.offset[0], self.pos3[1] + self.offset[1])
                offset_pos4 = (self.pos4[0] + self.offset[0], self.pos4[1] + self.offset[1])

                print(offset_pos1)

                download_books(self.books, offset_pos1, offset_pos2, offset_pos3, offset_pos4)
            except Exception as e:
                messagebox.showwarning("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Missing values!")
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = LocationSelectorApp(root)
    x, y = pyautogui.position()
    pyautogui.moveTo(x, y + 1, duration=0.1)
    root.mainloop()



