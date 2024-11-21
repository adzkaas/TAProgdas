
from abc import ABC, abstractmethod

class Payment(ABC):  # Kelas abstrak untuk pembayaran
    @abstractmethod
    def choose_payment_method(self, method):
        pass

class CashPayment(Payment):
    def choose_payment_method(self, method):
        return f"Pembayaran dengan {method}"

class NonCashPayment(Payment):
    def choose_payment_method(self, method):
        return f"Pembayaran dengan {method}"
