import flet as ft
import datetime

# --- Classes de Dados ---
class BLBook:
    def __init__(self, title, category, cover_color, total_pages=100):
        self.title = title
        self.category = category
        self.cover_color = cover_color
        self.current_page = 0
        self.total_pages = total_pages
        self.last_read = datetime.datetime.now()

# --- Dados Iniciais ---
# Usando strings para cores para evitar erro no Android
my_library = [
    BLBook("Love Stage!! Vol. 1", "Escolar", "indigo300", 150),
    BLBook("Blood Bank", "Fantasia", "indigo400", 200),
    BLBook("Omega Complex", "Omegaverse", "pink200", 120),
    BLBook("Bj Alex", "Drama", "deepPurple300", 80),
]

def main(page: ft.Page):
    # --- Configurações da Página (Mobile UI) ---
    page.title = "BL Reader"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    # Removidos tamanhos fixos de janela para se adaptar à tela do celular
    page.bgcolor = "#F5F5FA" 

    # Estado da aplicação
    current_book = None
    selected_category = None
    
    # --- Componentes Reutilizáveis ---

    def create_book_card(book, width=140, height=200, minimal=False):
        """Cria o card visual do livro"""
        
        progress_val = book.current_page / book.total_pages if book.total_pages > 0 else 0
        
        card_content = ft.Container(
            content=ft.Column([
                # Capa
                ft.Container(
                    content=ft.Text(
                        "".join([word[0] for word in book.title.split()[:2]]), 
                        size=30, weight=ft.FontWeight.BOLD, color="white"
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=book.cover_color,
                    height=140 if not minimal else 100,
                    border_radius=12,
                ),
                # Informações
                ft.Column([
                    ft.Text(book.title, weight=ft.FontWeight.BOLD, size=14, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f"Cap. {book.current_page} - Pág {book.current_page}", size=11, color="grey"),
                    ft.ProgressBar(value=progress_val, color="pinkAccent", bgcolor="pink50", height=4)
                ], spacing=2)
            ], spacing=5),
            width=width,
            padding=10,
            bgcolor="white",
            border_radius=16,
            on_click=lambda _: open_reader(book),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.05, "black"))
        )
        return card_content

    def create_folder_card(icon, name, count, color):
        """Cria o card das pastas"""
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=24),
                    bgcolor=ft.colors.with_opacity(0.1, color),
                    padding=10,
                    border_radius=10,
                    width=45, height=45, alignment=ft.alignment.center
                ),
                ft.Text(name, weight=ft.FontWeight.BOLD, size=14),
                ft.Text(f"{count} arquivos", size=11, color="grey")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START),
            width=150, height=120,
            bgcolor="white",
            border_radius=16,
            padding=15,
            on_click=lambda _: open_category(name),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.with_opacity(0.05, "black"))
        )

    # --- Navegação ---

    def open_reader(book):
        nonlocal current_book
        current_book = book
        page.go("/reader")

    def open_category(category_name):
        nonlocal selected_category
        selected_category = category_name
        page.go("/category")

    def search_books(e):
        pass # Busca simples

    # --- Views ---

    def get_home_view():
        recent_books = sorted(my_library, key=lambda x: x.last_read, reverse=True)[:2]
        
        folders_grid = ft.Row([
            create_folder_card(ft.icons.PETS, "Omegaverse", 5, "pink"),
            create_folder_card(ft.icons.SCHOOL, "Escolar", 3, "pink"),
            create_folder_card(ft.icons.TOKEN, "Fantasia", 8, "purple"),
            create_folder_card(ft.icons.THEATER_COMEDY, "Drama", 2, "purple"),
        ], wrap=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return ft.View(
            "/",
            controls=[
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("BL Reader", size=24, weight=ft.FontWeight.BOLD, color="deepPurple"),
                        ft.CircleAvatar(bgcolor="grey300", radius=16, content=ft.Icon(ft.icons.PERSON, size=20, color="white"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.only(left=20, right=20, top=10)
                ),
                
                # Barra de Pesquisa
                ft.Container(
                    content=ft.TextField(
                        prefix_icon=ft.icons.SEARCH,
                        hint_text="Love stage",
                        border=ft.InputBorder.NONE,
                        bgcolor="white",
                        border_radius=30,
                        content_padding=15,
                        text_size=14,
                        on_change=search_books
                    ),
                    padding=ft.padding.symmetric(horizontal=20)
                ),

                # Conteúdo
                ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Text("Continuar Lendo", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text("Ver tudo", size=12, color="deepPurple", weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.symmetric(horizontal=20)
                    ),
                    ft.Container(
                        content=ft.Row(
                            [create_book_card(book) for book in recent_books],
                            scroll=ft.ScrollMode.ALWAYS
                        ),
                        padding=ft.padding.only(left=20)
                    ),

                    ft.Container(
                        content=ft.Row([
                            ft.Text("Minhas Pastas", size=16, weight=ft.FontWeight.BOLD),
                            ft.Icon(ft.icons.SORT_BY_ALPHA, size=20)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                    ),
                    ft.Container(
                        content=folders_grid,
                        padding=ft.padding.symmetric(horizontal=20)
                    )
                ], scroll=ft.ScrollMode.AUTO, expand=True),

                # Botão Flutuante
                ft.Container(
                    content=ft.FloatingActionButton(icon=ft.icons.ADD, bgcolor="deepPurpleAccent", shape=ft.CircleBorder()),
                    alignment=ft.alignment.bottom_center,
                    padding=10
                ),
                
                # Navbar
                ft.NavigationBar(
                    destinations=[
                        ft.NavigationDestination(icon=ft.icons.HOME, label=""),
                        ft.NavigationDestination(icon=ft.icons.BOOK, label=""),
                        ft.NavigationDestination(icon=ft.icons.FAVORITE, label=""),
                        ft.NavigationDestination(icon=ft.icons.SETTINGS, label=""),
                    ],
                    height=60,
                    bgcolor="white",
                    indicator_color="transparent",
                    icon_color="grey",
                    selected_index=0
                )
            ],
            bgcolor="#F5F5FA",
            padding=0
        )

    def get_reader_view():
        
        def change_page(delta):
            new_page = current_book.current_page + delta
            if 0 <= new_page <= current_book.total_pages:
                current_book.current_page = new_page
                page_counter.value = f"Página {current_book.current_page} de {current_book.total_pages}"
                page.update()

        page_counter = ft.Text(f"Página {current_book.current_page} de {current_book.total_pages}")
        
        return ft.View(
            "/reader",
            controls=[
                ft.AppBar(title=ft.Text(current_book.title), bgcolor="deepPurple", color="white"),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.PICTURE_AS_PDF, size=100, color="grey300"),
                        ft.Text("Aqui apareceria o PDF", size=20, weight=ft.FontWeight.BOLD),
                        page_counter,
                        ft.Row([
                            ft.ElevatedButton("Anterior", on_click=lambda _: change_page(-1)),
                            ft.ElevatedButton("Próximo", on_click=lambda _: change_page(1)),
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    alignment=ft.alignment.center
                )
            ]
        )
    
    def get_category_view():
        category_books = [b for b in my_library if b.category == selected_category]
        
        return ft.View(
            "/category",
            controls=[
                ft.AppBar(title=ft.Text(selected_category), bgcolor="deepPurple", color="white"),
                ft.GridView(
                    runs_count=2,
                    max_extent=160,
                    child_aspect_ratio=0.7,
                    spacing=10,
                    run_spacing=10,
                    padding=20,
                    controls=[create_book_card(b, minimal=True) for b in category_books]
                )
            ]
        )

    def route_change(route):
        page.views.clear()
        page.views.append(get_home_view())
        
        if page.route == "/reader" and current_book:
            page.views.append(get_reader_view())
        elif page.route == "/category" and selected_category:
            page.views.append(get_category_view())
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
