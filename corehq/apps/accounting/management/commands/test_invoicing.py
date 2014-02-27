from django.core.management import BaseCommand
from corehq.apps.accounting.invoicing import InvoiceTemplate


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        generator = InvoiceTemplate('my_test.pdf')
        generator.get_pdf()

        print "%s generated" % self.filename
