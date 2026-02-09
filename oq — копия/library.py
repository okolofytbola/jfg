import os
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self,name):
        self._name = name 

    @abstractmethod
    def get_role(self): 
        pass 

class Librarian(Person):
    def get_role(self):
        return "Библиотекарь"
    def __init__(self, name,password):
        super().__init__(name)
        self.password=password

class User(Person):
    def get_role(self):
        return "Пользователь"
    def __init__(self, name):
        super().__init__(name)
        self.borrowed_books=[]

class Book:
    def __init__(self,title,author):
        self.title=title
        self.author = author
        self.available=True

    def __str__(self):
        if self.available:
            return f"'{self.title}'-{self.author}(доступна)"
        else:
            return f"'{self.title}'-{self.author}(выдана)"
        
class Library():
    def __init__(self):
        self.books=[]
        self.users=[]
        self.librarian=Librarian("Молоков","228")
        self.current_user=None

        self.load_data()

    def login(self,name,password):
        if name ==self.librarian._name and password == self.librarian.password:
            self.current_user=self.librarian
            print("Вы вошли как библиотекарь")
            return True
        print("Ошибка входа!")
        return False
    def login_user(self,name):
        name=name.strip()

        for user in self.users:
            if user._name==name:
                self.current_user=user
                print(f"Добро пожаловать,{name}")
                return True
        print(f"Пользователь {name} не найден")
        return False
    
    def logout(self):
        self.current_user=None
        print("Вы вышли из системы")

    def add_book(self):
        if not self.current_user:
            print("Сначала войдите в систему")
            return
        print("\n Добавление книги")
        title = input("Введите название книги")
        author = input("Введите автора книги")
        new_book = Book(title,author)
        self.books.append(new_book)
        print(f"Книга '{title}' успешно добавлена!")

    def remove_book(self):
        if not self.current_user:
            print("Сначала войдите в систему")
            return
        print("\nУдаление книги")
        title = input("Введите название книги")
        for book in self.books:
            if book.title.lower()==title.lower():
                if not book.available:
                    print("Ошибка: книга выдана,нельзя удалить")
                    return
                
                self.books.remove(book)
                print(f"Книга '{title}' удалена!")
                return
        print("Книга не найдена")

    def register_user(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return
        name = input("Введите имя нового пользователя: ")
        for user in self.users:
            if user._name==name:
                print("Пользователь с таким именем уже существует!")
                return

        new_user=User(name)
        self.users.append(new_user)
        print(f"Пользователь '{name}' зарегистрирован!")

    def show_all_users(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return
        print("\n Все пользователи")
        if not self.users:
            print("Нету пользователей")
            return
        for i,user in enumerate(self.users,1):
            print(f"{i}.{user._name}")
        
    
    def show_all_books(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return
        print("\n Все книги")
        if not self.books:
            print("Книг нету")
            return
        for i,book in enumerate(self.books,1):
            print(f"{i}.{book}")

    def show_available_books(self):
    
        if not isinstance(self.current_user, User):
            print("Эта функция только для пользователей!")
            return
    
        print("\n ДОСТУПНЫЕ КНИГИ ")
    
        found = False  
    
        for book in self.books:
            if book.available:  
                print(f"- {book}")
                found = True
    
        if not found:
            print("Нет доступных книг")

    def take_book(self):
    
        if not isinstance(self.current_user, User):
            print("Эта функция только для пользователей!")
            return
    
        print("\n ВЗЯТЬ КНИГУ ")
  
        self.show_available_books()
 
        title = input("Введите название книги, которую хотите взять: ").strip()
    
    
        for book in self.books:
            if book.title.lower() == title.lower():
                if book.available:
                    book.available = False
                    self.current_user.borrowed_books.append(title)
                    print(f"Вы взяли книгу: '{title}'")
                    return
                else:
                    print("Книга уже выдана!")
                    return
    
        print("Книга не найдена!")
    def save_data(self):
    
    
        with open('books.txt', 'w',encoding='utf-8') as f:
            for book in self.books:
             f.write(f"{book.title},{book.author},{book.available}\n")
    
    
        with open('users.txt', 'w',encoding='utf-8') as f:
            for user in self.users:
                f.write(f"{user._name}\n")
    
        print(" Данные сохранены")

    def load_data(self):
    
    
        try:
            with open('books.txt', 'r',encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        title, author, available = parts[0], parts[1], parts[2] == 'True'
                        book = Book(title, author)
                        book.available = available
                        self.books.append(book)
        except:
            print("Нет файла books.txt, создаём тестовые книги")
            self.books.append(Book("Война и мир", "Толстой"))
            self.books.append(Book("Трудно быть богом", "Братья Стругацкие"))
    
  
        try:
            with open('users.txt', 'r',encoding='utf-8') as f:
                for line in f:
                    name = line.strip()
                    if name:
                        self.users.append(User(name))
        except:
            print("Нет файла users.txt, создаём тестового пользователя")
            self.users.append(User("Денчик"))

    


    def show_menu(self):
        if self.current_user:
            print(f"Вы вошли как: {self.current_user.get_role()}")
            if isinstance(self.current_user,Librarian):
                print("1. Добавить книгу")
                print("2. Удалить книгу")
                print("3. Зарегистрировать пользователя")
                print("4. Показать всех пользователей")
                print("5. Показать все книги")
                print("6. Выйти из системы")
            elif isinstance(self.current_user,User):
                print("1. Показать доступные книги")  
                print("2. Взять книгу")               
                print("3. Выйти из системы")

        else:
           
            print("1. Войти как библиотекарь")
            print("2. Войти как пользователь")
            print("3. Выйти из программы")

    def run(self):
        print("БИБЛИОТЕЧНАЯ СИСТЕМА ")

        while True:
            self.show_menu()
            choice=input("\n Выберите действие")
            if not self.current_user:
                if choice == "1":
                    name=input("Имя").strip()
                    password=input("Пароль").strip()
                    self.login(name,password)
                elif choice == "2":
                    name=input("Ваше имя :").strip()
                    self.login_user(name)
                elif choice == "3":
                    print("Выход")
                    break
                else:
                    print("Неверный выбор")

            else:
                if isinstance(self.current_user, Librarian):
                    if choice == "1":
                        self.add_book()
                    elif choice == "2":
                        self.remove_book()
                    elif choice == "3":
                        self.register_user()
                    elif choice == "4":
                        self.show_all_users()
                    elif choice == "5":
                        self.show_all_books()
                    elif choice == "6":
                        self.save_data()
                        self.logout()
                    else:
                        print("Неверный выбор!")
                elif isinstance(self.current_user, User):
                    if choice=="1":
                        self.show_available_books()
                    elif choice=="2":
                        self.take_book()
                    elif choice=="3":
                        self.save_data()
                        self.logout()
                else:
                    print("Неверный выбор")
library = Library()
library.run()



           
