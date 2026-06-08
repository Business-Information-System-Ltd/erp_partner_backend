"""
BizSoft ERP - Partners Module

File:
    erp_partners/services/partner_service.py

Purpose:
    Provides transaction-safe partner application service methods.

Architectural Notes:
    - This module manages common Business Partner / Stakeholder master data.
    - Customer, Supplier, Employee, FAR, Finance, and other module-specific profiles
      must be implemented in their respective modules.
    - This module should remain a core shared service with minimum external dependency.

Author:
    BizSoft Systems

Created:
    2026-06-04
"""


from django.db import transaction
from rest_framework.exceptions import NotFound

from erp_partners.enums.partner_enums import PartnerStatus
from erp_partners.models import PartnerAddress, PartnerContact, PartnerIdentification, PartnerRegistration, PartnerRole
from erp_partners.repositories.partner_repository import PartnerRepository
from erp_partners.serializers import (
    PartnerAddressSerializer,
    PartnerContactSerializer,
    PartnerIdentificationSerializer,
    PartnerRegistrationSerializer,
    PartnerRoleSerializer,
    PartnerSerializer,
)


class PartnerService:
    repository = PartnerRepository()

    @classmethod
    @transaction.atomic
    def create_partner(cls, data, created_by=None):
        """Create a partner after serializer validation."""
        serializer = PartnerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        payload = dict(serializer.validated_data)
        payload['created_by'] = created_by
        return cls.repository.create(payload)

    @classmethod
    @transaction.atomic
    def update_partner(cls, partner_id, data, updated_by=None):
        """Update a partner after serializer validation."""
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        serializer = PartnerSerializer(partner, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        payload = dict(serializer.validated_data)
        payload['updated_by'] = updated_by
        return cls.repository.update(partner, payload)

    @classmethod
    @transaction.atomic
    def activate_partner(cls, partner_id, updated_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        partner.status = PartnerStatus.ACTIVE
        partner.is_active = True
        partner.updated_by = updated_by
        partner.save(update_fields=['status', 'is_active', 'updated_by', 'updated_at'])
        return partner

    @classmethod
    @transaction.atomic
    def block_partner(cls, partner_id, reason=None, updated_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        partner.status = PartnerStatus.BLOCKED
        partner.updated_by = updated_by
        if reason:
            partner.remarks = reason
        partner.save(update_fields=['status', 'updated_by', 'remarks', 'updated_at'])
        return partner

    @classmethod
    @transaction.atomic
    def add_role(cls, partner_id, role_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        payload = {**role_data, 'partner': partner.id, 'created_by': created_by}
        serializer = PartnerRoleSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return PartnerRole.objects.create(**serializer.validated_data)

    @classmethod
    @transaction.atomic
    def add_address(cls, partner_id, address_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        payload = {**address_data, 'partner': partner.id, 'created_by': created_by}
        serializer = PartnerAddressSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return PartnerAddress.objects.create(**serializer.validated_data)

    @classmethod
    @transaction.atomic
    def add_contact(cls, partner_id, contact_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        payload = {**contact_data, 'partner': partner.id, 'created_by': created_by}
        serializer = PartnerContactSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return PartnerContact.objects.create(**serializer.validated_data)

    @classmethod
    @transaction.atomic
    def add_identification(cls, partner_id, identification_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        payload = {**identification_data, 'partner': partner.id, 'created_by': created_by}
        serializer = PartnerIdentificationSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return PartnerIdentification.objects.create(**serializer.validated_data)

    @classmethod
    @transaction.atomic
    def add_registration(cls, partner_id, registration_data, created_by=None):
        partner = cls.repository.get_by_id(partner_id)
        if not partner:
            raise NotFound('Partner not found.')
        payload = {**registration_data, 'partner': partner.id, 'created_by': created_by}
        serializer = PartnerRegistrationSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return PartnerRegistration.objects.create(**serializer.validated_data)
