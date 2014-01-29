import os
import uuid
from corehq.apps.commtrack.tests.util import CommTrackTest
from corehq.apps.receiverwrapper import submit_form_locally
from casexml.apps.stock.models import StockTransaction

class IntrahealthSubmissionTest(CommTrackTest):

    def test_intrahealth(self):
        dir = os.path.dirname(__file__)
        filename = 'intrahealth.xml'
        file = os.path.join(dir, 'data', 'xml', filename)
        with open(file) as f:
            xml = f.read()

        from casexml.apps.case import settings
        settings.CASEXML_FORCE_DOMAIN_CHECK = False
        instance_id = uuid.uuid4().hex
        instance = xml.format(
            instance_id=instance_id,
            case_id=self.sp._id,
            user_id=self.user._id,
            p1_id=self.products[0]._id,
            p2_id=self.products[1]._id,
            p3_id=self.products[2]._id,
        )
        submit_form_locally(
            instance=instance,
            domain=self.domain.name,
        )
        self.assertEqual(3, StockTransaction.objects.count())

