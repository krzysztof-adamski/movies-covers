from marshmallow import Schema, fields


class OmdbMovieSchema(Schema):
    Title = fields.String(
        required=True,
        allow_none=False,
        attribute="title",
        error_messages={
            'required': 'Title is required'
        }
    )
    Year = fields.Integer(
        required=True,
        allow_none=False,
        attribute="year",
        error_messages={
            'required': 'Year is required'
        }
    )
    Plot = fields.String(
        required=True,
        allow_none=False,
        attribute="description",
        error_messages={
            'required': 'Url to poster is required'
        }
    )

    class Meta:
        strict = True
