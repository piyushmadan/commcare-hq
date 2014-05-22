from django.forms.fields import *
from corehq.apps.sms.forms import BackendForm
from dimagi.utils.django.fields import TrimmedCharField
from crispy_forms import layout as crispy
from django.utils.translation import ugettext_lazy as _


class TwilioBackendForm(BackendForm):
    account_sid = TrimmedCharField(
        label=_("Account SID"),
    )
    auth_token = TrimmedCharField(
        label=_("Auth Token"),
    )
    phone_number = TrimmedCharField(
        label=_("Phone Number"),
        help_text=_(
            "For short codes, just enter the short code. For phone numbers, "
            "enter the number in international format including the '+' sign."
        )
    )

    @property
    def gateway_specific_fields(self):
        return crispy.Fieldset(
            _("Twilio Settings"),
            'account_sid',
            'auth_token',
            'phone_number',
        )
