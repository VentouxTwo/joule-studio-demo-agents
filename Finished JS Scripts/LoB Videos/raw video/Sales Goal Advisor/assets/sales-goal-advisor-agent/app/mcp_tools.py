"""
MCP tool indirection layer.

This module is the single place that loads tools from the SAP Agent Gateway.
Tests monkey-patch `get_mcp_tools` here (not in sap_cloud_sdk) so agent code
is completely identical in production and offline test runs.
"""
from mcp_providers.agw import get_mcp_tools  # re-export


__all__ = ["get_mcp_tools"]
