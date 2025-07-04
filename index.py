import customtkinter
from PIL import Image
from backend.sql_connector_3 import get_conn
from backend.tasks_dao import get_all_tasks, create_task, delete_task
__root = None
__page_container = None
__current_page = None

def init():
    global __root, __page_container
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")
    __root = customtkinter.CTk()
    __root.geometry("600x500")
    __root.title("Achievement Diary - Tasks")

    __page_container = customtkinter.CTkFrame(__root)
    __page_container.pack(fill="both", expand=True)

    return __root

def switch_page(new_page):
    global __current_page
    if __current_page is not None:
        __current_page.destroy()
    __current_page = new_page
    __current_page.pack(fill="both", expand=True)

# ---- Fetch and display tasks ----
def show_tasks():
    page = customtkinter.CTkFrame(master=__page_container)
    header = customtkinter.CTkLabel(page, text="Your Tasks", font=("Arial", 20))
    header.pack(pady=10)

    task_scroll = customtkinter.CTkScrollableFrame(master=page, label_text="Tasks")
    task_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    # Add task button
    button = customtkinter.CTkButton(
        master=page,
        text="Add Task",
        command=lambda: switch_page(show_form())
    )
    button.pack(pady=10)


    # Load tasks
    my_image = customtkinter.CTkImage(
        light_image=Image.open('./ui_assets/easy_sword.png'),
        dark_image=Image.open('./ui_assets/easy_sword.png'),
        size=(30, 30)
    )
    conn = get_conn()
    tasks = get_all_tasks(conn)
    
    for task in tasks:
        print(task)
        task_text = f"{task['name']} - {task['description']}  (Type: {task['type_name']})  (Difficulty: {task['difficulty_name']}) completed? {task['completed']}"
        if task['archived']:
            task_text += " [ARCHIVED]"

        # Row frame for label + button
        row = customtkinter.CTkFrame(task_scroll)
        row.pack(fill="x", pady=5, padx=10)

        # Task label
        label = customtkinter.CTkLabel(
            master=row,
            text=task_text,
            image=my_image,
            compound="left",
            anchor="w",
            justify="left",
            padx=5
        )
        label.pack(side="left", fill="x", expand=True)

        # Delete button with late binding fix
        del_button = customtkinter.CTkButton(
            master=row,
            text="Delete",
            fg_color="red",
            width=60,
            command=lambda task_id=task['id']: delete_and_refresh(conn, task_id)
        )
        del_button.pack(side="right", padx=5)

    return page

def delete_and_refresh(conn, task_id):
    delete_task(conn,task_id)
    switch_page(show_tasks())
# ---- Fetch and display tasks ----
def show_form():
    page = customtkinter.CTkFrame(master=__page_container)
    header = customtkinter.CTkLabel(page, text="Add Task", font=("Arial", 20))
    header.pack(pady=10)

    # Form UI goes here...
    form_area = customtkinter.CTkScrollableFrame(master=page, label_text="Task Details")
    form_area.pack(pady=10, padx=10, fill="both", expand=True)
    form_name = customtkinter.CTkEntry(form_area,placeholder_text="name")
    form_description = customtkinter.CTkEntry(form_area,placeholder_text="Description" )
    form_archived = customtkinter.CTkCheckBox(form_area,text="archived?")
    form_type = customtkinter.CTkEntry(form_area,placeholder_text="typeid")
    form_difficulty = customtkinter.CTkEntry(form_area,placeholder_text="difficulty_id")
    
    form_name.pack()
    form_description.pack()
    form_archived.pack()
    form_type.pack()
    form_difficulty.pack()
    conn = get_conn()

    def submit_task():
        form_data = {
            "name": form_name.get(),
            "description": form_description.get(),  # lowercase 'description' for consistency
            "archived": int(form_archived.get()),  # CTkCheckBox returns 0 or 1
            "type_id": int(form_type.get()) if form_type.get().isdigit() else None,
            "difficulty_id": int(form_difficulty.get()) if form_difficulty.get().isdigit() else None
        }
        print("Submitting:", form_data)
        create_task(conn, form_data)
        switch_page(show_tasks())  # return to tasks page

    submit_btn = customtkinter.CTkButton(
        master=page,
        text="Submit",
        command=submit_task
    )
    # Back button
    back_btn = customtkinter.CTkButton(
        master=page,
        text="← Back to Tasks",
        command=lambda: switch_page(show_tasks())
    )
    submit_btn.pack(pady=10)
    back_btn.pack(pady=10)
    
    return page

def button_to_form(master):
    frame = customtkinter.CTkFrame(master=master)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    button = customtkinter.CTkButton(
    master= frame,
    width = 140,
    height = 28,
    corner_radius = 6,
    border_width=3,
    border_spacing=2,
    text = "Add Task",
    image = None,
    state = "normal",
    hover = True,
    command= show_form,
    compound  = "left",
    anchor = "center"
    )
    button.pack(padx = 10, pady=10)

def loop():
    init()
    switch_page(show_tasks())
    __root.mainloop()

loop()

