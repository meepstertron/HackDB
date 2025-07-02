from datetime import datetime, timedelta
from app import db
from .models import Tokens, Usertables, Databases, Users,CreditsHistory

def checkToken(token: str) -> bool:
    """
    Check if the token is valid.
    """
    
    if not token.startswith('hkdb_tkn_'):
        return False
    
    if not db.session.query(Tokens).filter(Tokens.c.key == token).first():
        return False
    
    return True


def checkTable(table: str, token: str ) -> bool:
    """
    Check if a table name is valid for the token's user and database.
    """
    if not checkToken(token):
        return False
    if not table:
        return False
    
    # get token entry
    tokenentry = db.session.query(Tokens).filter(Tokens.c.key == token).first()
    if not tokenentry:
        return False
    dbid = tokenentry['dbid']
    userid = tokenentry['userid']

    # check that the database is owned by the user
    db_entry = db.session.query(Databases).filter(Databases.id == dbid, Databases.owner == userid).first()
    if not db_entry:
        return False

    # check that the table exists in usertables for this db
    table_entry = db.session.query(Usertables).filter(Usertables.db == dbid, Usertables.name == table).first()
    if not table_entry:
        return False

    return True

def tableToUUID(table: str, token: str) -> str:
    """
    Convert a table name to its UUID.
    """
    if not checkTable(table, token):
        return None
    
    # get token entry
    tokenentry = db.session.query(Tokens).filter(Tokens.c.key == token).first()
    if not tokenentry:
        return None
    dbid = tokenentry['dbid']

    # check that the table exists in usertables for this db
    table_entry = db.session.query(Usertables).filter(Usertables.db == dbid, Usertables.name == table).first()
    if not table_entry:
        return None

    return str(table_entry.id)


def whereObjectParser(where: dict):
    """
     Parse a where object into a WHERE thingie for sql 
    """
    if not where:
        return None
    
    sql_where = "WHERE "
    
    where_list = []
    
    for column, operation in where.items():
        
        if isinstance(operation, dict):
            for operation, value in operation.items():
                if operation == 'equals':
                    if value is None:
                        where_list.append(f"{column} IS NULL")
                    else:
                        where_list.append(f"{column} = {_convert_to_sql_type(value)}")
                if operation == 'gt':
                    where_list.append(f"{column} > {_convert_to_sql_type(value)}")
                if operation in ['gte', 'ge', 'greaterthanequal']:
                    where_list.append(f"{column} >= {_convert_to_sql_type(value)}")
                if operation == 'lt':
                    where_list.append(f"{column} < {_convert_to_sql_type(value)}")
                if operation in ['lte', 'le', 'lessthanequal']:
                    where_list.append(f"{column} <= {_convert_to_sql_type(value)}")
                if operation == 'contains':
                    where_list.append(f"{column} LIKE '%{value}%'")
                if operation == 'startswith':
                    where_list.append(f"{column} LIKE '{value}%'")
                if operation == 'endswith':
                    where_list.append(f"{column} LIKE '%{value}'")


        else:
            where_list.remove(f"{column} ")
            raise ValueError(f"Invalid operation for column {column}: {operation}")
    sql_where += " AND ".join(where_list)

    return sql_where



def _convert_to_sql_type(value):
    """
    Convert a Python value to a SQL type.
    """
    if isinstance(value, str):
        return f"'{value}'"
    elif isinstance(value, (int, float)):
        return str(value)
    elif value is None:
        return "NULL"
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")
    
    
    
class Credits:
    """
    A class to handle credit operations.
    """
    
    @staticmethod
    def get_credits(token: str) -> int:
        """
        Get the number of credits for a token.
        """
        if not checkToken(token):
            return 0
        
        token_entry = db.session.query(Tokens).filter(Tokens.c.key == token).first()
        user = db.session.query(Users).filter(Users.id == token_entry['userid']).first()
        if not user:
            return 0
        if user.quota is None:
            user.quota = 0
            db.session.commit()

        return user.quota
    
    
    @staticmethod
    def log_credits(user_id, action, credits_spent):
        history = CreditsHistory(
            user_id=user_id,
            action=action,
            credits_spent=credits_spent
        )
        
        
        user = db.session.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        user.quota -= credits_spent
        if user.quota < 0:
            user.quota = 0
            raise ValueError("Insufficient credits")
            
        db.session.add(history)
        db.session.commit()
        
    @staticmethod
    def charge_credits(user_id, credits_needed, action=""):
        user = db.session.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Unlimited users never get charged
        if getattr(user, "unlimited", False):
            history = CreditsHistory(
                user_id=user_id,
                action=action or "unlimited",
                credits_spent=0
            )
            db.session.add(history)
            db.session.commit()
            return

        # Calculate how much of the weekly allowance is left
        used_this_week = Credits.get_used_credits_this_week(user_id)
        weekly_left = max(user.weekly_allowance - used_this_week, 0)
        purchased_left = user.purchased_credits or 0

        # Check if enough credits
        total_available = weekly_left + purchased_left
        if credits_needed > total_available:
            raise ValueError("Insufficient credits")

        # Deduct from weekly allowance first, then purchased
        from_weekly = min(credits_needed, weekly_left)
        from_purchased = credits_needed - from_weekly

        # Update purchased_credits if needed
        if from_purchased > 0:
            user.purchased_credits -= from_purchased

        # Log the charge
        history = CreditsHistory(
            user_id=user_id,
            action=action,
            credits_spent=credits_needed
        )
        db.session.add(history)
        db.session.commit()
        
    def get_credits_change(weeks=1):
        """
        Get the change in credits over the last few weeks. in percentage.
        """
        if weeks < 1:
            raise ValueError("Weeks must be at least 1")
        
        # Get the current week
        current_week = db.session.query(CreditsHistory).filter(CreditsHistory.created_at >= db.func.date_trunc('week', db.func.now())).all()
        
        # Get the previous weeks
        previous_weeks = db.session.query(CreditsHistory).filter(CreditsHistory.created_at < db.func.date_trunc('week', db.func.now())).order_by(CreditsHistory.created_at.desc()).limit(weeks).all()
        
        current_credits = sum(entry.credits_spent for entry in current_week)
        previous_credits = sum(entry.credits_spent for entry in previous_weeks)



        return (current_credits - previous_credits) / previous_credits * 100
    
    
    @staticmethod
    def get_used_credits_this_week(user_id):
        now = datetime.utcnow()
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        used = db.session.query(db.func.sum(CreditsHistory.credits_spent)).filter(
            CreditsHistory.user_id == user_id,
            CreditsHistory.created_at >= start_of_week
        ).scalar()
        return used or 0

    @staticmethod
    def get_used_credits_last_week(user_id):
        now = datetime.utcnow()
        
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        start_of_last_week = start_of_week - timedelta(days=7)
        used = db.session.query(db.func.sum(CreditsHistory.credits_spent)).filter(
            CreditsHistory.user_id == user_id,
            CreditsHistory.created_at >= start_of_last_week,
            CreditsHistory.created_at < start_of_week
        ).scalar()
        return used or 0

    @staticmethod
    def get_change_percent(user_id):
        this_week = Credits.get_used_credits_this_week(user_id)
        last_week = Credits.get_used_credits_last_week(user_id)
        if last_week == 0:
            return 0
        return ((this_week - last_week) / last_week) * 100

    @staticmethod
    def get_history(user_id, limit=10):
        history = db.session.query(CreditsHistory).filter(
            CreditsHistory.user_id == user_id
        ).order_by(CreditsHistory.created_at.desc()).limit(limit).all()
        return [
            {
                "action": h.action,
                "credits_spent": h.credits_spent,
                "created_at": h.created_at.isoformat()
            } for h in history
        ]
        
    @staticmethod
    def get_weekly_usage(user_id, weeks=1):
        """
        Get the usage per week for a set amount of weeks, including all Mondays and today's usage.
        """
        if weeks < 1:
            raise ValueError("Weeks must be at least 1")
        
        now = datetime.utcnow()
        start_date = now - timedelta(weeks=weeks)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)


        mondays = []
        current_date = start_date
        while current_date <= now:
            if current_date.weekday() == 0:  
                mondays.append(current_date)
            current_date += timedelta(days=1)


        usage = db.session.query(
            db.func.date_trunc('week', CreditsHistory.created_at).label('week'),
            db.func.sum(CreditsHistory.credits_spent).label('total_spent')
        ).filter(
            CreditsHistory.user_id == user_id,
            CreditsHistory.created_at >= start_date
        ).group_by('week').order_by('week').all()

  
        usage_dict = {week.date(): total_spent for week, total_spent in usage}
        result = []
        for monday in mondays:
            monday_date = monday.date()
            result.append({
                "date": monday_date.isoformat(),
                "usage": usage_dict.get(monday_date, 0) 
            })

        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_usage = db.session.query(
            db.func.sum(CreditsHistory.credits_spent).label('total_spent')
        ).filter(
            CreditsHistory.user_id == user_id,
            CreditsHistory.created_at >= start_of_today
        ).scalar() or 0

        result[-1]['date'] = "This week"

        return result