from couchdbkit.ext.django.schema import (Document, StringProperty,
    StringListProperty, IntegerProperty, ListProperty)

from ..opm_reports.constants import DOMAIN, InvalidRow


class OpmReportSnapshot(Document):
    """
    Represents a snapshot of a report, to be taken at the end of each month
    """
    domain = StringProperty()
    month = IntegerProperty()
    year = IntegerProperty()
    report_class = StringProperty()
    headers = StringListProperty()
    slugs = StringListProperty()
    rows = ListProperty()
    block = StringProperty()
    visible_cols = ListProperty()

    @classmethod
    def by_month(cls, month, year, report_class, block=None):
        return cls.view(
            'opm_tasks/opm_snapshots',
            key=[DOMAIN, month, year, report_class, block],
            reduce=False,
            include_docs=True
        ).first()

    @classmethod
    def filtered(cls, snapshot, report):
        filtered_rows = []

        need_filering = False
        filters = []
        for key, field in report.filter_fields:
            keys = report.filter_data.get(field, [])
            if keys:
                need_filering = True
                filters.append((key, field))
        if need_filering:
            for row in snapshot.rows:
                def key_finder(key):
                    index = snapshot.slugs.index(key)
                    return row[index]
                try:
                    report.filter(fn=key_finder, filter_fields=filters)
                except InvalidRow:
                    pass
                else:
                    filtered_rows.append(row)
            snapshot.rows = filtered_rows
        return snapshot

    @classmethod
    def from_view(cls, report):
        block = None
        if report.block:
            block = report.block.lower()
        snapshot = cls.view(
            'opm_tasks/opm_snapshots',
            key=[DOMAIN, report.month, report.year, report.__class__.__name__, block],
            reduce=False,
            include_docs=True
        ).first()
        if not snapshot:
            return None
        return cls.filtered(snapshot, report)
