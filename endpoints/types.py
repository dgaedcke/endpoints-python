# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provide various utility/container types needed by Endpoints Framework.

Putting them in this file makes it easier to avoid circular imports,
as well as keep from complicating tests due to importing code that
uses App Engine apis.
"""

from __future__ import absolute_import

# import attr

__all__ = [
    'OAuth2Scope', 'Issuer', 'LimitDefinition', 'Namespace',
]


# @attr.s(frozen=True, slots=True)
class OAuth2Scope(object):
    # scope = attr.ib(validator=attr.validators.instance_of(basestring))
    # description = attr.ib(validator=attr.validators.instance_of(basestring))

    def __init__(self, scope, description, **kwargs):
        s = kwargs.get("scope", scope)
        d = kwargs.get("description", description)
        assert isinstance(s, basestring), "invalid type"
        assert isinstance(d, basestring), "invalid type"
        self.scope = s
        self.description = d

        # fix me for immutable
        self.__setattr__ = self.setLate__setattr__


    def __eq__(self, other):
        if type(other) is type(self):
            return self.scope == other.scope
        else:
            return False

    def __str__(self):
        return "OAuth2Scope: s:{0} d:{1}".format(self.scope, self.description)

    def __repr__(self):
        return str(self)

    def setLate__setattr__(self):
        raise Exception.message("instance is immutable")

    def __getstate__(self):
        # being pickled; required to support pickling;
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def __setstate__(self, d):
        # being hydrated
        for slot in d:
            setattr(self, slot, d[slot])

    @property
    def __key(self):
        return self.scope      #, self.description)

    def __hash__(self):
        return hash(self.__key)


    @classmethod
    def convert_scope(cls, scope):
        "Convert string scopes into OAuth2Scope objects."
        if isinstance(scope, cls):
            return scope
        return cls(scope=scope, description=scope)

    @classmethod
    def convert_list(cls, values):
        "Convert a list of scopes into a list of OAuth2Scope objects."
        if values is not None:
            return [cls.convert_scope(value) for value in values]


# Issuer = attr.make_class('Issuer', ['issuer', 'jwks_uri'])


class Issuer(object):

    def __init__(self, issuer, jwks_uri, **kwargs):
        s = kwargs.get("issuer", issuer)
        j = kwargs.get("jwks_uri", jwks_uri)
        self.issuer = s
        self.jwks_uri = j

    def __str__(self):
        return "Issuer: s:{0} d:{1}".format(self.issuer, self.jwks_uri)

    def __repr__(self):
        return str(self)



# LimitDefinition = attr.make_class('LimitDefinition', ['metric_name',
#                                                       'display_name',
#                                                       'default_limit'])

class LimitDefinition(object):

    def __init__(self, metric_name, display_name, default_limit, **kwargs):
        m = kwargs.get("metric_name", metric_name)
        dn = kwargs.get("display_name", display_name)
        dl = kwargs.get("default_limit", default_limit)

        self.metric_name = m
        self.display_name = dn
        self.default_limit = dl

    def __str__(self):
        return "LimitDefinition: mn:{0} dn:{1}   dl:{2}".format(self.metric_name, self.display_name, self.default_limit)

    def __repr__(self):
        return str(self)


# Namespace = attr.make_class('Namespace', ['owner_domain', 'owner_name', 'package_path'])

class Namespace(object):

    def __init__(self, owner_domain, owner_name, package_path, **kwargs):
        m = kwargs.get("owner_domain", owner_domain)
        dn = kwargs.get("owner_name", owner_name)
        dl = kwargs.get("package_path", package_path)

        self.owner_domain = m
        self.owner_name = dn
        self.package_path = dl

    def __str__(self):
        return "Namespace: od:{0}   on:{1}   pp:{2}".format(self.owner_domain, self.owner_name, self.package_path)

    def __repr__(self):
        return str(self)