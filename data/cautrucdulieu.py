from datetime import datetime

class User:
    def __init__(self, user_id, first_name, last_name, phone_number, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_contact_info(self, phone_number=None, email=None):
        if phone_number:
            self.phone_number = phone_number
        if email:
            self.email = email


class Customer(User):
    def __init__(self, user_id, first_name, last_name, phone_number, email, customer_id, address, registration_date, money):
        super().__init__(user_id, first_name, last_name, phone_number, email)
        self.customer_id = customer_id
        self.address = address
        self.registration_date = registration_date
        self.money = money
        self.order_history = []

    def add_order(self, order_list, order):
        if not hasattr(order_list, "add_order"):
            raise TypeError("order_list must have an add_order method.")
        self.order_history.append(order)
        order_list.add_order(order)

    def get_order_history(self):
        return self.order_history

    def update_balance(self, amount):
        self.money += amount


class Admin(User):
    def __init__(self, user_id, first_name, last_name, phone_number, email, admin_id, role):
        super().__init__(user_id, first_name, last_name, phone_number, email)
        self.admin_id = admin_id
        self.role = role

    def update_role(self, new_role):
        self.role = new_role


class Dish:
    def __init__(self, dish_id, name, price, dish_type, description, quantity=1):
        self.dish_id = dish_id
        self.name = name
        self.price = price
        self.dish_type = dish_type
        self.description = description
        self.quantity = quantity
        self.amount = self.calculate_total_amount()

    def calculate_total_amount(self):
        return self.price * self.quantity


class DishList:
    def __init__(self):
        self.dishes = []

    def add_dish(self, dish):
        self.dishes.append(dish)

    def remove_dish(self, dish_id):
        self.dishes = [dish for dish in self.dishes if dish.dish_id != dish_id]

    def get_all_dishes(self):
        return self.dishes

    def get_dish_by_name(self, name):
        for dish in self.dishes:
            if dish.name.lower() == name.lower():
                return dish
        return None


class Order:
    def __init__(self, order_id, customer_id, order_date, total_amount=0, status="Pending"):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.status = status
        self.dishes = []
        self.status_history = [(status, datetime.utcnow())]

    def add_dish(self, dish):
        self.dishes.append(dish)
        self.update_total_amount()

    def update_total_amount(self):
        self.total_amount = sum(dish.calculate_total_amount() for dish in self.dishes)

    def update_status(self, new_status):
        valid_statuses = ["Pending", "Paid", "Ready for Delivery", "Cancelled", "Completed"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid order status: {new_status}.")
        self.status = new_status
        self.status_history.append((new_status, datetime.utcnow()))

    def get_order_details(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "total_amount": self.total_amount,
            "status": self.status,
            "dishes": [dish.name for dish in self.dishes]
        }


class Reservation:
    def __init__(self, reservation_id, customer_id, reservation_date, number_of_guests, special_requests=None, deposit_amount=0):
        if reservation_date < datetime.utcnow():
            raise ValueError("Reservation date cannot be in the past.")
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.reservation_date = reservation_date
        self.reservation_status = "Pending"
        self.number_of_guests = number_of_guests
        self.special_requests = special_requests if special_requests else []
        self.deposit_amount = deposit_amount
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_reservation(self, reservation_status=None, special_requests=None, number_of_guests=None):
        if reservation_status and reservation_status not in ["Pending", "Confirmed", "Cancelled"]:
            raise ValueError("Invalid reservation status.")
        if number_of_guests and number_of_guests <= 0:
            raise ValueError("Number of guests must be greater than 0.")

        if reservation_status and reservation_status != self.reservation_status:
            self.reservation_status = reservation_status
        if special_requests:
            self.special_requests.append(special_requests)
        if number_of_guests:
            self.number_of_guests = number_of_guests

        self.updated_at = datetime.utcnow()


class Feedback:
    def __init__(self, feedback_id, customer_id, order_id, feedback_text, rating, created_at=None):
        self.feedback_id = feedback_id
        self.customer_id = customer_id
        self.order_id = order_id
        self.feedback_text = feedback_text
        self.rating = rating
        self.created_at = created_at if created_at else datetime.utcnow()

    def update_feedback(self, feedback_text=None, rating=None):
        if feedback_text:
            self.feedback_text = feedback_text
        if rating:
            self.rating = rating


class Delivery:
    def __init__(self, delivery_id, order, delivery_partner, delivery_date, tracking_number=None, delivery_status="Pending"):
        if not isinstance(order, Order):
            raise TypeError("The order must be an instance of the Order class.")
        if order.status not in ["Paid", "Ready for Delivery"]:
            raise ValueError("Delivery can only be created for orders that are 'Paid' or 'Ready for Delivery'.")
        self.delivery_id = delivery_id
        self.order = order
        self.delivery_partner = delivery_partner
        self.delivery_date = delivery_date
        self.tracking_number = tracking_number
        self.delivery_status = delivery_status

    def update_delivery_status(self, new_status):
        valid_statuses = ["Pending", "In Transit", "Delivered", "Cancelled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid delivery status: {new_status}.")
        self.delivery_status = new_status
        if new_status == "Delivered" and self.order.status == "Ready for Delivery":
            self.order.update_status("Completed")

    def get_delivery_details(self):
        return {
            "delivery_id": self.delivery_id,
            "order_id": self.order.order_id,
            "delivery_partner": self.delivery_partner,
            "delivery_date": self.delivery_date,
            "tracking_number": self.tracking_number,
            "delivery_status": self.delivery_status,
            "order_details": self.order.get_order_details()
        }

