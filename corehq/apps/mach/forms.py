from django.forms.fields import *
from corehq.apps.sms.forms import BackendForm
from dimagi.utils.django.fields import TrimmedCharField
from crispy_forms import layout as crispy
from django.utils.translation import ugettext_lazy as _


class MachBackendForm(BackendForm):
    account_id = TrimmedCharField(
        label=_("Account ID"),
    )
    password = TrimmedCharField(
        label=_("Password"),
    )
    sender_id = TrimmedCharField(
        label=_("Sender ID"),
    )

    @property
    def gateway_specific_fields(self):
        return crispy.Fieldset(
            _("Syniverse Settings"),
            'account_id',
            'password',
            'sender_id',
        )
