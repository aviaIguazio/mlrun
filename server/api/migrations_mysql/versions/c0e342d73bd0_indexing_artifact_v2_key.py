# Copyright 2023 Iguazio
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
"""indexing artifact_v2 key

Revision ID: c0e342d73bd0
Revises: b268044fa2f7
Create Date: 2024-02-07 14:46:55.639228

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "c0e342d73bd0"
down_revision = "b268044fa2f7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("ix_artifacts_v2_key"), "artifacts_v2", ["key"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_artifacts_v2_key"), table_name="artifacts_v2")
    # ### end Alembic commands ###
