from accounts.models import Account

account_data_patient = {
    'password': 'test123',
    'last_name': 'test123',
    'first_name': 'test123',
    'email': 'test123@test.com',
    'age': 32,
    'profile': 0,
    'phone_number': 999888444,
}

def create_account():
    account = Account.objects.create_user(**account_data_patient)
    return account
