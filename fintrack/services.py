import os
from typing import Literal

from fintrack.models import Transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


def create_transaction(user_id: int, title: str, amount: int, transaction_type: Literal['balance', 'expense']):
    """
    Creates a record in transaction table.
    :param user_id: User ID
    :param title: Transaction title
    :param amount: Transaction amount
    :param transaction_type: Transaction type ('balance' or 'expense')
    :returns: Transaction in a dictionary format
    """
    print(f'Creating transaction for user {user_id}: {title}, amount {amount}, type {transaction_type}')
    try:
        Transaction.objects.create(
            user_id=user_id,
            title=title,
            amount=amount,
            transaction_type=transaction_type,
        )
        return f"Transaction recorded of type {transaction_type}"
    except Exception as e:
        print(str(e))
        return f"Could not create transaction. Error: {str(e)}"


def get_current_balance(user_id):
    """
    Gets the last transaction and returns the balance of the transaction.
    :param user_id: User ID
    :returns: User current balance
    """
    print(f'Getting current balance for user {user_id}')
    last_transaction = Transaction.objects.filter(user_id=user_id).order_by('-created_at').first()
    return last_transaction.balance_after_transaction if last_transaction else 0


from typing import List, Dict, Optional
from datetime import datetime


def get_transaction_list(
        user_id: str,
        transaction_type: Literal['balance', 'expense'],
        order_by: str = '-created_at',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
) -> List[Dict]:
    """
    Retrieve a list of a user's financial transactions filtered, ordered, and serialized.
    Can be used to get transaction records.

    Args:
        user_id (str): The unique identifier of the user whose transactions are to be retrieved.
        transaction_type (Literal['balance', 'expense']): The type of transactions to retrieve.
            - 'balance' for balance-related transactions.
            - 'expense' for spending records.
        order_by (str, optional): Field by which to order the results (e.g., '-created_at' for most recent first).
        start_date (Optional[str], optional): A date string in 'YYYY-MM-DD' format. If provided, filters transactions
            created on or after this date.
        end_date (Optional[str], optional): A date string in 'YYYY-MM-DD' format. If provided, filters transactions
            created on or before this date.
        limit (int, optional): The maximum number of transactions to retrieve (max 100). Defaults to 100.
        offset (int, optional): The number of records to skip before returning results. Defaults to 0.

    Returns:
        List[Dict]: A list of dictionaries representing transactions, where each dictionary contains:
            - 'id': Transaction ID.
            - 'user_id': User ID.
            - 'transaction_type': 'balance' or 'expense'.
            - 'amount': Transaction amount.
            - 'description': Description of the transaction.
            - 'created_at': Timestamp of creation (ISO 8601 string).
            - Other fields relevant to the Transaction model.

    Raises:
        ValueError: If an invalid date format is provided for start_date or end_date.

    Notes:
        - Transactions are retrieved using Django's ORM and limited to 100 records to ensure performance.
        - If no transactions match the filters, an empty list is returned.
        - This function ensures safe serialization of the transactions for external use.
    """
    print(f'Passed values', user_id, start_date, end_date, limit, offset, transaction_type)
    limit = min(limit, 100)

    try:
        transactions = Transaction.objects.filter(
            user_id=user_id, transaction_type=transaction_type
        )
        if start_date:
            transactions = transactions.filter(created_at__gte=start_date)
        if end_date:
            transactions = transactions.filter(created_at__lte=f'{end_date} 23:59:59')
        transactions = transactions.order_by(order_by)[offset:offset + limit]
    except Exception as e:
        raise f"Error fetching transactions: {str(e)}"

    print('fetched results: ', transactions)

    return [
        {
            'id': t.id,
            'title': t.title,
            'transaction_type': t.transaction_type,
            'amount': t.amount,
            'description': t.description,
            'created_at': t.created_at.isoformat() if isinstance(t.created_at, datetime) else str(t.created_at),
        }
        for t in transactions
    ]
