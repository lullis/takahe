from django import forms
from django.contrib.auth.password_validation import validate_password
from django.db import models, transaction
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView

from users.decorators import admin_required
from users.models import Domain, User
from users.services import IdentityService

from .domains import DomainValidator


@method_decorator(admin_required, name="dispatch")
class UsersRoot(ListView):
    template_name = "admin/users.html"
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get("query")
        self.extra_context = {
            "section": "users",
            "query": self.query or "",
        }
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        users = User.objects.annotate(
            num_identities=models.Count("identities")
        ).order_by("created")
        if self.query:
            users = users.filter(email__icontains=self.query)
        return users


@method_decorator(admin_required, name="dispatch")
class UserCreate(FormView):
    template_name = "admin/user_create.html"
    extra_context = {"section": "users"}

    class form_class(forms.Form):
        email_address = forms.EmailField()
        initial_password = forms.CharField(required=False, widget=forms.PasswordInput)
        username = forms.CharField(help_text="Your handle at the desired domain")
        identity_domain = forms.CharField(
            help_text="Identity domain, used by webfinger queries, Owned by the user",
            validators=[DomainValidator],
        )

        service_domain = forms.CharField(
            help_text="Service domain, will point to this takahe instance. Owned by the user",
            validators=[DomainValidator],
        )

        def clean_email_address(self):
            if User.objects.filter(email=self.cleaned_data["email_address"]).exists():
                raise forms.ValidationError("This user is already registered")
            return self.cleaned_data["email_address"]

        def clean_initial_password(self):
            password = self.cleaned_data["initial_password"]
            if password:
                validate_password(password)
            return password

        def clean_identity_domain(self):
            domain_name = self.cleaned_data["identity_domain"]
            if Domain.objects.filter(domain=domain_name).exists():
                raise forms.ValidationError("Domain name is already registered")

            return domain_name

        def clean_service_domain(self):
            domain_name = self.cleaned_data["service_domain"]
            if Domain.objects.filter(service_domain=domain_name).exists():
                raise forms.ValidationError("Domain name is already registered")

            return domain_name

    @transaction.atomic()
    def form_valid(self, form):
        user = User.objects.create_user(
            email=form.cleaned_data["email_address"],
            password=form.cleaned_data["initial_password"],
        )
        domain = Domain.objects.create(
            domain=form.cleaned_data["identity_domain"],
            service_domain=form.cleaned_data["service_domain"],
            public=False,
            default=False,
            local=True,
        )
        domain.users.add(user)
        username = form.cleaned_data["username"]
        IdentityService.create(
            user=user,
            username=username,
            domain=domain,
            name=username,
            discoverable=True,
        )
        return redirect(User.urls.admin)


@method_decorator(admin_required, name="dispatch")
class UserEdit(FormView):
    template_name = "admin/user_edit.html"
    extra_context = {
        "section": "users",
    }

    class form_class(forms.Form):
        status = forms.ChoiceField(
            choices=[
                ("normal", "Normal User"),
                ("moderator", "Moderator"),
                ("admin", "Admin"),
                ("banned", "Banned"),
            ]
        )

    def dispatch(self, request, id, *args, **kwargs):
        self.user = get_object_or_404(User, id=id)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        status = "normal"
        if self.user.moderator:
            status = "moderator"
        if self.user.admin:
            status = "admin"
        if self.user.banned:
            status = "banned"
        return {
            "email": self.user.email,
            "status": status,
        }

    def form_valid(self, form):
        # Don't let them change themselves
        if self.user == self.request.user:
            return redirect(".")
        status = form.cleaned_data["status"]
        self.user.banned = status == "banned"
        self.user.moderator = status == "moderator"
        self.user.admin = status == "admin"
        self.user.save()
        return redirect(self.user.urls.admin)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing_user"] = self.user
        context["same_user"] = self.user == self.request.user
        context["page"] = self.request.GET.get("page")
        return context
