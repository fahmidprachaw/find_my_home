import tkinter as tk
from tkinter import ttk, messagebox
from user import User
from house import House
from transaction import Transaction
from database import create_tables, get_connection


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Find My Home")
        self.geometry("800x600")
        self.current_user = None
        self.user_role = None
        self.login_screen()

    def login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Login", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Email").pack(pady=5)
        entry_email = tk.Entry(self)
        entry_email.pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        entry_password = tk.Entry(self, show="*")
        entry_password.pack(pady=5)

        def authenticate():
            email = entry_email.get()
            password = entry_password.get()
            user = self.authenticate_user(email, password)
            if user:
                self.current_user = user
                self.user_role = user[6]  # Role column in Users table
                self.main_menu()
            else:
                messagebox.showerror("Error", "Invalid email or password!")

        def open_register_screen():
            self.register_screen()

        tk.Button(self, text="Login", command=authenticate).pack(pady=10)
        tk.Button(self, text="Register", command=open_register_screen).pack(pady=10)

    def register_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Register", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="First Name").pack(pady=5)
        entry_first_name = tk.Entry(self)
        entry_first_name.pack(pady=5)

        tk.Label(self, text="Last Name").pack(pady=5)
        entry_last_name = tk.Entry(self)
        entry_last_name.pack(pady=5)

        tk.Label(self, text="Email").pack(pady=5)
        entry_email = tk.Entry(self)
        entry_email.pack(pady=5)

        tk.Label(self, text="Phone").pack(pady=5)
        entry_phone = tk.Entry(self)
        entry_phone.pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        entry_password = tk.Entry(self, show="*")
        entry_password.pack(pady=5)

        tk.Label(self, text="Role").pack(pady=5)
        role_var = tk.StringVar(value="customer")
        tk.Radiobutton(self, text="Customer", variable=role_var, value="customer").pack()
        tk.Radiobutton(self, text="Flat Owner", variable=role_var, value="flat_owner").pack()

        def register():
            first_name = entry_first_name.get()
            last_name = entry_last_name.get()
            email = entry_email.get()
            phone = entry_phone.get()
            password = entry_password.get()
            role = role_var.get()

            if not all([first_name, last_name, email, phone, password]):
                messagebox.showerror("Error", "All fields are required!")
                return

            User.add_user(first_name, last_name, email, phone, password, role)
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.login_screen()

        tk.Button(self, text="Register", command=register).pack(pady=10)
        tk.Button(self, text="Back", command=self.login_screen).pack(pady=10)

    def authenticate_user(self, email, password):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM Users WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()
        connection.close()
        return user

    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text=f"Welcome, {self.current_user[1]}!", font=("Arial", 18)).pack(pady=20)

        if self.user_role == 'admin':
            tk.Button(self, text="Manage Users", width=30, command=self.manage_users).pack(pady=10)
            tk.Button(self, text="Approve House Posts", width=30, command=self.approve_houses).pack(pady=10)
        elif self.user_role == 'customer':
            tk.Button(self, text="View Available Houses", width=30, command=self.view_available_houses).pack(pady=10)
            tk.Button(self, text="Book a House", width=30, command=self.book_house).pack(pady=10)
        elif self.user_role == 'flat_owner':
            tk.Button(self, text="Post House Advertisement", width=30, command=self.post_house_ad).pack(pady=10)
            tk.Button(self, text="View Bookings", width=30, command=self.view_bookings).pack(pady=10)

        tk.Button(self, text="Logout", width=30, command=self.login_screen).pack(pady=10)

    def manage_users(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Manage Users", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="List Users", width=30, command=self.list_users).pack(pady=10)
        tk.Button(self, text="Delete User", width=30, command=self.delete_user).pack(pady=10)
        tk.Button(self, text="Back", width=30, command=self.main_menu).pack(pady=10)

    def list_users(self):
        list_users_window = tk.Toplevel(self)
        list_users_window.title("List Users")
        list_users_window.geometry("600x400")

        tree = ttk.Treeview(
            list_users_window,
            columns=("ID", "First Name", "Last Name", "Email", "Phone", "Role"),
            show="headings"
        )
        tree.heading("ID", text="ID")
        tree.heading("First Name", text="First Name")
        tree.heading("Last Name", text="Last Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.heading("Role", text="Role")
        tree.pack(fill=tk.BOTH, expand=True)

        users = User.list_users()

        if users:
            for user in users:
                tree.insert("", tk.END, values=user)
        else:
            messagebox.showinfo("No Data", "No users found in the database!")

    def delete_user(self):
        def confirm_delete():
            user_id = entry_user_id.get()
            User.delete_user(user_id)
            messagebox.showinfo("Success", "User deleted successfully!")
            delete_user_window.destroy()

        delete_user_window = tk.Toplevel(self)
        delete_user_window.title("Delete User")
        delete_user_window.geometry("300x200")

        tk.Label(delete_user_window, text="Enter User ID").pack(pady=5)
        entry_user_id = tk.Entry(delete_user_window)
        entry_user_id.pack(pady=5)

        tk.Button(delete_user_window, text="Delete", command=confirm_delete).pack(pady=10)

    def approve_houses(self):
        approve_window = tk.Toplevel(self)
        approve_window.title("Approve Houses")
        approve_window.geometry("600x400")

        houses = self.get_unapproved_houses()

        tree = ttk.Treeview(approve_window, columns=("ID", "Type", "Location", "Price"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Type", text="Type")
        tree.heading("Location", text="Location")
        tree.heading("Price", text="Price")
        tree.pack(fill=tk.BOTH, expand=True)

        for house in houses:
            tree.insert("", tk.END, values=house)

        def approve_selected():
            selected_item = tree.selection()
            if selected_item:
                house_id = tree.item(selected_item)['values'][0]
                self.approve_house(house_id)
                messagebox.showinfo("Success", "House approved successfully!")
                approve_window.destroy()

        tk.Button(approve_window, text="Approve Selected", command=approve_selected).pack(pady=10)

    def get_unapproved_houses(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT house_id, type_name, location, price FROM Houses WHERE approved = FALSE
        """)
        houses = cursor.fetchall()
        connection.close()
        return houses

    def approve_house(self, house_id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Houses SET approved = TRUE WHERE house_id = %s
        """, (house_id,))
        connection.commit()
        connection.close()

    def view_available_houses(self):
        view_houses_window = tk.Toplevel(self)
        view_houses_window.title("Available Houses")
        view_houses_window.geometry("600x400")

        tree = ttk.Treeview(
            view_houses_window,
            columns=("ID", "Type", "Description", "Location", "Price"),
            show="headings"
        )
        tree.heading("ID", text="ID")
        tree.heading("Type", text="Type")
        tree.heading("Description", text="Description")
        tree.heading("Location", text="Location")
        tree.heading("Price", text="Price")
        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(view_houses_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        houses = House.list_houses(status="available", approved=True)

        if houses:
            for house in houses:
                tree.insert("", tk.END, values=house)
        else:
            messagebox.showinfo("No Data", "No available houses at the moment!")

    def book_house(self):
        def confirm_booking():
            house_id = entry_house_id.get()
            amount = entry_amount.get()

            if not house_id or not amount:
                messagebox.showerror("Error", "Please provide House ID and Booking Amount.")
                return

            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered!")
                return

            # Add transaction and update house status
            Transaction.add_transaction(self.current_user[0], house_id, amount)
            messagebox.showinfo("Success", "House booked successfully!")
            book_house_window.destroy()

        book_house_window = tk.Toplevel(self)
        book_house_window.title("Book a House")
        book_house_window.geometry("300x200")

        tk.Label(book_house_window, text="House ID").pack(pady=5)
        entry_house_id = tk.Entry(book_house_window)
        entry_house_id.pack(pady=5)

        tk.Label(book_house_window, text="Booking Amount").pack(pady=5)
        entry_amount = tk.Entry(book_house_window)
        entry_amount.pack(pady=5)

        tk.Button(book_house_window, text="Confirm Booking", command=confirm_booking).pack(pady=10)

    def post_house_ad(self):
        def save_house_ad():
            type_name = entry_type.get()
            description = entry_description.get()
            location = entry_location.get()
            price = entry_price.get()

            if not all([type_name, description, location, price]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Invalid price entered!")
                return

            # Add house advertisement
            House.add_house(self.current_user[0], type_name, description, location, price)
            messagebox.showinfo("Success", "House advertisement posted successfully!")
            post_ad_window.destroy()

        post_ad_window = tk.Toplevel(self)
        post_ad_window.title("Post House Advertisement")
        post_ad_window.geometry("400x400")

        tk.Label(post_ad_window, text="Type").pack(pady=5)
        entry_type = tk.Entry(post_ad_window)
        entry_type.pack(pady=5)

        tk.Label(post_ad_window, text="Description").pack(pady=5)
        entry_description = tk.Entry(post_ad_window)
        entry_description.pack(pady=5)

        tk.Label(post_ad_window, text="Location").pack(pady=5)
        entry_location = tk.Entry(post_ad_window)
        entry_location.pack(pady=5)

        tk.Label(post_ad_window, text="Price").pack(pady=5)
        entry_price = tk.Entry(post_ad_window)
        entry_price.pack(pady=5)

        tk.Button(post_ad_window, text="Save Advertisement", command=save_house_ad).pack(pady=10)

    def view_bookings(self):
        bookings_window = tk.Toplevel(self)
        bookings_window.title("View Bookings")
        bookings_window.geometry("600x400")

        tree = ttk.Treeview(
            bookings_window,
            columns=("Transaction ID", "Customer Name", "Amount", "Date"),
            show="headings"
        )
        tree.heading("Transaction ID", text="Transaction ID")
        tree.heading("Customer Name", text="Customer Name")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(bookings_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        transactions = Transaction.list_transactions_by_owner(self.current_user[0])

        if transactions:
            for transaction in transactions:
                tree.insert("", tk.END, values=transaction)
        else:
            messagebox.showinfo("No Data", "No bookings found!")


if __name__ == "__main__":
    create_tables()
    app = App()
    app.mainloop()
