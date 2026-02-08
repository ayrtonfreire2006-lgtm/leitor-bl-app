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

# --- Dados Iniciais (Simulando seus arquivos) ---
# Aqui estariam os caminhos para seus PDFs reais
my_library = [
    BLBook("Love Stage!! Vol. 1", "Escolar", ft.colors.INDIGO_300, 150),
    BLBook("Blood Bank", "Fantasia", ft.colors.INDIGO_400, 200),
    BLBook("Omega Complex", "Omegaverse", ft.colors.PINK_200, 120),
    BLBook("Bj Alex", "Drama", ft.colors.DEEP_PURPLE_300, 80),
]

def main(page: ft.Page):
    # --- Configurações da Página (Mobile UI) ---
    page.title = "BL Reader"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 380  # Tamanho simulado de celular
    page.window_height = 800
    page.bgcolor = "#F5F5FA" # Cor de fundo levemente cinza do print

    # Estado da aplicação
    current_book = None
    selected_category = None
    
    # --- Componentes Reutilizáveis ---

    def create_book_card(book, width=140, height=200, minimal=False):
        """Cria o card visual do livro"""
        
        # Barra de progresso visual
        progress_val = book.current_page / book.total_pages if book.total_pages > 0 else 0
        
        card_content = ft.Container(
            content=ft.Column([
                # Capa (Placeholder da cor)
                ft.Container(
                    content=ft.Text(
                        "".join([word[0] for word in book.title.split()[:2]]), # Iniciais
                        size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=book.cover_color,
                    height=140 if not minimal else 100,
                    border_radius=12,
                ),
                # Informações
                ft.Column([
                    ft.Text(book.title, weight=ft.FontWeight.BOLD, size=14, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f"Cap. {book.current_page} - Pág {book.current_page}", size=11, color=ft.colors.GREY),
                    ft.ProgressBar(value=progress_val, color=ft.colors.PINK_ACCENT, bgcolor=ft.colors.PINK_50, height=4)
                ], spacing=2)
            ], spacing=5),
            width=width,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border_radius=16,
            on_click=lambda _: open_reader(book), # Clicar abre o leitor
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.05, ft.colors.BLACK))
        )
        return card_content

    def create_folder_card(icon, name, count, color):
        """Cria o card das pastas (Omegaverse, Escolar, etc)"""
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
                ft.Text(f"{count} arquivos", size=11, color=ft.colors.GREY)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START),
            width=150, height=120,
            bgcolor=ft.colors.WHITE,
            border_radius=16,
            padding=15,
            on_click=lambda _: open_category(name),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.with_opacity(0.05, ft.colors.BLACK))
        )

    # --- Funções de Navegação e Lógica ---

    def open_reader(book):
        nonlocal current_book
        current_book = book
        page.go("/reader")

    def open_category(category_name):
        nonlocal selected_category
        selected_category = category_name
        page.go("/category")

    def save_progress(e):
        """Simula salvar a página ao clicar em voltar ou sair"""
        if current_book:
            current_book.last_read = datetime.datetime.now()
        page.go("/")

    def search_books(e):
        """Filtra os livros na home"""
        search_term = e.control.value.lower()
        filtered_books = [b for b in my_library if search_term in b.title.lower()]
        update_home_grid(filtered_books)

    # --- Views (Telas) ---

    def get_home_view():
        # Ordenar por leitura recente para a seção "Continuar Lendo"
        recent_books = sorted(my_library, key=lambda x: x.last_read, reverse=True)[:2]
        
        # Grid de Pastas
        folders_grid = ft.Row([
            create_folder_card(ft.icons.PETS, "Omegaverse", 5, ft.colors.PINK),
            create_folder_card(ft.icons.SCHOOL, "Escolar", 3, ft.colors.PINK),
            create_folder_card(ft.icons.TOKEN, "Fantasia", 8, ft.colors.PURPLE), # Ícone dragão não padrão, usando token
            create_folder_card(ft.icons.THEATER_COMEDY, "Drama", 2, ft.colors.PURPLE),
        ], wrap=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return ft.View(
            "/",
            controls=[
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("BL Reader", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.DEEP_PURPLE),
                        ft.CircleAvatar(bgcolor=ft.colors.GREY_300, radius=16, content=ft.Icon(ft.icons.PERSON, size=20, color=ft.colors.WHITE))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.only(left=20, right=20, top=10)
                ),
                
                # Barra de Pesquisa
                ft.Container(
                    content=ft.TextField(
                        prefix_icon=ft.icons.SEARCH,
                        hint_text="Love stage",
                        border=ft.InputBorder.NONE,
                        bgcolor=ft.colors.WHITE,
                        border_radius=30,
                        content_padding=15,
                        text_size=14,
                        on_change=search_books
                    ),
                    padding=ft.padding.symmetric(horizontal=20)
                ),

                # Conteúdo Scrollável
                ft.Column([
                    # Seção Continuar Lendo
                    ft.Container(
                        content=ft.Row([
                            ft.Text("Continuar Lendo", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text("Ver tudo", size=12, color=ft.colors.DEEP_PURPLE, weight=ft.FontWeight.BOLD)
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

                    # Seção Minhas Pastas
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

                # Botão Flutuante (Add)
                ft.Container(
                    content=ft.FloatingActionButton(icon=ft.icons.ADD, bgcolor=ft.colors.DEEP_PURPLE_ACCENT, shape=ft.CircleBorder()),
                    alignment=ft.alignment.bottom_center,
                    padding=10
                ),
                
                # Navbar Simulada
                ft.NavigationBar(
                    destinations=[
                        ft.NavigationDestination(icon=ft.icons.HOME, label=""),
                        ft.NavigationDestination(icon=ft.icons.BOOK, label=""),
                        ft.NavigationDestination(icon=ft.icons.FAVORITE, label=""),
                        ft.NavigationDestination(icon=ft.icons.SETTINGS, label=""),
                    ],
                    height=60,
                    bgcolor=ft.colors.WHITE,
                    indicator_color="transparent",
                    icon_color=ft.colors.GREY,
                    selected_index=0
                )
            ],
            bgcolor="#F5F5FA",
            padding=0
        )

    def get_reader_view():
        """Tela de Leitura Simulada"""
        
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
                ft.AppBar(title=ft.Text(current_book.title), bgcolor=ft.colors.DEEP_PURPLE, color=ft.colors.WHITE),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.PICTURE_AS_PDF, size=100, color=ft.colors.GREY_300),
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
        """Tela de Categoria Específica"""
        category_books = [b for b in my_library if b.category == selected_category]
        
        return ft.View(
            "/category",
            controls=[
                ft.AppBar(title=ft.Text(selected_category), bgcolor=ft.colors.DEEP_PURPLE, color=ft.colors.WHITE),
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

    # Função para atualizar dinamicamente a home (usada na busca)
    def update_home_grid(filtered_list=None):
        # Numa app real, você reconstruiria os controles aqui.
        # Para este exemplo, a busca apenas imprime no console para simplicidade, 
        # mas a estrutura está pronta.
        pass

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