import datetime
from typing import List

from celery import shared_task


@shared_task
def add_new_property(data: dict, msg: str = "") -> None:
    """Add new property to database."""
    # import locally
    from main import mongo

    # check if property already exists
    if mongo.db.properties_checker.find_one({"N° do imóvel": data["N° do imóvel"]}):
        return

    # add message field and insert
    data["msg"] += f"{msg}\n"
    mongo.db.properties_checker.insert_one(data)


def save_changes_on_db(data: dict, msg: List[str] = None) -> None:
    """Save on database."""
    # import locally
    from main import mongo

    # check if data already exists
    if mongo.db.properties_checker.find_one({"N° do imóvel": data["N° do imóvel"]}):
        print("Updating...")
        # update data
        mongo.db.properties_checker.update_one(
            {"N° do imóvel": data["N° do imóvel"]}, {"$set": data}
        )
        if msg:
            # try to get message field
            try:
                msgs_on_db = mongo.db.properties_checker.find_one(
                    {"N° do imóvel": data["N° do imóvel"]}, {"msg": 1}
                )["msg"]
            except KeyError:
                # create msg field on db
                mongo.db.properties_checker.update_one(
                    {"N° do imóvel": data["N° do imóvel"]}, {"$set": {"msg": ""}}
                )
                msgs_on_db = ""

            # add new messages
            for message in msg:
                msgs_on_db += f"{message}\n"

            # update message
            mongo.db.properties_checker.update_one(
                {"N° do imóvel": data["N° do imóvel"]},
                {"$set": {"msg": msgs_on_db}},
            )

        return

    print("Inserting...")
    # add property
    add_new_property.delay(data)


def get_all_properties() -> List[dict]:
    """Get all properties from database."""
    # import locally
    from main import mongo

    return list(mongo.db.properties_checker.find())
