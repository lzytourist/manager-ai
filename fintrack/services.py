import os
from datetime import datetime
from typing import List, Literal, Dict, Optional

from django.db.models import Sum, Case, When, F, Value, Q
from django.db.models.fields import DecimalField

from fintrack.models import Transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


def create_transaction(user_id: int, title: str, description: Optional[str], amount: int,
                       transaction_type: Literal['balance', 'expense']):
    """
    Creates a record in transaction table.
    :param user_id: User ID
    :param title: Transaction title
    :param amount: Transaction amount
    :param description: Details about the Transaction made
    :param transaction_type: Transaction type ('balance' or 'expense')
    :returns: Transaction in a dictionary format
    """
    print(
        f'Creating transaction for user {user_id}: {title}, amount {amount}, type {transaction_type}, description {description}')
    try:
        Transaction.objects.create(
            user_id=user_id,
            title=title,
            amount=amount,
            description=description,
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
    result = (
        Transaction.objects.filter(user_id=user_id).aggregate(
            current_balance=Sum(
                Case(
                    When(transaction_type=Transaction.Type.BALANCE, then=F('amount')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ) - Sum(
                Case(
                    When(transaction_type=Transaction.Type.EXPENSE, then=F('amount')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        )
    )
    return result['current_balance']


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


def search_transactions(search_text: str) -> List[Dict]:
    """
    Search for transactions matching a search text. Searches are done for title, description, transaction type, and amount.
    Better way of searching is to use words and use it for search_text, then join other words to narrow down the results.
    Args:
        search_text (str): The search text.
    Returns:
        List[Dict]: A list of dictionaries representing transactions, where each dictionary contains: Transaction details
    """
    print('Searching transactions...', search_text)
    transactions = Transaction.objects.filter(
        Q(title__icontains=search_text) |
        Q(description__icontains=search_text) |
        Q(transaction_type__icontains=search_text)
    )[:20]
    print('Fetched search results: ', transactions)
    return [
        {
            'id': transaction.id,
            'title': transaction.title,
            'description': transaction.description,
            'transaction_type': transaction.transaction_type,
            'amount': transaction.amount,
            'created_at': transaction.created_at.isoformat() if isinstance(transaction.created_at, datetime) else str(
                transaction.created_at),
        }
        for transaction in transactions
    ]


def get_transaction_by_id(transaction_id: int) -> [Dict | str]:
    """
    Retrieve a transaction by its ID.
    Args:
        transaction_id (int): The unique identifier of the transaction.
    Returns:
        List[Dict]: A list of dictionaries representing transactions, where each dictionary contains: Transaction details,
        or provides a string containing transaction not found and error from backend system.
    """
    print('Getting transaction by ID:', transaction_id)
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        return {
            'id': transaction.id,
            'title': transaction.title,
            'description': transaction.description,
            'created_at': transaction.created_at.isoformat() if isinstance(transaction.created_at, datetime) else str(
                transaction.created_at),
            'transaction_type': transaction.transaction_type,
            'amount': transaction.amount,
        }
    except Transaction.DoesNotExist as e:
        return f'Transaction not found: {str(e)}'


def update_transaction(transaction_id: int, update_fields: dict) -> str:
    """
    Update a transaction by its ID.
    Args:
        transaction_id (int): The unique identifier of the transaction.
        update_fields (dict): The fields to update on the transaction. Provided in key value pairs.
    Returns:
        str: The updated message.
    """
    print('Updating transaction...', transaction_id, update_fields)
    try:
        Transaction.objects.filter(id=transaction_id).update(**update_fields)
        return 'Transaction updated.'
    except Transaction.DoesNotExist as e:
        return f'Transaction not found: {str(e)}'
