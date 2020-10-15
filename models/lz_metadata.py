from config import db, ma

class LZMetadata(db.Model):
    __tablename__ = "lzmetadata"
    __table_args__ = {'schema': 'eagle_db'}
    key = db.Column(db.String(), primary_key=True)
    value = db.Column(db.String())

class LZMetadataSchema(ma.ModelSchema):
    class Meta:
        model = LZMetadata
        include_fk = True
        load_instance = True
