"""
BizSoft ERP - Partners Module

File:
    erp_partners/views/partner_views.py

Purpose:
    Defines partner API ViewSet and child collection actions.

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


from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from erp_partners.models import Partner, PartnerAddress, PartnerContact, PartnerIdentification, PartnerRegistration, PartnerRole
from erp_partners.serializers import (
    PartnerAddressSerializer,
    PartnerContactSerializer,
    PartnerDetailSerializer,
    PartnerIdentificationSerializer,
    PartnerRegistrationSerializer,
    PartnerRoleSerializer,
    PartnerSerializer,
)
from erp_partners.services.partner_service import PartnerService


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by('partner_code')
    serializer_class = PartnerSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartnerDetailSerializer
        return PartnerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        partner_type = self.request.query_params.get('partner_type')
        role_type = self.request.query_params.get('role_type')
        status_value = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        if partner_type:
            qs = qs.filter(partner_type=partner_type)
        if role_type:
            qs = qs.filter(roles__role_type=role_type, roles__is_active=True).distinct()
        if status_value:
            qs = qs.filter(status=status_value)
        if search:
            qs = qs.filter(Q(partner_code__icontains=search) | Q(display_name__icontains=search) | Q(legal_name__icontains=search) | Q(short_name__icontains=search))
        return qs

    def create(self, request, *args, **kwargs):
        partner = PartnerService.create_partner(request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partner = PartnerService.update_partner(kwargs['pk'], request.data, updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    def partial_update(self, request, *args, **kwargs):
        partner = PartnerService.update_partner(kwargs['pk'], request.data, updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        partner = PartnerService.activate_partner(pk, updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        partner = PartnerService.block_partner(pk, reason=request.data.get('reason'), updated_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerSerializer(partner).data)

    @action(detail=True, methods=['get', 'post'])
    def roles(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerRoleSerializer(PartnerRole.objects.filter(partner_id=pk), many=True).data)
        role = PartnerService.add_role(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerRoleSerializer(role).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def addresses(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerAddressSerializer(PartnerAddress.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_address(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerAddressSerializer(obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def contacts(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerContactSerializer(PartnerContact.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_contact(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerContactSerializer(obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def identifications(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerIdentificationSerializer(PartnerIdentification.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_identification(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerIdentificationSerializer(obj).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'])
    def registrations(self, request, pk=None):
        if request.method == 'GET':
            return Response(PartnerRegistrationSerializer(PartnerRegistration.objects.filter(partner_id=pk), many=True).data)
        obj = PartnerService.add_registration(pk, request.data, created_by=str(request.user) if request.user.is_authenticated else None)
        return Response(PartnerRegistrationSerializer(obj).data, status=status.HTTP_201_CREATED)
