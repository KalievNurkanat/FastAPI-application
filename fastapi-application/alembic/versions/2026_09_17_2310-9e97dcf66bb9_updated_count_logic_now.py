"""updated count logic now

Revision ID: 9e97dcf66bb9
Revises: 291daca1e56a
Create Date: 2026-09-17 23:10:59.294454

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9e97dcf66bb9"
down_revision: Union[str, Sequence[str], None] = "291daca1e56a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint('count', 'order_product_association', type_='check')
    
    op.create_check_constraint(
        'count',
        'order_product_association',
        'count <= 20 AND count > 0'
    )

def downgrade():
    op.drop_constraint('count', 'order_product_association', type_='check')
    op.create_check_constraint(
        'count',
        'order_product_association',
        'count <= 20' 
    )
