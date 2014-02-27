from django.core.management import BaseCommand
from corehq.apps.accounting.invoicing import InvoiceTemplate, Address


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        filename = 'my_test.pdf'

        try:
            from_address = Address(first_line='585 Massachusetts Ave',
                                   second_line='Suite 3',
                                   city='Cambridge',
                                   region='MA',
                                   postal_code='02139',
                                   country='USA',
                                   phone_number='(617) 649-2214',
                                   email_address='admin@dimagi.com',
                                   website='http://dimagi.com')

            generator = InvoiceTemplate(filename,
                                        from_address=from_address)
            generator.get_pdf()

            print "%s generated" % filename
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print tb
