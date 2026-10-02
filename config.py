class Config:
    SECRET_KEY = "dev-secret-key-change-later"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://codeforge_user:codeforge_password@localhost:5432/codeforge"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

