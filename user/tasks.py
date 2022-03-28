from celery import shared_task
from celery.utils.log import get_task_logger
import user.models as um

logger = get_task_logger(__name__)


@shared_task
def make_bulk_payment(employees, description, admin_user, organisation):
    try:
        for employee in employees:
            logger.info('creating transaction')
            # Create Organisation Transaction
            um.Transaction.objects.create(wallet=organisation.wallet, type='withdrawal', amount=employee.get('amount'),
                                          is_verified=True, initiated_by=admin_user.id,
                                          initiator_wallet=organisation.wallet, created_by=admin_user.id,
                                          description=description)

            # Create Employee Transaction
            employee_wallet = um.Wallet.objects.get(address=employee.get('employee_wallet'))
            um.Transaction.objects.create(wallet=employee_wallet, type='deposit', amount=employee.get('amount'),
                                          is_verified=True, initiated_by=admin_user.id,
                                          initiator_wallet=organisation.wallet, created_by=admin_user.id,
                                          description=description)
            logger.info('done creating transaction')
    except Exception as e:
        print(str(e))


@shared_task
def make_employee_payment(employee_wallet, description, admin_user, organisation, amount):
    try:
        data = {
            "wallet": organisation.wallet,
            "type": 'withdrawal',
            'amount': amount,
            'is_verified': True,
            "initiated_by": admin_user.id,
            "initiator_wallet": organisation.wallet,
            "created_by": admin_user.id,
            "description": description
        }

        logger.info('creating transaction')
        # Create Organisation Transaction
        um.Transaction.objects.create(**data)

        # Create Employee Transaction
        wallet_employee = um.Wallet.objects.get(address=employee_wallet)
        um.Transaction.objects.create(wallet=wallet_employee, type='deposit', amount=amount,
                                      is_verified=True, initiated_by=admin_user.id,
                                      initiator_wallet=organisation.wallet, created_by=admin_user.id,
                                      description=description)
        logger.info('done creating transaction')
    except Exception as e:
        print(str(e))
