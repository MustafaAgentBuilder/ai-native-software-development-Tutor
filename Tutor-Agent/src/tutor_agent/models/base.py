# Claude is Work to Build this Project
"""
Shared database base for all models
"""

from sqlalchemy.ext.declarative import declarative_base

# Single Base instance shared across all models
Base = declarative_base()
