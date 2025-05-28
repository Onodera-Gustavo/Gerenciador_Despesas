import flet as ft
from flet import *
import requests
import json
import os
from datetime import datetime




def mostrar_tela_inicial(page: ft.Page):
        page.clean()    
        page.title = "Debtors Tracker" 
        page.scroll = True  # Habilita scroll na página principal

        botao_voltar = ft.ElevatedButton(
        "Voltar",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda e: mostrar_tela_inicial(page),
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREY_900,
            padding=10,
            shape=ft.RoundedRectangleBorder(radius=5),
        )
    )

        if os.path.exists("Assinados.json"):
            with open("Assinados.json", "r", encoding="utf-8") as f:
                try:
                    dados = json.load(f)
                except json.JSONDecodeError:
                    dados = []
        else:
            dados = []

        def recarregar_pagina(e):
            mostrar_tela_inicial(page)  # Chama a função novamente para recarregar

        def criar_botao_recarregar():
            return ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    icon_size=15,
                    tooltip="Recarregar usuários",
                    on_click=recarregar_pagina,
                    style=ft.ButtonStyle(
                        shape=ft.CircleBorder(),
                        padding=15,
                        bgcolor=ft.Colors.GREY_900,
                        overlay_color=ft.Colors.GREY_600,
                    )
                ),
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(left=20, top=0),
            )

        def criar_botao_recarregar2():
            return ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.ASSIGNMENT_TURNED_IN,
                    icon_size=15,
                    tooltip="Recarregar usuários",
                    on_click=lambda e: mostrar_assinados(page),
                    style=ft.ButtonStyle(
                        shape=ft.CircleBorder(),
                        padding=15,
                        bgcolor=ft.Colors.GREY_900,
                        overlay_color=ft.Colors.GREY_600,
                    )
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(right=20, top=0),
            )

        def salvar_assinatura(user):
            assinatura = {
                "nome": f"{user['name']['first']} {user['name']['last']}",
                "email": user['email'],
                "telefone": user['phone'],
                "localizacao": f"{user['location']['city']}, {user['location']['state']}",
                "foto": user['picture']['large'],
                "data_assinatura": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }

            try:
                if os.path.exists("Assinados.json"):
                    with open("Assinados.json", "r", encoding='utf-8') as f:
                        dados = json.load(f)
                else:
                    dados = []
                
                dados.append(assinatura)
                
                with open("Assinados.json", "w", encoding='utf-8') as f:
                    json.dump(dados, f, indent=4, ensure_ascii=False)
                    
                print(f"Assinatura de {assinatura['nome']} salva com sucesso!")
                
            except Exception as e:
                print(f"Erro ao salvar assinatura: {e}")

        def fetch_random_users(num_users=20):
            try:
                response = requests.get(f"https://randomuser.me/api/?results={num_users}&nat=br")
                data = response.json()
                return data["results"]
            except Exception as e:
                print("Erro ao buscar usuários:", e)
                return []
                
        def create_user_card(user):
            phone = user['phone']
            location = f"{user['location']['city']}, {user['location']['state']}"
            
            return ft.Card(
                elevation=5,
                content=ft.Container(
                    width=220,
                    height=320,
                    padding=10,
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=user["picture"]["large"],
                                width=120,
                                height=120,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.all(60),
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"{user['name']['first']} {user['name']['last']}",
                                    size=16,
                                    weight="bold",
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                padding=ft.padding.only(top=10),
                                width=200,
                            ),
                            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                            ft.Container(
                                content=ft.Text(
                                    f"📧 {user['email']}",
                                    size=12,
                                    color=ft.Colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=200,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"📍 {location}",
                                    size=12,
                                    color=ft.Colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=200,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"📞 {phone}",
                                    size=12,
                                    color=ft.Colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=200,
                            ),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Assinar",  
                                width=200,
                                height=40,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLACK87,
                                    padding=10,
                                    shape=ft.RoundedRectangleBorder(radius=5),
                                ),
                                on_click=lambda e, u=user: salvar_assinatura(u)
                            ),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.START,
                        expand=True
                    ),
                ),
            )
                
        def build_user_grid():
            users = fetch_random_users()
            if not users:
                return ft.Text("Erro ao carregar usuários.", color=ft.Colors.RED)

            rows = []
            for i in range(0, len(users), 4):
                row_cards = users[i:i+4]
                rows.append(
                    ft.Row(
                        controls=[create_user_card(user) for user in row_cards],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    )
                )

            return ft.ListView(
                controls=rows,
                spacing=20,
                padding=20,
                expand=True,
            )
        
        def header():
            return ft.Column(
                controls=[
                    ft.Text("Devedores perto de você", size=24, weight="bold", color=ft.Colors.WHITE),
                    ft.Divider(color=ft.Colors.WHITE30, height=10),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )   


        # Layout principal com scroll
        main_content = ft.Column(
            controls=[
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=10),
                    content=ft.Row(
                        controls=[
                            criar_botao_recarregar2(),
                            ft.Container(expand=True),
                            criar_botao_recarregar()
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ),
                header(),
                ft.Container(
                    content=build_user_grid(),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )


        page.add(main_content)


def mostrar_assinados(page):
        page.clean()    
        page.title = "Meus Assinados"   
        page.scroll = True

        if os.path.exists("Assinados.json"):
            with open("Assinados.json", "r", encoding="utf-8") as f:
                try:
                    dados = json.load(f)
                except json.JSONDecodeError:
                    dados = []
        else:
            dados = []

        if not dados:
            page.add(
                ft.Text("Nenhum usuário assinado encontrado.", color=ft.Colors.WHITE)
            )
            return

        botao_voltar = ft.ElevatedButton(
            "Voltar",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: mostrar_tela_inicial(page),
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREY_900,
                padding=10,
                shape=ft.RoundedRectangleBorder(radius=5),
            )
        )

        def create_assinado_card(user):
            return ft.Card(
                elevation=5,
                content=ft.Container(
                    width=220,
                    height=320,
                    padding=10,
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=user["foto"],
                                width=120,
                                height=120,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.all(60),
                            ),
                            ft.Container(
                                content=ft.Text(
                                    user["nome"],
                                    size=16,
                                    weight="bold",
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                padding=ft.padding.only(top=10),
                                width=200,
                            ),
                            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                            ft.Container(
                                content=ft.Text(
                                    f"📧 {user['email']}",
                                    size=12,
                                    color=ft.Colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=200,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"📍 {user['localizacao']}",
                                    size=12,
                                    color=ft.Colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=200,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"📅 {user['data_assinatura']}",
                                    size=12,
                                    color=ft.Colors.WHITE70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=200,
                            ),
                            ft.Container(expand=True),
                            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                            ft.Container(
                                content=ft.Text(
                                    "Não concluído",
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                    size=12,
                                    weight="bold"
                                ),
                                bgcolor=ft.Colors.RED_900,
                                border_radius=ft.border_radius.all(4),
                                padding=8,
                                width=200,
                                alignment=ft.alignment.center
                            )
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.START,
                        expand=True
                    ),
                )
            )

        rows = []
        for i in range(0, len(dados), 4):
            grupo = dados[i:i+4]
            rows.append(
                ft.Row(
                    controls=[create_assinado_card(u) for u in grupo],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    wrap=True
                )
            )

        header = ft.Text("Devedores assinados", size=24, weight="bold", color=ft.Colors.WHITE)

        page.add(
            ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                botao_voltar,
                                ft.Container(expand=True)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        header,
                        ft.Divider(color=ft.Colors.WHITE30),
                        *rows
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        )


