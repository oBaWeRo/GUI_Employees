import tkinter
import tkinter.messagebox
import sqlite3


class EmployeeDetails:

  def __init__(self):
    self.__main_window = tkinter.Tk()
    self.__build_main_window()
    tkinter.mainloop()

  def __build_main_window(self): # Создать все окна
    self.__create_prompt_label()
    self.__build_listbox_frame()
    self.__create_quit_button()

  def __create_prompt_label(self): #Создать таблицу в верху окна приложения tkinter.
    self.employee_prompt_label = tkinter.Label(self.__main_window,
                                               text='Выберите сотрудника')
    self.employee_prompt_label.pack(side='top')

  def __build_listbox_frame(self): #Создать окно со списком ,прокруткой страницы и именами сотрудников.
    self.listbox_frame = tkinter.Frame(self.__main_window)
    self.__setup_listbox()
    self.__create_scrollbar()
    self.__populate_listbox()
    self.listbox_frame.pack()

  def __setup_listbox(self): # Задать настройки для списка Listbox.
    self.employee_listbox = tkinter.Listbox(self.listbox_frame, height=6, width=0,selectmode='Single')
    self.employee_listbox.bind('<<ListboxSelect>>', self.__get_details)
    self.employee_listbox.pack(side='left')

  def __create_scrollbar(self): # Создать с правой стороны вертикальную прокрутку.
    self.scrollbar = tkinter.Scrollbar(self.listbox_frame, orient=tkinter.VERTICAL)
    self.scrollbar.config(command=self.employee_listbox.yview)
    self.employee_listbox.config(yscrollcommand=self.scrollbar.set)
    self.scrollbar.pack(side='right', fill=tkinter.Y)

  def __populate_listbox(self): #Заполнить список Listbox сотрудниками.
    for employee in self.__get_employees():
      self.employee_listbox.insert(tkinter.END, employee)

  def __create_quit_button(self): # Создать кнопку выхода.
    self.quit_button = tkinter.Button(self.__main_window, text='EXIT'
                                      , command=self.__main_window.destroy)
    self.quit_button.pack()

  def __get_employees(self): # Получить из базы данных имена сотрудников.
    with sqlite3.connect(r'employees.db') as conn:
      cur = conn.cursor()

      cur.execute('PRAGMA foreign_keys=ON')
      cur.execute(''' Select Name From Employees''')
      employee_list = [n[0] for n in cur.fetchall()]

    return employee_list

  def __get_details(self, event): #Получить все данные о сотрудниках из базы данных.
    listbox_index = self.employee_listbox.curselection()
    selected_emp = self.employee_listbox.get(listbox_index)

    with sqlite3.connect(r'employees.db') as conn:
      cur = conn.cursor()

      cur.execute('PRAGMA foreign_keys=ON')
      cur.execute(''' Select Employees.name,
      Employees.position,
      Departments.DepartmentName,
      Locations.City

      From Employees,Departments,Locations

      Where Employees.Name == ? AND 
      Employees.DepartmentID == Departments.DepartmentID AND
      Employees.LocationID == Locations.LocationID''',
                  (selected_emp,))
      results = cur.fetchone()

      self.__display_details(name=results[0], position=results[1],
                             department=results[2], location=results[3])

  def __display_details(self, name, position, department, location): # С помощью функции обратного вызова и импортированного модуля tkinter.messagebox
    # выводим всю информацию о сотруднике которого выбрали из списка Listbox.

    tkinter.messagebox.showinfo('Информация о сотруднике',
                                f'Имя: {name}\n'
                                f'Должность: {position}\n'
                                f'Отдел: {department}\n'
                                f'Местоположение: {location}')

#Точка входа.
if __name__ == '__main__':
  my_gui = EmployeeDetails()