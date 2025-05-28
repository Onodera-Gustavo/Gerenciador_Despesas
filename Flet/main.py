import flet as ft
from flet import *
import requests
import json
import os
from datetime import datetime
from inicial import mostrar_tela_inicial



def main(page: ft.Page):
    page.title = "Agiotagem tracker"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK87

    page.fonts = {
        "font": "fonts/Montserrat-Regular.ttf"
    }

    # Campos fora da função
    nome_input = ft.TextField(label="Nome de usuário", color=ft.Colors.WHITE, border_color=ft.Colors.WHITE)
    email_input = ft.TextField(label="Cadastro*", color=ft.Colors.WHITE, border_color=ft.Colors.WHITE)
    senha_input = ft.TextField(label="Senha*", password=True, color=ft.Colors.WHITE, border_color=ft.Colors.WHITE)
    
    alerta_dialog = ft.AlertDialog(modal=True)

    mensagem_erro = ft.Text("", color=ft.Colors.RED_400, size=12, visible=False)

    def salvar_dados(e):
        if not email_input.value.strip() or not senha_input.value.strip():
            email_input.error_text = "Campo obrigatório" if not email_input.value.strip() else None
            senha_input.error_text = "Campo obrigatório" if not senha_input.value.strip() else None
            mensagem_erro.visible = False
            page.update()
            return

        email_input.error_text = None
        senha_input.error_text = None

        usuario = {
            "nome": nome_input.value,
            "cadastro": email_input.value,
            "senha": senha_input.value
        }

        # Carrega o arquivo
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as f:
                try:
                    dados = json.load(f)
                except json.JSONDecodeError:
                    dados = []
        else:
            dados = []

        # Verifica se o cadastro já existe
        for u in dados:
            if u["cadastro"] == usuario["cadastro"]:
                if u["senha"] == usuario["senha"]:
                    mensagem_erro.visible = False
                    page.update()
                    print("Login bem-sucedido:", u)
                    mostrar_tela_inicial(page)
                    return
                else:
                    mensagem_erro.value = "Senha incorreta para este cadastro."
                    mensagem_erro.visible = True
                    page.update()
                    return

        # Novo usuário
        dados.append(usuario)
        with open("usuarios.json", "w") as f:
            json.dump(dados, f, indent=4)

        mensagem_erro.visible = False
        print("Novo usuário salvo:", usuario)
        mostrar_tela_inicial(page)

    def header():
        return ft.Column(
            controls=[
                ft.Image(src="goat.png", width=175, height=150, fit=ft.ImageFit.CONTAIN),
                ft.Text("A C E R T A D O R   D E   C O N T A S", size=24, weight="bold", color=ft.Colors.WHITE, font_family="font"),
                ft.Text("Nice and Easy.", size=14, color=ft.Colors.WHITE, font_family="font"),
            ],
            horizontal_alignment="center",
            spacing=10,
        )


    def user_inputs():
        return ft.Column(
            controls=[
                nome_input,
                email_input,
                senha_input,
                ft.ElevatedButton(
                    text="Confirmar",
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLACK,
                        bgcolor=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=5),
                    ),
                    width=300,
                    height=45,
                    on_click=salvar_dados,
                ),
                mensagem_erro  # Adicionado aqui!
            ],
            spacing=10,
            horizontal_alignment="center"
        )

    page.add(
        ft.Container(
            content=header(),
            padding=ft.padding.only(top=70)
        ),
        ft.Container(
            content=user_inputs(),
            padding=ft.padding.only(top=40),
            bgcolor=ft.Colors.BLACK87,
            border_radius=ft.border_radius.all(3),
            width=300,
        )
    )
    
    # def mostrar_tela_inicial():
    #     page.clean()    
    #     page.title = "Debtors Tracker" 
    #     page.scroll = True  # Habilita scroll na página principal

    #     def recarregar_pagina(e):
    #         mostrar_tela_inicial()  # Chama a função novamente para recarregar

    #     def criar_botao_recarregar():
    #         return ft.Container(
    #             content=ft.IconButton(
    #                 icon=ft.Icons.REFRESH,
    #                 icon_size=15,
    #                 tooltip="Recarregar usuários",
    #                 on_click=recarregar_pagina,
    #                 style=ft.ButtonStyle(
    #                     shape=ft.CircleBorder(),
    #                     padding=15,
    #                     bgcolor=ft.Colors.GREY_900,
    #                     overlay_color=ft.Colors.GREY_600,
    #                 )
    #             ),
    #             alignment=ft.alignment.top_right,
    #             padding=ft.padding.only(left=20, top=0),
    #         )

    #     def criar_botao_recarregar2():
    #         return ft.Container(
    #             content=ft.IconButton(
    #                 icon=ft.Icons.ASSIGNMENT_TURNED_IN,
    #                 icon_size=15,
    #                 tooltip="Recarregar usuários",
    #                 on_click=mostrar_assinados,
    #                 style=ft.ButtonStyle(
    #                     shape=ft.CircleBorder(),
    #                     padding=15,
    #                     bgcolor=ft.Colors.GREY_900,
    #                     overlay_color=ft.Colors.GREY_600,
    #                 )
    #             ),
    #             alignment=ft.alignment.top_left,
    #             padding=ft.padding.only(right=20, top=0),
    #         )

    #     def salvar_assinatura(user):
    #         assinatura = {
    #             "nome": f"{user['name']['first']} {user['name']['last']}",
    #             "email": user['email'],
    #             "telefone": user['phone'],
    #             "localizacao": f"{user['location']['city']}, {user['location']['state']}",
    #             "foto": user['picture']['large'],
    #             "data_assinatura": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #         }

    #         try:
    #             if os.path.exists("Assinados.json"):
    #                 with open("Assinados.json", "r", encoding='utf-8') as f:
    #                     dados = json.load(f)
    #             else:
    #                 dados = []
                
    #             dados.append(assinatura)
                
    #             with open("Assinados.json", "w", encoding='utf-8') as f:
    #                 json.dump(dados, f, indent=4, ensure_ascii=False)
                    
    #             print(f"Assinatura de {assinatura['nome']} salva com sucesso!")
                
    #         except Exception as e:
    #             print(f"Erro ao salvar assinatura: {e}")

    #     def fetch_random_users(num_users=20):
    #         try:
    #             response = requests.get(f"https://randomuser.me/api/?results={num_users}&nat=br")
    #             data = response.json()
    #             return data["results"]
    #         except Exception as e:
    #             print("Erro ao buscar usuários:", e)
    #             return []
                
    #     def create_user_card(user):
    #         phone = user['phone']
    #         location = f"{user['location']['city']}, {user['location']['state']}"
            
    #         return ft.Card(
    #             elevation=5,
    #             content=ft.Container(
    #                 width=220,
    #                 height=320,
    #                 padding=10,
    #                 content=ft.Column(
    #                     controls=[
    #                         ft.Image(
    #                             src=user["picture"]["large"],
    #                             width=120,
    #                             height=120,
    #                             fit=ft.ImageFit.COVER,
    #                             border_radius=ft.border_radius.all(60),
    #                         ),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 f"{user['name']['first']} {user['name']['last']}",
    #                                 size=16,
    #                                 weight="bold",
    #                                 color=ft.Colors.WHITE,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             padding=ft.padding.only(top=10),
    #                             width=200,
    #                         ),
    #                         ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 f"📧 {user['email']}",
    #                                 size=12,
    #                                 color=ft.Colors.WHITE70,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             width=200,
    #                         ),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 f"📍 {location}",
    #                                 size=12,
    #                                 color=ft.Colors.WHITE70,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             width=200,
    #                         ),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 f"📞 {phone}",
    #                                 size=12,
    #                                 color=ft.Colors.WHITE70,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             width=200,
    #                         ),
    #                         ft.Container(expand=True),
    #                         ft.ElevatedButton(
    #                             "Assinar",  
    #                             width=200,
    #                             height=40,
    #                             style=ft.ButtonStyle(
    #                                 color=ft.Colors.WHITE,
    #                                 bgcolor=ft.Colors.BLACK87,
    #                                 padding=10,
    #                                 shape=ft.RoundedRectangleBorder(radius=5),
    #                             ),
    #                             on_click=lambda e, u=user: salvar_assinatura(u)
    #                         ),
    #                     ],
    #                     spacing=0,
    #                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #                     alignment=ft.MainAxisAlignment.START,
    #                     expand=True
    #                 ),
    #             ),
    #         )
                
    #     def build_user_grid():
    #         users = fetch_random_users()
    #         if not users:
    #             return ft.Text("Erro ao carregar usuários.", color=ft.Colors.RED)

    #         rows = []
    #         for i in range(0, len(users), 4):
    #             row_cards = users[i:i+4]
    #             rows.append(
    #                 ft.Row(
    #                     controls=[create_user_card(user) for user in row_cards],
    #                     spacing=20,
    #                     alignment=ft.MainAxisAlignment.CENTER,
    #                     wrap=True,
    #                 )
    #             )

    #         return ft.ListView(
    #             controls=rows,
    #             spacing=20,
    #             padding=20,
    #             expand=True,
    #         )
        
    #     def header():
    #         return ft.Column(
    #             controls=[
    #                 ft.Text("Devedores perto de você", size=24, weight="bold", color=ft.Colors.WHITE),
    #                 ft.Divider(color=ft.Colors.WHITE30, height=10),
    #             ],
    #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #         )

    #     # Layout principal com scroll
    #     main_content = ft.Column(
    #         controls=[
    #             ft.Container(
    #                 padding=ft.padding.symmetric(horizontal=10),
    #                 content=ft.Row(
    #                     controls=[
    #                         criar_botao_recarregar2(),
    #                         ft.Container(expand=True),
    #                         criar_botao_recarregar()
    #                     ],
    #                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    #                 )
    #             ),
    #             header(),
    #             ft.Container(
    #                 content=build_user_grid(),
    #                 alignment=ft.alignment.center,
    #                 expand=True
    #             )
    #         ],
    #         scroll=ft.ScrollMode.AUTO,
    #         expand=True
    #     )


    #     page.add(main_content)


    # def mostrar_assinados(e):
    #     page.clean()    
    #     page.title = "Meus Assinados"   
    #     page.scroll = True

    #     if os.path.exists("Assinados.json"):
    #         with open("Assinados.json", "r", encoding="utf-8") as f:
    #             try:
    #                 dados = json.load(f)
    #             except json.JSONDecodeError:
    #                 dados = []
    #     else:
    #         dados = []

    #     if not dados:
    #         page.add(
    #             ft.Text("Nenhum usuário assinado encontrado.", color=ft.Colors.WHITE)
    #         )
    #         return

    #     def create_assinado_card(user):
    #         return ft.Card(
    #             elevation=5,
    #             content=ft.Container(
    #                 width=220,
    #                 height=320,
    #                 padding=10,
    #                 content=ft.Column(
    #                     controls=[
    #                         ft.Image(
    #                             src=user["foto"],
    #                             width=120,
    #                             height=120,
    #                             fit=ft.ImageFit.COVER,
    #                             border_radius=ft.border_radius.all(60),
    #                         ),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 user["nome"],
    #                                 size=16,
    #                                 weight="bold",
    #                                 color=ft.Colors.WHITE,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             padding=ft.padding.only(top=10),
    #                             width=200,
    #                         ),
    #                         ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 f"📧 {user['email']}",
    #                                 size=12,
    #                                 color=ft.Colors.WHITE70,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             width=200,
    #                         ),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 f"📍 {user['localizacao']}",
    #                                 size=12,
    #                                 color=ft.Colors.WHITE70,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             width=200,
    #                         ),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 f"📅 {user['data_assinatura']}",
    #                                 size=12,
    #                                 color=ft.Colors.WHITE70,
    #                                 text_align=ft.TextAlign.CENTER,
    #                             ),
    #                             width=200,
    #                         ),
    #                         ft.Container(expand=True),
    #                         ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
    #                         ft.Container(
    #                             content=ft.Text(
    #                                 "Não concluído",
    #                                 color=ft.Colors.WHITE,
    #                                 text_align=ft.TextAlign.CENTER,
    #                                 size=12,
    #                                 weight="bold"
    #                             ),
    #                             bgcolor=ft.Colors.RED_900,
    #                             border_radius=ft.border_radius.all(4),
    #                             padding=8,
    #                             width=200,
    #                             alignment=ft.alignment.center
    #                         )
    #                     ],
    #                     spacing=0,
    #                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #                     alignment=ft.MainAxisAlignment.START,
    #                     expand=True
    #                 ),
    #             )
    #         )

    #     rows = []
    #     for i in range(0, len(dados), 4):
    #         grupo = dados[i:i+4]
    #         rows.append(
    #             ft.Row(
    #                 controls=[create_assinado_card(u) for u in grupo],
    #                 alignment=ft.MainAxisAlignment.CENTER,
    #                 spacing=20,
    #                 wrap=True
    #             )
    #         )

    #     header = ft.Text("Devedores assinados", size=24, weight="bold", color=ft.Colors.WHITE)

    #     page.add(
    #         ft.Container(
    #             padding=20,
    #             content=ft.Column(
    #                 controls=[
    #                     header,
    #                     ft.Divider(color=ft.Colors.WHITE30),
    #                     *rows
    #                 ],
    #                 scroll=ft.ScrollMode.AUTO,
    #                 expand=True,
    #                 spacing=15,
    #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #             )
    #         )
    #     )


ft.app(target=main)