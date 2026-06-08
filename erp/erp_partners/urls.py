"""
BizSoft ERP - Partners Module

File:
    erp_partners/urls.py

Purpose:
    Defines partner API routes.

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


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from erp_partners.views import PartnerRelationshipViewSet, PartnerUsageValidationView, PartnerViewSet

router = DefaultRouter()
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'partner-relationships', PartnerRelationshipViewSet, basename='partner-relationship')


urlpatterns = [
    path('partners/validate-usage/', PartnerUsageValidationView.as_view(), name='partner-validate-usage'),
    path('', include(router.urls)),
]
