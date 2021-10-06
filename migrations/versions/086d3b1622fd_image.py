"""image

Revision ID: 086d3b1622fd
Revises: 3812f6585c2c
Create Date: 2021-10-05 22:55:50.285556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '086d3b1622fd'
down_revision = '3812f6585c2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_image', sa.String(length=10000), nullable=True),
    sa.Column('ArtistId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ArtistId'], ['artists.ArtistId'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artist_images')
    # ### end Alembic commands ###
