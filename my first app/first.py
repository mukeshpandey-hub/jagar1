import flet as ft
import mysql.connector

def main(page: ft.Page):
    page.title = "User Info Form"
    page.window_width = 420
    page.window_height = 550
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin@123",
        database="app1"
    )
    mycursor = mydb.cursor()

    username = ft.TextField(label="Enter your name")
    email = ft.TextField(label="Enter your email id")
    birth_date = ft.TextField(label="Enter your date of birth (YYYY-MM-DD)")
    mobile_no = ft.TextField(label="Enter your mobile no", keyboard_type=ft.KeyboardType.NUMBER)
    city = ft.TextField(label="Enter your city name")
    purpose = ft.TextField(label="Enter your purpose")

    status_text = ft.Text(value="", color="green")

    def insert_info(e):
        try:
            if not (username.value and email.value and birth_date.value and mobile_no.value and city.value and purpose.value):
                status_text.value = "Please fill all fields!"
                status_text.color = "red"
                page.update()
                return

            mycursor.execute("SELECT IFNULL(MAX(s_no), 0) + 1 FROM users")
            s_no = mycursor.fetchone()[0]

            query = """
            INSERT INTO users (s_no, username, email, birth_date, mobile_no, city, purpose) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            user_data = (
                s_no,
                username.value,
                email.value,
                birth_date.value,
                int(mobile_no.value),
                city.value,
                purpose.value
            )
            mycursor.execute(query, user_data)
            mydb.commit()

            status_text.value = "Added successfully!"
            status_text.color = "green"

            username.value = ""
            email.value = ""
            birth_date.value = ""
            mobile_no.value = ""
            city.value = ""
            purpose.value = ""

            page.update()

        except Exception as ex:
            status_text.value = f"Error: {ex}"
            status_text.color = "red"
            page.update()

    submit_btn = ft.ElevatedButton("Add Info", on_click=insert_info)

    page.add(
        ft.Text("User Info Form", size=22, weight=ft.FontWeight.BOLD),
        username,
        email,
        birth_date,
        mobile_no,
        city,
        purpose,
        submit_btn,
        status_text
    )

ft.app(target=main)
