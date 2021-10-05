"""initial Migration

Revision ID: fbc4b88b3cb9
Revises: 
Create Date: 2021-10-05 11:42:21.825006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc4b88b3cb9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invalid_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=24), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('pwd', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.drop_index('IFK_CustomerSupportRepId', table_name='customers')
    op.drop_table('customers')
    op.drop_table('playlists')
    op.drop_index('IFK_InvoiceCustomerId', table_name='invoices')
    op.drop_table('invoices')
    op.drop_table('sqlite_sequence')
    op.drop_table('sqlite_stat1')
    op.drop_index('IFK_InvoiceLineInvoiceId', table_name='invoice_items')
    op.drop_index('IFK_InvoiceLineTrackId', table_name='invoice_items')
    op.drop_table('invoice_items')
    op.drop_index('IFK_EmployeeReportsTo', table_name='employees')
    op.drop_table('employees')
    op.drop_index('IFK_PlaylistTrackTrackId', table_name='playlist_track')
    op.drop_table('playlist_track')
    op.add_column('albums', sa.Column('Name', sa.String(length=120), nullable=True))
    op.alter_column('albums', 'ArtistId',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index('IFK_AlbumArtistId', table_name='albums')
    op.drop_column('albums', 'Title')
    op.alter_column('tracks', 'Name',
               existing_type=sa.NVARCHAR(length=200),
               nullable=True)
    op.alter_column('tracks', 'MediaTypeId',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('tracks', 'Milliseconds',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('tracks', 'UnitPrice',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=True)
    op.drop_index('IFK_TrackAlbumId', table_name='tracks')
    op.drop_index('IFK_TrackGenreId', table_name='tracks')
    op.drop_index('IFK_TrackMediaTypeId', table_name='tracks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('IFK_TrackMediaTypeId', 'tracks', ['MediaTypeId'], unique=False)
    op.create_index('IFK_TrackGenreId', 'tracks', ['GenreId'], unique=False)
    op.create_index('IFK_TrackAlbumId', 'tracks', ['AlbumId'], unique=False)
    op.alter_column('tracks', 'UnitPrice',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=False)
    op.alter_column('tracks', 'Milliseconds',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('tracks', 'MediaTypeId',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('tracks', 'Name',
               existing_type=sa.NVARCHAR(length=200),
               nullable=False)
    op.add_column('albums', sa.Column('Title', sa.NVARCHAR(length=160), nullable=False))
    op.create_index('IFK_AlbumArtistId', 'albums', ['ArtistId'], unique=False)
    op.alter_column('albums', 'ArtistId',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('albums', 'Name')
    op.create_table('playlist_track',
    sa.Column('PlaylistId', sa.INTEGER(), nullable=False),
    sa.Column('TrackId', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['PlaylistId'], ['playlists.PlaylistId'], ),
    sa.ForeignKeyConstraint(['TrackId'], ['tracks.TrackId'], ),
    sa.PrimaryKeyConstraint('PlaylistId', 'TrackId')
    )
    op.create_index('IFK_PlaylistTrackTrackId', 'playlist_track', ['TrackId'], unique=False)
    op.create_table('employees',
    sa.Column('EmployeeId', sa.INTEGER(), nullable=False),
    sa.Column('LastName', sa.NVARCHAR(length=20), nullable=False),
    sa.Column('FirstName', sa.NVARCHAR(length=20), nullable=False),
    sa.Column('Title', sa.NVARCHAR(length=30), nullable=True),
    sa.Column('ReportsTo', sa.INTEGER(), nullable=True),
    sa.Column('BirthDate', sa.DATETIME(), nullable=True),
    sa.Column('HireDate', sa.DATETIME(), nullable=True),
    sa.Column('Address', sa.NVARCHAR(length=70), nullable=True),
    sa.Column('City', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('State', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('Country', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('PostalCode', sa.NVARCHAR(length=10), nullable=True),
    sa.Column('Phone', sa.NVARCHAR(length=24), nullable=True),
    sa.Column('Fax', sa.NVARCHAR(length=24), nullable=True),
    sa.Column('Email', sa.NVARCHAR(length=60), nullable=True),
    sa.ForeignKeyConstraint(['ReportsTo'], ['employees.EmployeeId'], ),
    sa.PrimaryKeyConstraint('EmployeeId')
    )
    op.create_index('IFK_EmployeeReportsTo', 'employees', ['ReportsTo'], unique=False)
    op.create_table('invoice_items',
    sa.Column('InvoiceLineId', sa.INTEGER(), nullable=False),
    sa.Column('InvoiceId', sa.INTEGER(), nullable=False),
    sa.Column('TrackId', sa.INTEGER(), nullable=False),
    sa.Column('UnitPrice', sa.NUMERIC(precision=10, scale=2), nullable=False),
    sa.Column('Quantity', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['InvoiceId'], ['invoices.InvoiceId'], ),
    sa.ForeignKeyConstraint(['TrackId'], ['tracks.TrackId'], ),
    sa.PrimaryKeyConstraint('InvoiceLineId')
    )
    op.create_index('IFK_InvoiceLineTrackId', 'invoice_items', ['TrackId'], unique=False)
    op.create_index('IFK_InvoiceLineInvoiceId', 'invoice_items', ['InvoiceId'], unique=False)
    op.create_table('sqlite_stat1',
    sa.Column('tbl', sa.NullType(), nullable=True),
    sa.Column('idx', sa.NullType(), nullable=True),
    sa.Column('stat', sa.NullType(), nullable=True)
    )
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    op.create_table('invoices',
    sa.Column('InvoiceId', sa.INTEGER(), nullable=False),
    sa.Column('CustomerId', sa.INTEGER(), nullable=False),
    sa.Column('InvoiceDate', sa.DATETIME(), nullable=False),
    sa.Column('BillingAddress', sa.NVARCHAR(length=70), nullable=True),
    sa.Column('BillingCity', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('BillingState', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('BillingCountry', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('BillingPostalCode', sa.NVARCHAR(length=10), nullable=True),
    sa.Column('Total', sa.NUMERIC(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['CustomerId'], ['customers.CustomerId'], ),
    sa.PrimaryKeyConstraint('InvoiceId')
    )
    op.create_index('IFK_InvoiceCustomerId', 'invoices', ['CustomerId'], unique=False)
    op.create_table('playlists',
    sa.Column('PlaylistId', sa.INTEGER(), nullable=False),
    sa.Column('Name', sa.NVARCHAR(length=120), nullable=True),
    sa.PrimaryKeyConstraint('PlaylistId')
    )
    op.create_table('customers',
    sa.Column('CustomerId', sa.INTEGER(), nullable=False),
    sa.Column('FirstName', sa.NVARCHAR(length=40), nullable=False),
    sa.Column('LastName', sa.NVARCHAR(length=20), nullable=False),
    sa.Column('Company', sa.NVARCHAR(length=80), nullable=True),
    sa.Column('Address', sa.NVARCHAR(length=70), nullable=True),
    sa.Column('City', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('State', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('Country', sa.NVARCHAR(length=40), nullable=True),
    sa.Column('PostalCode', sa.NVARCHAR(length=10), nullable=True),
    sa.Column('Phone', sa.NVARCHAR(length=24), nullable=True),
    sa.Column('Fax', sa.NVARCHAR(length=24), nullable=True),
    sa.Column('Email', sa.NVARCHAR(length=60), nullable=False),
    sa.Column('SupportRepId', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['SupportRepId'], ['employees.EmployeeId'], ),
    sa.PrimaryKeyConstraint('CustomerId')
    )
    op.create_index('IFK_CustomerSupportRepId', 'customers', ['SupportRepId'], unique=False)
    op.drop_table('users')
    op.drop_table('invalid_tokens')
    # ### end Alembic commands ###