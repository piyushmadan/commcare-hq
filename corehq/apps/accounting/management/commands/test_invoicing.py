import datetime
from django.core.management import BaseCommand
from corehq.apps.accounting.invoicing import InvoiceTemplate, Address


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        filename = 'my_test.pdf'

        try:
            from_address = Address(
                first_line='585 Massachusetts Ave',
                second_line='Suite 3',
                city='Cambridge',
                region='MA',
                postal_code='02139',
                country='USA',
                phone_number='(617) 649-2214',
                email_address='admin@dimagi.com',
                website='http://dimagi.com',
            )

            to_address = Address(
                first_line='Example address',
                website='website',
            )

            bank_address = Address(
                first_line='1 Citizens Drive',
                city='Riverside',
                region='RI',
                postal_code='02915'
            )

            template = InvoiceTemplate(
                filename,
                from_address=from_address,
                to_address=to_address,
                project_name='nick-project',
                invoice_number='HQ-5001',
                terms='Net 30',
                total=13.5,
                bank_name='RBS Citizens N.A.',
                bank_address=bank_address,
                account_number='5555555555',
                routing_number='555555555',
                swift_code='AAAAAA55',
            )

            template.add_item(
                datetime.date.today(),
                "A charge on the account",
                2,
                1.5
            )

            for _ in range(13):
                template.add_item(
                    datetime.date.today() - datetime.timedelta(days=2),
                    "Another charge",
                    1,
                    4
                )
            template.get_pdf()

            print "%s generated" % filename
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print tb
