#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"])) #false
print(a.require_auth("/api/v1/status", ["/api/v1/status/"])) #false
print(a.require_auth("/api/v1/statu", ["/api/v1/status/"])) #true
print(a.require_auth("/api/v1/stat", ["/api/v1/stat*"])) #false
print(a.require_auth("/api/v1/status", ["/api/v1/stat*"])) #false
