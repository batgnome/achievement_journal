import customtkinter
from PIL import Image
from backend.sql_connector_3 import get_conn
from backend.tasks_dao import get_all_tasks, create_task, delete_task
from backend.type_dao import get_all_types, create_type, delete_type
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
    button_1 = customtkinter.CTkButton(
        master=__page_container,
        text="Show Tasks",
        command=lambda: switch_page(show_tasks())
    )
    button_1.pack(pady=10)
    button_1 = customtkinter.CTkButton(
        master=__page_container,
        text="Show Types",
        command=lambda: switch_page(show_types())
    )
    button_1.pack(pady=10)
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
        command=lambda: switch_page(show_task_form())
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
            command=lambda task_id=task['id']: delete_and_refresh(conn, task_id,"task")
        )
        del_button.pack(side="right", padx=5)

    return page
# ---- Fetch and display tasks ----
def show_types():
    page = customtkinter.CTkFrame(master=__page_container)
    header = customtkinter.CTkLabel(page, text="Your types", font=("Arial", 20))
    header.pack(pady=10)

    type_scroll = customtkinter.CTkScrollableFrame(master=page, label_text="types")
    type_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    # Add task button
    button = customtkinter.CTkButton(
        master=page,
        text="Add Type",
        command=lambda: switch_page(show_type_form())
    )
    button.pack(pady=10)

    conn = get_conn()
    types = get_all_types(conn)
    
    for type in types:
        type_text = f"{type['name']}"
       
        # Row frame for label + button
        row = customtkinter.CTkFrame(type_scroll)
        row.pack(fill="x", pady=5, padx=10)

        # Task label
        label = customtkinter.CTkLabel(
            master=row,
            text=type_text,
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
            command=lambda type_id=type['id']: delete_and_refresh(conn, type_id, "type")
        )
        del_button.pack(side="right", padx=5)

    return page
def delete_and_refresh(conn, id, type):
    if type == "type":
        delete_type(conn,id)
        switch_page(show_types())
    if type == "task":
        delete_task(conn,id)
        switch_page(show_tasks())
# ---- Fetch and display tasks ----
def show_task_form():
    page = customtkinter.CTkFrame(master=__page_container)
    header = customtkinter.CTkLabel(page, text="Add Task", font=("Arial", 20))
    header.pack(pady=10)
    conn = get_conn()
    types = get_all_types(conn)
   
    
    # Form UI goes here...
    form_area = customtkinter.CTkScrollableFrame(master=page, label_text="Task Details")
    form_area.pack(pady=10, padx=10, fill="both", expand=True)
    form_name = customtkinter.CTkEntry(form_area,placeholder_text="name")
    form_description = customtkinter.CTkEntry(form_area,placeholder_text="Description" )
    form_archived = customtkinter.CTkCheckBox(form_area,text="archived?")

    type_name_to_id = {t['name']: t['id'] for t in types}
    type_names = list(type_name_to_id.keys())  # this goes into the dropdown
    type_optionmenu = customtkinter.CTkOptionMenu(form_area, values=type_names)
    form_difficulty = customtkinter.CTkEntry(form_area,placeholder_text="difficulty_id")
    
    form_name.pack()
    form_description.pack()
    form_archived.pack()
    type_optionmenu.pack()
    type_optionmenu.set(type_names[0])  # default to first option
    form_difficulty.pack()
    
    print("here! " , type_optionmenu.get())
    def submit_task():
        selected_type_name = type_optionmenu.get()
        selected_type_id = type_name_to_id.get(selected_type_name)

        form_data = {
            "name": form_name.get(),
            "description": form_description.get(),
            "archived": int(form_archived.get()),
            "type_id": selected_type_id,
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

def show_type_form():
    page = customtkinter.CTkFrame(master=__page_container)
    header = customtkinter.CTkLabel(page, text="Add Type", font=("Arial", 20))
    header.pack(pady=10)

    # Form UI goes here...
    form_area = customtkinter.CTkScrollableFrame(master=page, label_text="Type Details")
    form_area.pack(pady=10, padx=10, fill="both", expand=True)
    form_name = customtkinter.CTkEntry(form_area,placeholder_text="name")

    
    form_name.pack()

    conn = get_conn()

    def submit_type():
        form_data = form_name.get()
        
        print("Submitting:", form_data)
        create_type(conn, form_data)
        switch_page(show_types())  # return to tasks page

    submit_btn = customtkinter.CTkButton(
        master=page,
        text="Submit",
        command=submit_type
    )
    # Back button
    back_btn = customtkinter.CTkButton(
        master=page,
        text="← Back to Tasks",
        command=lambda: switch_page(show_types())
    )
    submit_btn.pack(pady=10)
    back_btn.pack(pady=10)
    
    return page

def loop():
    init()
    switch_page(show_tasks())
    __root.mainloop()

loop()

