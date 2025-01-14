from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from messaging.filters import ContactFilterSet, ContactRoleFilterSet, EmailFilterSet
from messaging.forms import (
    ContactAssignmentForm,
    ContactBulkEditForm,
    ContactFilterForm,
    ContactForm,
    ContactRoleBulkEditForm,
    ContactRoleFilterForm,
    ContactRoleForm,
    EmailFilterForm,
    EmailForm,
)
from messaging.models import Contact, ContactAssignment, ContactRole, Email
from messaging.tables import (
    ContactAssignmentTable,
    ContactRoleTable,
    ContactTable,
    EmailTable,
)
from utils.functions import count_related
from utils.tables import paginate_table
from utils.views import (
    AddOrEditView,
    BulkDeleteView,
    BulkEditView,
    DeleteView,
    DetailsView,
    ModelListView,
    PermissionRequiredMixin,
)


class ContactRoleList(PermissionRequiredMixin, ModelListView):
    permission_required = "messaging.view_contactrole"
    queryset = ContactRole.objects.all()
    filter = ContactRoleFilterSet
    filter_form = ContactRoleFilterForm
    table = ContactRoleTable
    template = "messaging/contactrole/list.html"


class ContactRoleDetails(DetailsView):
    permission_required = "messaging.view_contactrole"
    queryset = ContactRole.objects.all()

    def get_context(self, request, **kwargs):
        return {
            "instance": get_object_or_404(self.queryset, **kwargs),
            "active_tab": "main",
        }


class ContactRoleAdd(PermissionRequiredMixin, AddOrEditView):
    permission_required = "messaging.add_contactrole"
    model = ContactRole
    form = ContactRoleForm
    return_url = "bgp:relationship_list"
    template = "bgp/relationship/add_edit.html"


class ContactRoleEdit(PermissionRequiredMixin, AddOrEditView):
    permission_required = "messaging.change_contactrole"
    model = ContactRole
    form = ContactRoleForm
    template = "messaging/contactrole/add_edit.html"


class ContactRoleBulkEdit(PermissionRequiredMixin, BulkEditView):
    permission_required = "messaging.change_contactrole"
    queryset = ContactRole.objects.all()
    filter = ContactRoleFilterSet
    table = ContactRoleTable
    form = ContactRoleBulkEditForm


class ContactRoleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "messaging.delete_contactrole"
    model = ContactRole
    return_url = "messaging:contactrole_list"


class ContactRoleBulkDelete(PermissionRequiredMixin, BulkDeleteView):
    permission_required = "messaging.delete_contactrole"
    model = ContactRole
    filter = ContactRoleFilterSet
    table = ContactRoleTable


class ContactList(PermissionRequiredMixin, ModelListView):
    permission_required = "messaging.view_contact"
    queryset = Contact.objects.annotate(
        assignment_count=count_related(ContactAssignment, "contact")
    )
    filter = ContactFilterSet
    filter_form = ContactFilterForm
    table = ContactTable
    template = "messaging/contact/list.html"


class ContactDetails(PermissionRequiredMixin, ModelListView):
    permission_required = "messaging.view_contact"
    table = ContactAssignmentTable
    template = "messaging/contact/details.html"

    def build_queryset(self, request, kwargs):
        instance = get_object_or_404(Contact, pk=kwargs["pk"])
        return ContactAssignment.objects.filter(contact=instance)

    def extra_context(self, kwargs):
        instance = get_object_or_404(Contact, pk=kwargs["pk"])

        return {
            "instance": instance,
            "assignment_count": ContactAssignment.objects.filter(
                contact=instance
            ).count(),
            "active_tab": "main",
        }


class ContactAdd(PermissionRequiredMixin, AddOrEditView):
    permission_required = "messaging.add_contact"
    model = Contact
    form = ContactForm
    return_url = "messaging:relationship_list"
    template = "messaging/contact/add_edit.html"


class ContactEdit(PermissionRequiredMixin, AddOrEditView):
    permission_required = "messaging.change_contact"
    model = Contact
    form = ContactForm
    template = "messaging/contact/add_edit.html"


class ContactBulkEdit(PermissionRequiredMixin, BulkEditView):
    permission_required = "messaging.change_contact"
    queryset = Contact.objects.all()
    filter = ContactFilterSet
    table = ContactTable
    form = ContactBulkEditForm


class ContactDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "messaging.delete_contact"
    model = Contact
    return_url = "messaging:contact_list"


class ContactBulkDelete(PermissionRequiredMixin, BulkDeleteView):
    permission_required = "messaging.delete_contact"
    model = Contact
    filter = ContactFilterSet
    table = ContactTable


class ContactAssignmentEditView(PermissionRequiredMixin, AddOrEditView):
    permission_required = "messaging.edit_contactassignment"
    model = ContactAssignment
    form = ContactAssignmentForm
    template = "messaging/contactassignment/add_edit.html"

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            content_type = get_object_or_404(
                ContentType, pk=request.GET.get("content_type")
            )
            instance.object = get_object_or_404(
                content_type.model_class(), pk=request.GET.get("object_id")
            )
        return instance


class ContactAssignmentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "messaging.delete_contactassignment"
    model = ContactAssignment


class EmailList(PermissionRequiredMixin, ModelListView):
    permission_required = "messaging.view_email"
    queryset = Email.objects.all()
    filter = EmailFilterSet
    filter_form = EmailFilterForm
    table = EmailTable
    template = "messaging/email/list.html"


class EmailAdd(PermissionRequiredMixin, AddOrEditView):
    permission_required = "messaging.add_email"
    model = Email
    form = EmailForm
    template = "messaging/email/add_edit.html"
    return_url = "messaging:email_list"


class EmailDetails(DetailsView):
    permission_required = "messaging.view_email"
    queryset = Email.objects.all()

    def get_context(self, request, **kwargs):
        return {
            "instance": get_object_or_404(self.queryset, **kwargs),
            "active_tab": "main",
        }


class EmailEdit(PermissionRequiredMixin, AddOrEditView):
    permission_required = "messaging.change_email"
    model = Email
    form = EmailForm
    template = "messaging/email/add_edit.html"


class EmailDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "messaging.delete_email"
    model = Email
    return_url = "messaging:email_list"


class EmailBulkDelete(PermissionRequiredMixin, BulkDeleteView):
    permission_required = "messaging.delete_email"
    model = Email
    filter = EmailFilterSet
    table = EmailTable
