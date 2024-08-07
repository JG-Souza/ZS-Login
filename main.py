import customtkinter as ctk
from PIL import Image as PILImage, ImageTk
from tkinter import *
from tkinter import messagebox
import sqlite3 as sq 

class BackEnd():
    def conecta_db(self):
        self.conn = sq.connect("database.db")
        self.cursor = self.conn.cursor()

    def desconecta_db(self):
        self.conn.close()

    def cria_tabela(self):
        self.conecta_db()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
''')
        self.conn.commit()
        self.desconecta_db()

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        self.conecta_db()
        

        try:
            self.cursor.execute('''SELECT * FROM Usuarios WHERE Email = ?''', (self.email_cadastro,))
            self.verifica_cadastro = self.cursor.fetchone()
            if self.verifica_cadastro is not None:
                messagebox.showwarning(title='ZS Login', message='Este email já está em uso')
                return
            else:

                if (self.username_cadastro == '' or self.email_cadastro == '' or self.senha_cadastro == '' or self.confirma_senha_cadastro == ''):
                    messagebox.showerror(title='ZS Login', message='ERRO!!\nPor favor preencha todos os campos')
                elif (len(self.username_cadastro) < 4):
                    messagebox.showwarning(title='ZS Login', message='O nome de usuario deve conter pelo menos 4 caracteres')

                elif ('@' not in self.email_cadastro):
                    messagebox.showwarning(title='ZS Login', message='Seu email deve conter @')

                elif (len(self.senha_cadastro) < 4):
                    messagebox.showwarning(title='ZS Login', message='A senha deve conter pelo menos 4 caracteres')
                elif (self.senha_cadastro != self.confirma_senha_cadastro):
                    messagebox.showerror(title='ZS Login', message='ERRO!!\nAs senhas não coincidem, tente novamente')
                else:
                    self.cursor.execute('''
                        INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
                        VALUES (?, ?, ?, ?)
                            ''', (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
                    self.conn.commit()
                    messagebox.showinfo(title='ZS Login', message=f"Parabens {self.username_cadastro}\nVocê se cadastrou com sucesso")
                    self.desconecta_db()
                    self.limpa_entry_cadastro()

        except:
            messagebox.showerror(title='ZS Login', message='Erro no processamento do seu cadastro\nPor favor, tente novamente')
            self.desconecta_db()

    def verifica_login(self):
        self.email_login = self.email_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        self.conecta_db()
        self.cursor.execute('''SELECT * FROM Usuarios WHERE Email = ? AND Senha = ?''', (self.email_login, self.senha_login))


        # Percorrendo a Tabela Usuarios
        self.verifica_dados = self.cursor.fetchone()

        try:
            if (self.email_login == '' or self.senha_login == ''):
                messagebox.showwarning(title='ZS Login', message='Preencha todos os campos, por favor!')
            

            elif (self.email_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title='ZS Login', message=f"Parabens {self.verifica_dados[1]}\nLogin feito com sucesso")
                self.desconecta_db()
                self.limpa_entry_login()
        except:
            messagebox.showerror(title='ZS Login', message='Email ou senha incorretos!')
            self.desconecta_db()
            

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        self.appearance_mode()
        self.cria_tabela()


    # Configurando a janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("ZS Login")
        self.resizable(False, False)

    # Trocando tema
    def appearance_mode(self):
        ctk.set_appearance_mode('light')

    
    
    def visualizar_senha_login(self):
        if self.senha_visivel:
            self.senha_login_entry.configure(show='*')
        else:
            self.senha_login_entry.configure(show='')

        self.senha_visivel = not self.senha_visivel

    def visualizar_senha_cadastro(self):
        if self.senha_visivel:
            self.senha_cadastro_entry.configure(show='*')
            self.confirma_senha_entry.configure(show='*')
        else:
            self.senha_cadastro_entry.configure(show='')
            self.confirma_senha_entry.configure(show='')

        self.senha_visivel = not self.senha_visivel




    def tela_de_login(self):
        # Caso self tenha um atributo 'btn_login_back', então a linha de baixo será executada
        if hasattr(self, 'btn_login_back'):
            self.btn_login_back.grid_forget() 

        # Variável para rastrear o estado da senha
        self.senha_visivel = False


        # Trabalhando com as imagens
        image_path = "images/img-log.png"
        self.img = PILImage.open(image_path)

        new_width = 280
        new_height = 300
        resized_image = self.img.resize((new_width, new_height))
        tk_image = ImageTk.PhotoImage(resized_image)

        self.lb_img = ctk.CTkLabel(self, text=None, image=tk_image)
        self.lb_img.image = tk_image
        self.lb_img.grid(row=1, column=0, padx=10)

        # Titulo da nossa plaforma
        self.title = ctk.CTkLabel(self, text='Faça o seu Login ou Cadastre-se\nna nossa plataforma para acessar\nos nossos servicos', font=('Century Gothic', 14, 'bold'))
        self.title.grid(row=0, column=0,padx=10,  pady=10)

        # Frame do Formulário de Login
        self.frame_login = ctk.CTkFrame(self, width=350, height= 380 )
        self.frame_login.place(x=350, y=10)

        # Colocando widgets dentro do frame - formulario de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text='Faça seu Login', font=('Century Gothic', 20, 'bold'))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.email_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text='Seu email', font=('Century Gothic', 16), corner_radius=15)
        self.email_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text='Sua senha', font=('Century Gothic bold', 16), corner_radius=15, show='*')
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, width=300, text='Clique para ver a senha', font=('Century Gothic bold', 14), corner_radius=20, fg_color='#93e2a9', hover_color='#698b7a', command=self.visualizar_senha_login)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        self.btn_login= ctk.CTkButton(self.frame_login, width=300, text='Login', font=('Century Gothic bold', 16), corner_radius=15, fg_color='#93e2a9', hover_color='#698b7a', text_color='#2c3a3e', command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(self.frame_login, text='Ainda não tem conta?\nClique para se cadastrar', font=('Century Gothic', 14))
        self.span.grid(row=5, column=0, padx=10, pady=10)

        self.btn_cadastro= ctk.CTkButton(self.frame_login, width=300, text='Cadastre-se', font=('Century Gothic bold', 16), corner_radius=15, fg_color='#93e2a9', hover_color='#698b7a', text_color='#2c3a3e', command= self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, padx=10, pady=10)


    def tela_de_cadastro(self):
        # Remover o formulario de login
        self.frame_login.place_forget()

        # Variável para rastrear o estado da senha
        self.senha_visivel = False

        # Frame de formulario de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height= 380 )
        self.frame_cadastro.place(x=350, y=10)

        # Criando nosso titiulo
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text='Faça seu cadastro', font=('Century Gothic', 20, 'bold'))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        # Criando os widgets da tela de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Seu nome de usuario', font=('Century Gothic', 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Seu email', font=('Century Gothic bold', 16), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=10)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Sua senha', font=('Century Gothic', 16), corner_radius=15, show='*')
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=10)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Confirme sua senha', font=('Century Gothic bold', 16), corner_radius=15, show='*')
        self.confirma_senha_entry.grid(row=4, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, width=300, text='Clique para ver a senha', font=('Century Gothic bold', 14), corner_radius=20, fg_color='#93e2a9', hover_color='#698b7a', command=self.visualizar_senha_cadastro)
        self.ver_senha.grid(row=5, column=0, padx=10, pady=10)


        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, text='Cadastre-se', font=('Century Gothic bold', 16), corner_radius=15, fg_color='#93e2a9', hover_color='#698b7a', text_color='#2c3a3e', command= self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, padx=10, pady=10)

        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text='Voltar ao Login', font=('Century Gothic bold', 16), corner_radius=15, fg_color='#93e2a9', hover_color='#698b7a', text_color='#2c3a3e', command= self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, padx=10, pady=10)

    def limpa_entry_cadastro(self):
        self.email_cadastro_entry.delete(0, END)
        self.username_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    def limpa_entry_login(self):
        self.email_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)
        



if __name__=='__main__':
    app = App()
    app.mainloop()