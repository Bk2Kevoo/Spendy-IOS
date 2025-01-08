from models.__init__ import SerializerMixin, validates, re, db
from config import flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column("password_hash", db.String(60), nullable=False)  
    created_at = db.Column(db.DateTime,  server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relationships
    budgeting = db.relationship("Budget", back_populates="user")
    savings = db.relationship("Saving", back_populates="user", cascade="all, delete-orphan") 

    # Serialize
    serialize_rules = ("-_password_hash", "-budgets", "-savings",)

    def __repr__(self):
        return f"""
            <User #{self.id}:
                Name: {self.name}
                Email: {self.email}>
        """

    @validates("name")
    def validate_name(self, _, value):
        if len(value) < 3:
            raise ValueError("name must be 3 characters long")
        return value
    
    @validates("email")
    def validate_email(self, _, email):
        if not re.match(
            r"^(?:(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*)|(?:'.+'))@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$",
            email,
        ):
            raise ValueError("email not valid")
        return email

    @hybrid_property
    def password(self):
        raise AttributeError("passwords are private, set-only")

    @password.setter
    def password(self, password_to_validate):
        if not isinstance(password_to_validate, str):
            raise TypeError("password must be a string")
        if not 7 < len(password_to_validate) < 20:
            raise ValueError(
                "password must be a string between 7 and 20 characters long"
            )
        hashed_password = flask_bcrypt.generate_password_hash(
            password_to_validate
        ).decode("utf-8")
        self._password_hash = hashed_password

    def auth(self, password_to_check):
        return flask_bcrypt.check_password_hash(self._password_hash, password_to_check)
