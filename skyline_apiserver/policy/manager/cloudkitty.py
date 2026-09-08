# Copyright 2026 OpenStack Skyline Authors
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

# flake8: noqa
# fmt: off

# CloudKitty (the OpenStack "rating" service) policy rules.
#
# Rule names mirror the upstream CloudKitty policies so the UI permission
# hints line up with what the service actually enforces:
#   - cloudkitty/common/policies/v1/rating.py  (rating:*)
#   - cloudkitty/common/policies/v2/summary.py (summary:get_summary)
#
# Upstream gates every rating module / module_config operation on
# "role:admin", and the v2 summary on "project reader or admin". The project
# reader rule below also accepts "member" because many deployments grant
# users the member role without also granting reader, and a project user is
# expected to be able to see their own rating summary.

from . import base

PROJECT_READER = (
    "(role:reader or role:member or role:_member_) and project_id:%(project_id)s"
)
SYSTEM_READER = "role:reader and system_scope:all"
SYSTEM_ADMIN = "role:admin and system_scope:all"

list_rules = (
    base.Rule(
        name="cloudkitty_admin",
        check_str="role:admin",
        description="Administrators can manage CloudKitty rating configuration.",
    ),
    base.Rule(
        name="cloudkitty_project_reader",
        check_str=f"({PROJECT_READER})",
        description="Project readers and members can view their own rating data.",
    ),
    base.APIRule(
        name="rating:list_modules",
        check_str=f"rule:cloudkitty_admin or ({SYSTEM_ADMIN})",
        description="Return the list of loaded rating modules.",
        scope_types=["project", "system"],
        operations=[{"method": "GET", "path": "/v1/rating/modules"}],
    ),
    base.APIRule(
        name="rating:get_module",
        check_str=f"rule:cloudkitty_admin or ({SYSTEM_ADMIN})",
        description="Get the specified rating module.",
        scope_types=["project", "system"],
        operations=[{"method": "GET", "path": "/v1/rating/modules/{module_id}"}],
    ),
    base.APIRule(
        name="rating:update_module",
        check_str=f"rule:cloudkitty_admin or ({SYSTEM_ADMIN})",
        description="Change the state and priority of a rating module.",
        scope_types=["project", "system"],
        operations=[{"method": "PUT", "path": "/v1/rating/modules/{module_id}"}],
    ),
    base.APIRule(
        name="rating:module_config",
        check_str=f"rule:cloudkitty_admin or ({SYSTEM_ADMIN})",
        description=(
            "Manage rating module configuration. Covers the hashmap module "
            "(services, fields, mappings, groups, thresholds) and the "
            "pyscripts module, plus rating module list reloads."
        ),
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v1/rating/reload_modules"},
            {"method": "GET", "path": "/v1/rating/module_config/hashmap/types"},
            {"method": "POST", "path": "/v1/rating/module_config/hashmap/types"},
            {"method": "DELETE", "path": "/v1/rating/module_config/hashmap/types"},
            {"method": "GET", "path": "/v1/rating/module_config/hashmap/fields"},
            {"method": "POST", "path": "/v1/rating/module_config/hashmap/fields"},
            {"method": "DELETE", "path": "/v1/rating/module_config/hashmap/fields"},
            {"method": "GET", "path": "/v1/rating/module_config/hashmap/mappings"},
            {"method": "POST", "path": "/v1/rating/module_config/hashmap/mappings"},
            {"method": "PUT", "path": "/v1/rating/module_config/hashmap/mappings"},
            {"method": "DELETE", "path": "/v1/rating/module_config/hashmap/mappings"},
            {"method": "GET", "path": "/v1/rating/module_config/hashmap/groups"},
            {"method": "POST", "path": "/v1/rating/module_config/hashmap/groups"},
            {"method": "DELETE", "path": "/v1/rating/module_config/hashmap/groups"},
            {"method": "GET", "path": "/v1/rating/module_config/hashmap/thresholds"},
            {"method": "POST", "path": "/v1/rating/module_config/hashmap/thresholds"},
            {"method": "PUT", "path": "/v1/rating/module_config/hashmap/thresholds"},
            {"method": "DELETE", "path": "/v1/rating/module_config/hashmap/thresholds"},
            {"method": "GET", "path": "/v1/rating/module_config/pyscripts/scripts"},
            {"method": "POST", "path": "/v1/rating/module_config/pyscripts/scripts"},
            {"method": "PUT", "path": "/v1/rating/module_config/pyscripts/scripts"},
            {"method": "DELETE", "path": "/v1/rating/module_config/pyscripts/scripts"},
        ],
    ),
    base.APIRule(
        name="rating:quote",
        check_str="",
        description="Get an instant quote based on multiple resource descriptions.",
        scope_types=["project", "system"],
        operations=[{"method": "POST", "path": "/v1/rating/quote"}],
    ),
    base.APIRule(
        name="summary:get_summary",
        check_str=(
            f"rule:cloudkitty_project_reader or rule:cloudkitty_admin "
            f"or ({SYSTEM_READER}) or ({SYSTEM_ADMIN})"
        ),
        description="Get a rating summary.",
        scope_types=["project", "system"],
        operations=[{"method": "GET", "path": "/v2/summary"}],
    ),
    base.APIRule(
        name="info:get_config",
        check_str=f"rule:cloudkitty_project_reader or rule:cloudkitty_admin",
        description="Get the CloudKitty collector configuration (metrics, period).",
        scope_types=["project", "system"],
        operations=[{"method": "GET", "path": "/v1/info/config"}],
    ),
    base.APIRule(
        name="info:list_metrics_info",
        check_str=f"rule:cloudkitty_project_reader or rule:cloudkitty_admin",
        description="List the metrics known to CloudKitty and their units.",
        scope_types=["project", "system"],
        operations=[
            {"method": "GET", "path": "/v1/info/metrics"},
            {"method": "GET", "path": "/v1/info/metrics/{metric_name}"},
        ],
    ),
)

__all__ = ("list_rules",)
