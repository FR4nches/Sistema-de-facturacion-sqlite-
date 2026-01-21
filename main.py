import ttkbootstrap as ttk
from controllers.login_controller import LoginController


def main():
    app = ttk.Window(title="Sistema POS", themename="cosmo", size=(1100, 650))
    LoginController(app, db_path="pos_system.db")
    app.mainloop()


if __name__ == "__main__":
    main()
