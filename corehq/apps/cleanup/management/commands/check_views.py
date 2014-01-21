from optparse import make_option
import re
from django.core.management.base import BaseCommand
import csv
import logging
from dimagi.utils.couch.database import get_db

logger = logging.getLogger(__name__)

VIEWS = [
    "_design/adm/_view/all_default_columns",
    "_design/adm/_view/all_default_reports",
    "_design/adm/_view/configurable_columns",
    "_design/announcements/_view/all_announcements",
    "_design/announcements/_view/notifications",
    "_design/app_manager/_view/applications",
    "_design/app_manager/_view/applications_brief",
    "_design/app_manager/_view/builds_by_date",
    "_design/app_manager/_view/saved_app",
    "_design/app_manager/_view/settings",
    "_design/app_manager/_view/types_by_module",
    "_design/app_manager/_view/xforms_index",
    "_design/appstore/_view/by_app",
    "_design/appstore/_view/by_version",
    "_design/auditcare/_view/all_events",
    "_design/auditcare/_view/by_date",
    "_design/auditcare/_view/by_date_access_events",
    "_design/auditcare/_view/by_date_events",
    "_design/auditcare/_view/login_events",
    "_design/auditcare/_view/model_actions_by_id",
    "_design/auditcare/_view/urlpath_by_user_date",
    "_design/benin/_view/by_user_form",
    "_design/benin/_view/by_village_case",
    "_design/benin/_view/by_village_form",
    "_design/benin/_view/danger_signs",
    "_design/benin/_view/outcomes",
    "_design/builds/_view/all",
    "_design/callcenter/_view/case_actions_by_user",
    "_design/care_benin/_view/by_user_form",
    "_design/care_benin/_view/by_village_case",
    "_design/care_benin/_view/by_village_form",
    "_design/care_benin/_view/danger_signs",
    "_design/care_benin/_view/outcomes",
    "_design/case/_view/all_cases",
    "_design/case/_view/by_date_modified",
    "_design/case/_view/by_date_modified_owner",
    "_design/case/_view/by_owner",
    "_design/case/_view/by_owner_lite",
    "_design/case/_view/by_user",
    "_design/case/_view/by_xform_id",
    "_design/case/_view/form_case_index",
    "_design/case/_view/get_lite",
    "_design/case/_view/groups_by_domain",
    "_design/case/_view/open_cases",
    "_design/case/_view/related",
    "_design/cleanup/_view/case_submissions",
    "_design/cleanup/_view/submissions",
    "_design/cloudcare/_view/application_access",
    "_design/cloudcare/_view/case_specs_by_domain_case_type",
    "_design/cloudcare/_view/cloudcare_apps",
    "_design/commtrack/_view/current_stock_status",
    "_design/commtrack/_view/domain_config",
    "_design/commtrack/_view/locations_by_code",
    "_design/commtrack/_view/product_by_code",
    "_design/commtrack/_view/product_by_program_id",
    "_design/commtrack/_view/product_cases",
    "_design/commtrack/_view/products",
    "_design/commtrack/_view/program_by_code",
    "_design/commtrack/_view/programs",
    "_design/commtrack/_view/requisitions",
    "_design/commtrack/_view/stock_product_state",
    "_design/commtrack/_view/stock_reports",
    "_design/commtrack/_view/stock_transactions",
    "_design/commtrack/_view/stock_transactions_by_product",
    "_design/commtrack/_view/supply_point_by_loc",
    "_design/commtrack/_view/supply_point_types",
    "_design/couchexport/_view/saved_export_schemas",
    "_design/couchexport/_view/saved_exports",
    "_design/couchexport/_view/schema_checkpoints",
    "_design/couchexport/_view/schema_index",
    "_design/couchforms/_view/all_submissions_by_domain",
    "_design/couchforms/_view/by_user",
    "_design/couchforms/_view/by_xmlns",
    "_design/couchforms/_view/edits",
    "_design/crs_reports/_view/field_block",
    "_design/ctable/_view/by_name",
    "_design/ctable/_view/schedule",
    "_design/cvsu/_view/abuse",
    "_design/cvsu/_view/debug",
    "_design/cvsu/_view/incidents_outreach",
    "_design/cvsu/_view/resolutions",
    "_design/cvsu/_view/services",
    "_design/dca/_view/dca_collection_forms",
    "_design/dca/_view/dca_collection_forms_by_case",
    "_design/dca/_view/dca_registration_forms",
    "_design/doc_summary/_view/summary",
    "_design/domain/_view/by_organization",
    "_design/domain/_view/by_status",
    "_design/domain/_view/copied_from_snapshot",
    "_design/domain/_view/counter",
    "_design/domain/_view/docs",
    "_design/domain/_view/domains",
    "_design/domain/_view/fields_by_prefix",
    "_design/domain/_view/not_snapshots",
    "_design/domain/_view/published_snapshots",
    "_design/domain/_view/related_to_domain",
    "_design/domain/_view/snapshots",
    "_design/domain/_view/with_deployment",
    "_design/eula_report/_view/noneulized_users",
    "_design/exports_forms/_view/by_xmlns",
    "_design/facilities/_view/facilities_by_registry",
    "_design/facilities/_view/registries_by_domain",
    "_design/fixtures/_view/data_items_by_domain_type",
    "_design/fixtures/_view/data_items_by_field_value",
    "_design/fixtures/_view/data_types_by_domain",
    "_design/fixtures/_view/data_types_by_domain_tag",
    "_design/fixtures/_view/ownership",
    "_design/formtrends/_view/form_duration_by_user",
    "_design/fri/_view/message_bank",
    "_design/fri/_view/randomized_message",
    "_design/groupexport/_view/by_domain",
    "_design/groups/_view/all_groups",
    "_design/groups/_view/by_domain",
    "_design/groups/_view/by_hierarchy_type",
    "_design/groups/_view/by_name",
    "_design/groups/_view/by_user",
    "_design/groups/_view/by_user_type",
    "_design/gsid/_view/patient_summary",
    "_design/hqadmin/_view/active_domains_over_time",
    "_design/hqadmin/_view/active_users_over_time",
    "_design/hqadmin/_view/cases_over_time",
    "_design/hqadmin/_view/deploy_history",
    "_design/hqadmin/_view/domains_over_time",
    "_design/hqadmin/_view/emails",
    "_design/hqadmin/_view/forms_over_time",
    "_design/hqadmin/_view/users_over_time",
    "_design/hqbilling/_view/currencies",
    "_design/hqbilling/_view/domains_marked_for_billing",
    "_design/hqbilling/_view/domains_with_billables",
    "_design/hqbilling/_view/mach_billables",
    "_design/hqbilling/_view/mach_phone_numbers",
    "_design/hqbilling/_view/monthly_bills",
    "_design/hqbilling/_view/sms_billables",
    "_design/hqbilling/_view/sms_rates",
    "_design/hqbilling/_view/tax_rates",
    "_design/hqcase/_view/all_case_properties",
    "_design/hqcase/_view/by_domain_external_id",
    "_design/hqcase/_view/by_domain_hq_user_id",
    "_design/hqcase/_view/by_owner",
    "_design/hqcase/_view/types_by_domain",
    "_design/hqmedia/_view/by_doc_type",
    "_design/hqmedia/_view/by_domain",
    "_design/hqmedia/_view/by_hash",
    "_design/hqmedia/_view/tags",
    "_design/hsph/_view/cases_by_birth_date_old",
    "_design/hsph/_view/cati_performance",
    "_design/hsph/_view/cati_performance_report_old",
    "_design/hsph/_view/cati_team_leader",
    "_design/hsph/_view/data_summary",
    "_design/hsph/_view/data_summary_old",
    "_design/hsph/_view/dcc_followup_summary_old",
    "_design/hsph/_view/facility_registrations",
    "_design/hsph/_view/facility_wise_follow_up",
    "_design/hsph/_view/fada_observations",
    "_design/hsph/_view/fida_performance",
    "_design/hsph/_view/field_data_collection_activity_old",
    "_design/hsph/_view/field_dco_activity_old",
    "_design/hsph/_view/field_follow_up_status_old",
    "_design/hsph/_view/field_process_data_old",
    "_design/hsph/_view/pm_implementation_status_old",
    "_design/hsph/_view/pm_project_status_old",
    "_design/indicators/_view/available_to_combine",
    "_design/indicators/_view/dynamic_indicator_definitions",
    "_design/indicators/_view/form_labels",
    "_design/indicators/_view/indicator_definitions",
    "_design/languages/_view/list",
    "_design/locations/_view/by_name",
    "_design/locations/_view/by_type",
    "_design/locations/_view/hierarchy",
    "_design/locations/_view/linked_docs",
    "_design/locations/_view/post_move_processing",
    "_design/locations/_view/prop_index_site_code",
    "_design/migration/_view/user_id_by_username",
    "_design/mobile_auth/_view/key_records",
    "_design/mvp_births/_view/child_cases_by_status",
    "_design/mvp_births/_view/child_registrations",
    "_design/mvp_child_health/_view/child_case_indicators",
    "_design/mvp_child_health/_view/child_muac",
    "_design/mvp_child_health/_view/under5_child_health",
    "_design/mvp_chw_referrals/_view/urgent_referrals_by_case",
    "_design/mvp_chw_visits/_view/all_cases",
    "_design/mvp_chw_visits/_view/all_visit_forms",
    "_design/mvp_deaths/_view/over5_deaths",
    "_design/mvp_deaths/_view/pregnancy_close",
    "_design/mvp_deaths/_view/under5_deaths",
    "_design/mvp_maternal_health/_view/anc_visits",
    "_design/mvp_maternal_health/_view/family_planning",
    "_design/mvp_maternal_health/_view/pregnancy_danger_signs",
    "_design/mvp_over5/_view/over5_health",
    "_design/opm_tasks/_view/opm_snapshots",
    "_design/orgs/_view/by_name",
    "_design/orgs/_view/org_requests",
    "_design/orgs/_view/team_by_domain",
    "_design/orgs/_view/team_by_org_and_name",
    "_design/pact/_view/chw_dot_schedules",
    "_design/pact/_view/dots_observations",
    "_design/pathfinder/_view/pathfinder_all_wards",
    "_design/pathfinder/_view/pathfinder_gov_followup_by_caseid",
    "_design/pathfinder/_view/pathfinder_gov_referral",
    "_design/pathfinder/_view/pathfinder_gov_reg_by_username",
    "_design/pathfinder/_view/pathfinder_xforms",
    "_design/pathindia/_view/kranti_cases",
    "_design/pathindia/_view/kranti_report",
    "_design/penn_state/_view/smiley_weekly_reports",
    "_design/phone/_view/case_modification_status",
    "_design/phone/_view/cases_to_sync_logs",
    "_design/phone/_view/sync_logs_by_user",
    "_design/phonelog/_view/device_log_first_last",
    "_design/phonelog/_view/device_log_tags",
    "_design/phonelog/_view/device_log_uniq",
    "_design/phonelog/_view/device_log_users",
    "_design/phonelog/_view/device_logs",
    "_design/phonelog/_view/devicelog_data",
    "_design/phonelog/_view/devicelog_data_devices",
    "_design/phonelog/_view/devicelog_data_users",
    "_design/prescriptions/_view/all",
    "_design/psi/_view/events",
    "_design/psi/_view/household_demonstrations",
    "_design/psi/_view/sensitization",
    "_design/psi/_view/training",
    "_design/receiverwrapper/_view/all_submissions_by_domain",
    "_design/receiverwrapper/_view/repeat_records_by_next_check",
    "_design/receiverwrapper/_view/repeaters",
    "_design/registration/_view/requests_by_guid",
    "_design/registration/_view/requests_by_time",
    "_design/registration/_view/requests_by_username",
    "_design/reminders/_view/by_domain_handler_case",
    "_design/reminders/_view/by_next_fire",
    "_design/reminders/_view/handlers_by_domain_case_type",
    "_design/reminders/_view/handlers_by_reminder_type",
    "_design/reminders/_view/reminders_in_error",
    "_design/reminders/_view/sample_by_domain",
    "_design/reminders/_view/sample_to_survey",
    "_design/reminders/_view/survey_by_domain",
    "_design/reminders/_view/survey_keywords",
    "_design/reportconfig/_view/all_notifications",
    "_design/reportconfig/_view/configs_by_domain",
    "_design/reportconfig/_view/notifications_by_config",
    "_design/reportconfig/_view/user_notifications",
    "_design/reports/_view/case_activity",
    "_design/reports/_view/case_activity_cache",
    "_design/reports/_view/maps_config",
    "_design/reports_apps/_view/remote",
    "_design/reports_forms/_view/all_forms",
    "_design/reports_forms/_view/all_submitted_users",
    "_design/reports_forms/_view/by_app_info",
    "_design/reports_forms/_view/name_by_xmlns",
    "_design/sms/_view/backend_by_domain",
    "_design/sms/_view/backend_by_owner_domain",
    "_design/sms/_view/backend_map",
    "_design/sms/_view/by_domain",
    "_design/sms/_view/by_recipient",
    "_design/sms/_view/call_by_session",
    "_design/sms/_view/direction_by_domain",
    "_design/sms/_view/expected_callback_event",
    "_design/sms/_view/forwarding_rule",
    "_design/sms/_view/global_backends",
    "_design/sms/_view/migrate_smslog_2012_04",
    "_design/sms/_view/old_mobile_backend",
    "_design/sms/_view/phones_to_domains",
    "_design/sms/_view/queued_sms",
    "_design/sms/_view/verified_number_by_doc_type_id",
    "_design/sms/_view/verified_number_by_domain",
    "_design/sms/_view/verified_number_by_number",
    "_design/sms/_view/verified_number_by_owner_id",
    "_design/sms/_view/verified_number_by_suffix",
    "_design/smsforms/_view/open_sms_sessions_by_connection",
    "_design/smsforms/_view/sessions_by_touchforms_id",
    "_design/submituserlist/_view/all_users",
    "_design/telerivet/_view/backend_by_secret",
    "_design/translations/_view/popularity",
    "_design/trialconnect/_view/smslogs",
    "_design/users/_view/admins_by_domain",
    "_design/users/_view/by_default_phone",
    "_design/users/_view/by_domain",
    "_design/users/_view/by_group",
    "_design/users/_view/by_org_and_team",
    "_design/users/_view/by_username",
    "_design/users/_view/deleted_cases_by_user",
    "_design/users/_view/deleted_forms_by_user",
    "_design/users/_view/mailing_list_emails",
    "_design/users/_view/old_users",
    "_design/users/_view/open_invitations_by_domain",
    "_design/users/_view/phone_users_by_domain",
    "_design/users/_view/roles_by_domain",
    "_design/users/_view/web_users_by_domain",
    "_design/wisepill/_view/device",
    "_design/wisepill/_view/device_event",
]

def all_ddocs():
    ddocs = get_db().all_docs(startkey="_design",
                        endkey="_design/"+u"\u9999",
                        include_docs=True)
    for ddoc in ddocs:
        yield ddoc["doc"]

class Command(BaseCommand):
    help = ('Checks all views to see which doc_types they handle')

    option_list = BaseCommand.option_list + (
        make_option('-f', '--filename',
            help="Save output to this file."),
        make_option('-o', "--old", "--from_files", action="store_true",
            help="Old method for retrieving design docs."),
        make_option('--verbose', action="store_true",
            help="Verbose"),
        )

    def handle(self, *args, **options):
        filename = options.get("filename") or "couchview_info"
        if not filename.endswith(".csv"):
            filename = "%s.csv" % filename
        verbose, from_files = options.get("verbose"), options.get("from_files")
        logger.info("writing to file: %s" % filename)

        def parse_views(txt):
            tokens = txt.split('/')
            return tokens[1], tokens[3]

        def possible_filenames(app, name):
            yield "app view", "corehq/apps/%s/_design/views/%s/map.js" % (app, name)
            yield "couchapp view", "corehq/couchapps/%s/_design/views/%s/map.js" % (app, name)

        def find_equality_check(txt, checking):
            p = re.compile('%s ==+ ["\']+(.+?)["\']+' % checking)
            return p.findall(txt)


        csvfile = open(filename, 'wb+')
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        if from_files:
            csv_writer.writerow(['app', 'name', 'filename', 'type', 'doc_types', 'other'])
            for app, name in map(parse_views, VIEWS):
                print app, name

                for viewtype, fname in possible_filenames(app, name):
                    try:
                        f = open(fname, 'r')
                        filetxt = " ".join(f.readlines())
                        doc_types = find_equality_check(filetxt, "doc_type")
                        base_docs = find_equality_check(filetxt, "base_doc")
                        base_types = find_equality_check(filetxt, "base_type")
                        csv_writer.writerow([app, name, fname, viewtype, " ".join(doc_types), " ".join(base_docs + base_types)])
                        f.close()
                        break
                    except IOError:
                        continue
                else:
                    csv_writer.writerow([app, name, "view not found", "", "", ""])

        else:
            csv_writer.writerow(['key', 'viewname', 'type', 'doc_types', 'other'])

            for ddoc in all_ddocs():
                key = ddoc["_id"]
                for view, view_doc in ddoc.get("views", {}).iteritems():
                    map_view = view_doc["map"]
                    doc_types = find_equality_check(map_view, "doc_type")
                    base_docs = find_equality_check(map_view, "base_doc")
                    base_types = find_equality_check(map_view, "base_type")
                    csv_writer.writerow([key, view, "view", " ".join(doc_types), " ".join(base_docs + base_types)])
                for filter, filter_doc in ddoc.get("filters", {}).iteritems():
                    doc_types = find_equality_check(filter_doc, "doc_type")
                    base_docs = find_equality_check(filter_doc, "base_doc")
                    base_types = find_equality_check(filter_doc, "base_type")
                    csv_writer.writerow([key, filter, "filter", " ".join(doc_types), " ".join(base_docs + base_types)])

        csvfile.close()
