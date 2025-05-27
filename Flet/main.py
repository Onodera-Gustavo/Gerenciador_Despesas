import flet as ft
from flet import *
import json
import os
from datetime import datetime

def main(page: ft.Page):
    page.title = "Agiotagem tracker"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK87

    page.fonts = {
        "font": "fonts/Montserrat-Regular.ttf"
    }

    # Campos fora da função
    nome_input = ft.TextField(label="Nome de usuário", color=ft.Colors.WHITE, border_color=ft.Colors.WHITE)
    email_input = ft.TextField(label="Email*", color=ft.Colors.WHITE, border_color=ft.Colors.WHITE)
    senha_input = ft.TextField(label="Senha*", password=True, color=ft.Colors.WHITE, border_color=ft.Colors.WHITE)

    def salvar_dados(e):
        usuario = {
            "nome": nome_input.value,
            "email": email_input.value,
            "senha": senha_input.value
        }

        # Cria arquivo se não existir e lê 
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r") as f:
                try:
                    dados = json.load(f)
                except json.JSONDecodeError:
                    dados = []
        else:
            dados = []

        dados.append(usuario)

        with open("usuarios.json", "w") as f:
            json.dump(dados, f, indent=4)

        print("Usuário salvo:", usuario)
        mostrar_tela_inicial()
        

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
    
    def mostrar_tela_inicial():
        page.clean()    
        page.title = "Tela Inicial"
        
        def inicio_tela():
            # Pega a data atual formatada
            data_atual = datetime.now().strftime("%d/%m/%Y")

            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Saldo atual: ",
                                size=20,
                                weight="bold",
                                color=ft.Colors.WHITE,
                                font_family="font",
                            ),
                            ft.Container(
                                content=ft.Text(
                                    data_atual,
                                    size=22,
                                    color=ft.Colors.WHITE,
                                    font_family="font",
                                ),
                                alignment=ft.alignment.top_right,
                                expand=True,
                                padding=ft.padding.only(right=10, top=10),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "A Receber: ",
                                size=20,
                                weight="bold",
                                color=ft.Colors.WHITE,
                                font_family="font",
                            )
                        ]
                    ),
                ],
                alignment=ft.alignment.top_left,
                spacing=20,
            )
            
        
        page.add(
            ft.Container(
                content=inicio_tela(),
                padding=ft.padding.only(top=10, left=10),
                
            )
        )

ft.app(target=main)