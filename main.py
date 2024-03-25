import customtkinter
import sqlite3 as sq
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("500x540")
app.title("Scoring App")
app.iconbitmap("icon.ico")

button_font = customtkinter.CTkFont(family="Comic Sans", size=16, weight='bold')
label_font = customtkinter.CTkFont(family="Comic Sans", size=24, weight='bold')
small_label_font = customtkinter.CTkFont(family="Comic Sans", size=16, weight='bold')
question_label_font = customtkinter.CTkFont(family='Comic Sans', size=12, weight='bold')


def data_list(entry_check_frame, match_phrase):
    entry_check_frame.forget()
    data_list_frame = customtkinter.CTkFrame(master=app)
    data_list_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def delete_data_btn():
        cursor.execute("SELECT * FROM client WHERE passport_series = ?", (match_phrase,))
        row_delete = cursor.fetchone()

        if row_delete:
            cursor.execute("DELETE FROM client WHERE passport_series = ?", (match_phrase,))
            conn.commit()
            conn.close()
            CTkMessagebox(message="Анкета успешно удалена",
                          icon="check", option_1="Ок")
            data_btn_back()
        else:
            CTkMessagebox(title="Ошибка", message="Удаление анкеты невозможно",
                          icon="cancel")
            conn.close()
            return

    def data_btn_back():
        data_list_frame.forget()
        start_frame.pack(pady=20, padx=20, fill="both", expand=True)

    test_label = customtkinter.CTkLabel(master=data_list_frame,
                                        text='Анкета заемщика',
                                        font=label_font)
    test_label.pack(pady=10)

    conn = sq.connect('scoring.db')
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS client (
                        id INTEGER PRIMARY KEY,
                        full_name TEXT,
                        passport_series TEXT,
                        debt_status TEXT,
                        income INTEGER,
                        real_estate_expense INTEGER,
                        car_expense INTEGER,
                        family_expense INTEGER,
                        borrower_status TEXT
                    )
                ''')
    query = f"SELECT * FROM client WHERE passport_series = '{match_phrase}'"
    cursor.execute(query)
    row = cursor.fetchone()

    if row:
        data_fullname = row[1]
        data_passport_series = row[2]
        data_debt_status = row[3]
        data_income = row[4]
        data_estate = row[5]
        data_car = row[6]
        data_fam = row[7]
        data_status = row[8]

        data_label_1 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=small_label_font,
                                              text=f'ФИО: {data_fullname}')
        data_label_1.pack()
        data_label_2 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=small_label_font,
                                              text=f'Серия и номер паспорта: {data_passport_series}')
        data_label_2.pack()
        data_label_3 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=small_label_font,
                                              text=f'Наличие задолженности: {data_debt_status}')
        data_label_3.pack()
        data_label_4 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=small_label_font,
                                              text=f'Ежемесячный доход: {data_income}₽')
        data_label_4.pack()
        data_label_5 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=small_label_font,
                                              text=f'Расходы на недвижимость: {data_estate}₽')
        data_label_5.pack()
        data_label_6 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=small_label_font,
                                              text=f'Расходы на транспорт: {data_car}₽')
        data_label_6.pack()
        data_label_7 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=small_label_font,
                                              text=f'Расходы на семью: {data_fam}₽')
        data_label_7.pack()
        data_label_8 = customtkinter.CTkLabel(master=data_list_frame,
                                              font=label_font,
                                              text=f'{data_status}')
        data_label_8.pack(pady=10)
        if data_status == 'Кредит одобрен':
            data_label_8.configure(text_color='#108500')
        else:
            data_label_8.configure(text_color='#850000')

        data_delete_btn = customtkinter.CTkButton(master=data_list_frame,
                                                  width=220, height=60,
                                                  text='Удалить анкету',
                                                  font=button_font,
                                                  fg_color='#850000',
                                                  hover_color='#570000',
                                                  command=delete_data_btn)
        data_delete_btn.pack(pady=20)

        data_back_btn = customtkinter.CTkButton(master=data_list_frame,
                                                width=220, height=60,
                                                text='Назад',
                                                font=button_font,
                                                fg_color='#850000',
                                                hover_color='#570000',
                                                command=data_btn_back)
        data_back_btn.pack(pady=10)

    else:
        CTkMessagebox(title="Ошибка", message="Анкета не найдена",
                      icon="cancel")
        data_btn_back()

# Check Data Frame


def check_data_button():
    start_frame.forget()
    entry_check_frame = customtkinter.CTkFrame(master=app)
    entry_check_frame.pack(pady=20, padx=20, fill="both", expand=True)

    check_data_label = customtkinter.CTkLabel(master=entry_check_frame,
                                              justify=customtkinter.CENTER,
                                              text="Введите серию и номер паспорта",
                                              font=small_label_font)
    check_data_label.pack(pady=30)

    check_field = customtkinter.CTkEntry(master=entry_check_frame,
                                         width=240, height=30,
                                         placeholder_text="1234 567890",
                                         justify=customtkinter.CENTER)
    check_field.pack(pady=30)

    def find_data_db():
        try:
            int(check_field.get().replace(" ", ""))
        except ValueError:
            CTkMessagebox(title="Ошибка", message="Недопустимые символы в поле для числовых значений",
                          icon="cancel")
            return
        match_phrase = check_field.get()
        data_list(entry_check_frame, match_phrase)

    find_data_btn = customtkinter.CTkButton(master=entry_check_frame,
                                            width=220, height=60,
                                            text='Найти', font=button_font,
                                            command=find_data_db)
    find_data_btn.pack(pady=20)

    def back_find():
        entry_check_frame.forget()
        start_frame.pack(pady=20, padx=20, fill="both", expand=True)

    back_entry_button = customtkinter.CTkButton(master=entry_check_frame,
                                                width=220, height=60,
                                                text='Назад', font=button_font,
                                                command=back_find,
                                                fg_color='#850000',
                                                hover_color='#570000')
    back_entry_button.pack(pady=20)


def create_data():
    start_frame.forget()
    create_data_frame = customtkinter.CTkScrollableFrame(master=app)
    create_data_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def save_from_entry():
        try:
            int(entry_2.get().replace(" ", ""))
            int(entry_3.get())
            int(entry_4.get())
            int(entry_5.get())
            int(entry_6.get())
        except ValueError:
            CTkMessagebox(title="Ошибка", message="Недопустимые символы в полях для числовых значений",
                          icon="cancel")
            return
        conn = sq.connect('scoring.db')
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS client (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    passport_series TEXT,
                    debt_status TEXT,
                    income INTEGER,
                    real_estate_expense INTEGER,
                    car_expense INTEGER,
                    family_expense INTEGER,
                    borrower_status TEXT
                )
            ''')

        match_pass = entry_2.get()
        cursor.execute('''
            SELECT passport_series FROM client
            WHERE passport_series = ?
        ''', (match_pass,))
        result = cursor.fetchall()

        if result:
            CTkMessagebox(title="Ошибка", message="В базе данных уже есть такой пользователь", icon="cancel")
            conn.close()
        else:
            client_status = label_9.cget('text')
            if client_status == 'Не определено':
                CTkMessagebox(title="Ошибка", message="Невозможно сохранить анкету с неопределенным статусом",
                              icon="cancel")
                conn.close()
            else:
                fullname = entry_1.get()
                pass_num = entry_2.get()
                debt = combobox_1.get()
                income = entry_3.get()
                estate_cost = entry_4.get()
                auto_cost = entry_5.get()
                fam_cost = entry_6.get()

                cursor.execute('''
                        INSERT INTO client (full_name, passport_series, debt_status, income, real_estate_expense,
                        car_expense, family_expense, borrower_status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                    fullname, pass_num, debt, income, estate_cost, auto_cost,
                    fam_cost, client_status))

                conn.commit()
                conn.close()
                CTkMessagebox(title='Успех', message="Анкета успешно сохранена",
                              icon="check", option_1="Ок")

    def calculate_value():
        mrot = 18000
        debt = combobox_1.get()
        income = entry_3.get()
        estate_cost = entry_4.get()
        auto_cost = entry_5.get()
        fam_cost = entry_6.get()

        try:
            int(entry_2.get().replace(" ", ""))
            int(entry_3.get())
            int(entry_4.get())
            int(entry_5.get())
            int(entry_6.get())
        except ValueError:
            CTkMessagebox(title="Ошибка", message="Недопустимые символы в полях для числовых значений",
                          icon="cancel")
            return

        if debt == 'Есть задолженность':
            label_9.configure(text='Отказ',
                              text_color='#850000')
        if debt == 'Не определено':
            label_9.configure(text='Не определено')
        elif debt == 'Нет задолженности':
            if int(income) >= mrot:
                if int(estate_cost) < (int(income) / 4):
                    if int(auto_cost) < (int(income) / 4):
                        if int(fam_cost) < (int(income) / 4):
                            label_9.configure(text='Кредит одобрен',
                                              text_color='#108500')
                        else:
                            label_9.configure(text='Отказ',
                                              text_color='#850000')
                    else:
                        label_9.configure(text='Отказ',
                                          text_color='#850000')
                else:
                    label_9.configure(text='Отказ',
                                      text_color='#850000')
            else:
                label_9.configure(text='Отказ',
                                  text_color='#850000')

    # Questions Entry

    label_1 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=label_font,
                                     text='Анкета заемщика')
    label_1.pack(pady=10)

    entry_1 = customtkinter.CTkEntry(master=create_data_frame,
                                     width=240, height=30,
                                     placeholder_text="ФИО",
                                     justify=customtkinter.CENTER)
    entry_1.pack()

    label_2 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=small_label_font,
                                     text='Серия и номер паспорта')
    label_2.pack(pady=10)

    entry_2 = customtkinter.CTkEntry(master=create_data_frame,
                                     width=240, height=30,
                                     placeholder_text="1234 567890",
                                     justify=customtkinter.CENTER)
    entry_2.pack()

    label_7 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=small_label_font,
                                     text='Наличие задолженностей')
    label_7.pack(pady=10)

    combobox_1 = customtkinter.CTkComboBox(master=create_data_frame,
                                           values=['Не определено',
                                                   'Нет задолженности',
                                                   'Есть задолженность'],
                                           width=240,
                                           justify=customtkinter.CENTER,
                                           font=small_label_font,
                                           dropdown_font=small_label_font)
    combobox_1.pack()

    label_3 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=small_label_font,
                                     text='Ежемесячный доход, ₽')
    label_3.pack(pady=10)

    entry_3 = customtkinter.CTkEntry(master=create_data_frame,
                                     width=240, height=30,
                                     placeholder_text="0",
                                     justify=customtkinter.CENTER)
    entry_3.insert(0, '0')
    entry_3.pack()

    label_4 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=small_label_font,
                                     text='Расходы на недвижимость, ₽')
    label_4.pack(pady=10)

    entry_4 = customtkinter.CTkEntry(master=create_data_frame,
                                     width=240, height=30,
                                     placeholder_text="0",
                                     justify=customtkinter.CENTER)
    entry_4.insert(0, '0')
    entry_4.pack()

    label_5 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=small_label_font,
                                     text='Расходы на личный транспорт, ₽')
    label_5.pack(pady=10)

    entry_5 = customtkinter.CTkEntry(master=create_data_frame,
                                     width=240, height=30,
                                     placeholder_text="0",
                                     justify=customtkinter.CENTER)
    entry_5.insert(0, '0')
    entry_5.pack()

    label_6 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=small_label_font,
                                     text='Расходы на членов семьи, ₽')
    label_6.pack(pady=10)

    entry_6 = customtkinter.CTkEntry(master=create_data_frame,
                                     width=240, height=30,
                                     placeholder_text="0",
                                     justify=customtkinter.CENTER)
    entry_6.insert(0, '0')
    entry_6.pack()

    label_8 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=small_label_font,
                                     text='Статус заемщика:')
    label_8.pack(pady=10)

    label_9 = customtkinter.CTkLabel(master=create_data_frame,
                                     font=label_font,
                                     text='Не определено')
    label_9.pack(pady=10)

    calculate_button = customtkinter.CTkButton(master=create_data_frame,
                                               width=220, height=60,
                                               text='Рассчитать',
                                               font=button_font,
                                               command=calculate_value)
    calculate_button.pack(pady=10)

    save_button = customtkinter.CTkButton(master=create_data_frame,
                                          width=220, height=60,
                                          text='Сохранить',
                                          font=button_font,
                                          command=save_from_entry)
    save_button.pack(pady=10)

    def back_entry():
        create_data_frame.pack_forget()
        start_frame.pack(pady=20, padx=20, fill="both", expand=True)

    back_entry_button = customtkinter.CTkButton(master=create_data_frame,
                                                width=220, height=60,
                                                text='Назад',
                                                font=button_font,
                                                command=back_entry,
                                                fg_color='#850000',
                                                hover_color='#570000')
    back_entry_button.pack(pady=10)


# Start_frame Configure

start_frame = customtkinter.CTkFrame(master=app)
start_frame.pack(pady=20, padx=20, fill="both", expand=True)
start_label = customtkinter.CTkLabel(master=start_frame,
                                     justify=customtkinter.CENTER,
                                     text="Scoring App",
                                     font=label_font)
start_label.pack(pady=30)

btn_check_data = customtkinter.CTkButton(master=start_frame,
                                         width=220, height=60,
                                         text='Проверить данные',
                                         font=button_font,
                                         command=check_data_button)
btn_check_data.pack(expand=1)
btn_new_data = customtkinter.CTkButton(master=start_frame,
                                       width=220, height=60,
                                       text='Ввести данные',
                                       font=button_font,
                                       command=create_data)
btn_new_data.pack(expand=1)

app.mainloop()
