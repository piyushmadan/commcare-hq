from django.core.management import BaseCommand
from corehq.apps.accounting.invoicing import InvoiceTemplate


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        filename = 'my_test.pdf'

        try:
            generator = InvoiceTemplate(filename)
            generator.get_pdf()

            print "%s generated" % filename
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print tb
