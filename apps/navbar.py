import dash_bootstrap_components as dbc


def create_navbar():
    # Create the Navbar using Dash Bootstrap Components
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="TỔNG QUAN", # Label given to the dropdown menu
                children=[
                    dbc.DropdownMenuItem("Thế giới", href='/apps/map_world'), # Hyperlink item that appears in the dropdown menu
                    dbc.DropdownMenuItem("Việt Nam", href='/apps/map_vn'), # Hyperlink item that appears in the dropdown menu
                ],
            ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="CHI TIẾT", # Label given to the dropdown menu
                children=[
                    dbc.DropdownMenuItem("Thế giới", href='/apps/world'), # Hyperlink item that appears in the dropdown menu
                    dbc.DropdownMenuItem("Việt Nam", href='/apps/vietnam'), # Hyperlink item that appears in the dropdown menu
                ],
            ),
        ],
        brand="THÔNG TIN COVID-19",  # Set the text on the left side of the Navbar
        brand_href="/",  # Set the URL where the user will be sent when they click the brand we just created "THÔNG TIN COVID-19"
        sticky="top",  # Stick it to the top... like Spider Man crawling on the ceiling?
        color="#3da05b",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for light text)
        brand_style={"fontSize":32,"fontWeight":600,"fontStyle":"Lato"},
    )

    return navbar