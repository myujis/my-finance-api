from .base import CRUDBase

from app.models.transactions import Transactions as TransactionsModel
from app.schemas.transactions import Transactions_Create, Transactions_Update, Transactions

transactions = CRUDBase[TransactionsModel, Transactions, Transactions_Create, Transactions_Update](Transactions)