import datetime
from typing import List

from main import mongo


def save_changes_on_db(data: dict, msg: List[str] = None):
    """Save changes on database."""

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
    # add message field and insert by default
    data["msg"] = ""
    mongo.db.properties_checker.insert_one(data)
