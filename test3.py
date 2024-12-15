import pygame
import mysql.connector

pygame.init()

# Pygame setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# MySQL connection setup (replace with your actual credentials)
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",  # replace with your MySQL username
    password="mysqlroot2343",  # replace with your MySQL password
    database="jampy"  # replace with your MySQL database name
)
cursor = db_connection.cursor()

# Set up Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MySQL Table Viewer')
clock = pygame.time.Clock()
font = pygame.font.Font("assets\\Flexi_IBM_VGA_True_437.ttf", 24)

# Table name (replace with your actual table name)
selectedData3 = "company"

# Pagination variables
page_number = 0
rows_per_page = 15

def fetch_table_data(page):
    """Fetch data for the current page from the MySQL table."""
    start = page * rows_per_page
    query = f"SELECT * FROM {selectedData3} LIMIT {start}, {rows_per_page}"
    cursor.execute(query)
    return cursor.fetchall()

def get_table_headers():
    """Get column headers from the table description."""
    cursor.execute(f"DESCRIBE {selectedData3}")
    return [desc[0] for desc in cursor.fetchall()]

def calculate_column_widths(data, headers):
    """Calculate column widths based on the longest content in each column."""
    col_widths = [len(header) for header in headers]
    for row in data:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(value)))
    return [width * 12 for width in col_widths]  # Scale width for rendering

def render_table(data, headers, page):
    """Render the table data and headers in Pygame."""
    screen.fill((60, 150, 60))  # Background color

    # Calculate column widths
    col_widths = calculate_column_widths(data, headers)

    # Render table headers
    x_offset = 10
    for i, header in enumerate(headers):
        header_surface = font.render(header, True, (255, 255, 255))
        screen.blit(header_surface, (x_offset, 10))
        x_offset += col_widths[i] + 20  # Add padding between columns

    # Render table rows
    y_offset = 50  # Start rendering rows below the header
    for row in data:
        x_offset = 10
        for i, value in enumerate(row):
            row_surface = font.render(str(value), True, (255, 255, 255))
            screen.blit(row_surface, (x_offset, y_offset))
            x_offset += col_widths[i] + 20
        y_offset += 30  # Space between rows

    # Page navigation buttons (simple up/down pagination)
    nav_font = pygame.font.Font(None, 28)
    prev_button = nav_font.render("Prev", True, (255, 255, 255))
    next_button = nav_font.render("Next", True, (255, 255, 255))

    screen.blit(prev_button, (10, SCREEN_HEIGHT - 40))
    screen.blit(next_button, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40))

    # Display page number
    page_text = f"Page {page + 1}"
    page_surface = nav_font.render(page_text, True, (255, 255, 255))
    screen.blit(page_surface, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40))

def handle_events():
    """Handle Pygame events such as key presses and mouse clicks."""
    global page_number
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Check if "Prev" button is clicked
            if 10 <= mx <= 70 and SCREEN_HEIGHT - 40 <= my <= SCREEN_HEIGHT - 10:
                if page_number > 0:
                    page_number -= 1
            # Check if "Next" button is clicked
            if SCREEN_WIDTH - 100 <= mx <= SCREEN_WIDTH - 10 and SCREEN_HEIGHT - 40 <= my <= SCREEN_HEIGHT - 10:
                page_number += 1

def ShowTable():
    """Main function to display the MySQL table in Pygame."""
    headers = get_table_headers()

    while True:
        data = fetch_table_data(page_number)  # Fetch current page data
        render_table(data, headers, page_number)  # Render the table

        handle_events()  # Handle user input events
        pygame.display.flip()  # Update display
        clock.tick(FPS)  # Limit frame rate to FPS

# Initialize and run the Pygame application
if __name__ == "__main__":
    ShowTable()
