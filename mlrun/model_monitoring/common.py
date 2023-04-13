# Copyright 2018 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import enum
import hashlib
from dataclasses import dataclass
from typing import Optional

import mlrun.utils


class ModelMonitoringMode(str, enum.Enum):
    enabled = "enabled"
    disabled = "disabled"


class EndpointType(enum.IntEnum):
    NODE_EP = 1  # end point that is not a child of a router
    ROUTER = 2  # endpoint that is router
    LEAF_EP = 3  # end point that is a child of a router


def create_model_endpoint_uid(function_uri: str, versioned_model: str):
    function_uri = FunctionURI.from_string(function_uri)
    versioned_model = VersionedModel.from_string(versioned_model)

    if (
        not function_uri.project
        or not function_uri.function
        or not versioned_model.model
    ):
        raise ValueError("Both function_uri and versioned_model have to be initialized")

    uid = EndpointUID(
        function_uri.project,
        function_uri.function,
        function_uri.tag,
        function_uri.hash_key,
        versioned_model.model,
        versioned_model.version,
    )

    return uid


@dataclass
class FunctionURI:
    project: str
    function: str
    tag: Optional[str] = None
    hash_key: Optional[str] = None

    @classmethod
    def from_string(cls, function_uri):
        project, uri, tag, hash_key = mlrun.utils.parse_versioned_object_uri(
            function_uri
        )
        return cls(
            project=project,
            function=uri,
            tag=tag or None,
            hash_key=hash_key or None,
        )


@dataclass
class VersionedModel:
    model: str
    version: Optional[str]

    @classmethod
    def from_string(cls, model):
        try:
            model, version = model.split(":")
        except ValueError:
            model, version = model, None

        return cls(model, version)


@dataclass
class EndpointUID:
    project: str
    function: str
    function_tag: str
    function_hash_key: str
    model: str
    model_version: str
    uid: Optional[str] = None

    def __post_init__(self):
        function_ref = (
            f"{self.function}_{self.function_tag or self.function_hash_key or 'N/A'}"
        )
        versioned_model = f"{self.model}_{self.model_version or 'N/A'}"
        unique_string = f"{self.project}_{function_ref}_{versioned_model}"
        self.uid = hashlib.sha1(unique_string.encode("utf-8")).hexdigest()

    def __str__(self):
        return self.uid
