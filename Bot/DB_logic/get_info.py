from basic_logic.config import cur

class UserData():
    def DB_get_tg_phone(user_id: int) -> str:
        return cur.execute(f"SELECT telegram_phone_number FROM customers WHERE tg_id={user_id}").fetchall()[0][0]

    def user_exist(user_id: int) -> bool:
        return bool(cur.execute(f"SELECT 1 FROM customers WHERE tg_id={user_id}").fetchone())