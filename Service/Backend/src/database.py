# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ
from re import compile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError
from dataclasses import dataclass, field
from typing import List, Self
from bson.objectid import ObjectId
from log import LogFile
from error import HttpError, DBException
from schema import DataSchema


# =====================================================================================================================
#                   Database Aggregation
# =====================================================================================================================
@dataclass
class BaseCollection:
    name: str
    collection: AsyncIOMotorCollection = field(init=False, repr=False)


    def __post_init__(self: Self):
        self.collection = eval(f"{self.name}_collection")


    async def create_data(self: Self, data: dict) -> dict:
        try:
            schema_data = DataSchema.set_schema_data(name=self.name, data=data)
            result = await self.collection.insert_one(schema_data)
            new_data = await self.collection.find_one({ "_id": ObjectId(result.inserted_id) })

            return new_data

        except DuplicateKeyError:
            log.error(f"{self.name.capitalize()} Create Data Duplicate Error")
            raise DBException(
                response=HttpError.Error_409_CONFLICT()
            )

        except Exception:
            log.error(f"{self.name.capitalize()} Create Data Unknown Error")
            raise DBException(
                response=HttpError.Error_500_Internal_Server_Error()
            )

    async def get_data(self: Self, pipelines: List[dict] = []) -> dict:
        try:
            aggregation_result = await self.collection.aggregate([
                {
                    "$addFields": {
                        "id": {
                            "$toString": "$_id"
                        },
                        "_id": "$$REMOVE"
                    }
                },
                *pipelines
            ]).to_list(length=None)

            show_data = aggregation_result[0] if aggregation_result else None
            log.info(f"{self.name.capitalize()} Read Data: {show_data}")

            return show_data

        except Exception:
            log.error(f"{self.name.capitalize()} Read Data Unknown Error")
            raise DBException(
                response=HttpError.Error_500_Internal_Server_Error()
            )


    async def update_data(self: Self, find: dict, data: dict, method: str="set") -> dict:
        try:
            search_info = {}
            if find.get("id"):
                id = find["id"]
                search_info["_id"] = ObjectId(id)
            else:
                search_info = find.copy()

            result = await self.collection.update_one(search_info, {f"${method}": data})
            if result.matched_count == 0:
                log.error(f"{self.name.capitalize()} Update Data Not Found Error")
                raise DBException(
                    response=HttpError.Error_404_NOT_FOUND()
                )
            elif result.modified_count == 0:
                log.error(f"{self.name.capitalize()} Update Data Nothing Error")
                raise DBException(
                    response=HttpError.Error_405_METHOD_NOT_ALLOWED()
                )

            update_data = await self.collection.find_one(search_info)
            log.info(f"{self.name.capitalize()} Update Data: {update_data}")

            return update_data

        except Exception as error:
            if isinstance(error, DBException):
                raise error
            else:
                print(error)
                log.error(f"{self.name.capitalize()} Update Data Unknown Error")
                raise DBException(
                    response=HttpError.Error_500_Internal_Server_Error()
                )


    async def delete_data(self: Self, find: dict) -> dict:
        try:
            search_info = {}
            if find.get("id"):
                id = find["id"]
                search_info["_id"] = ObjectId(id)
            else:
                search_info = find.copy()

            old_data = await self.collection.find_one(search_info)

            result = await self.collection.delete_one(search_info)
            if result.deleted_count == 0:
                log.error(f"{self.name.capitalize()} Delete Data Not Found Error")
                raise DBException(
                    response=HttpError.Error_404_NOT_FOUND()
                )

            return old_data

        except Exception as error:
            if isinstance(error, DBException):
                raise error
            else:
                log.error(f"{self.name.capitalize()} Delete Data Unknown Error")
                raise DBException(
                    response=HttpError.Error_500_Internal_Server_Error()
                )


    async def get_list_data(
        self: Self, pipelines: List[dict]=[], page: int=1, count: int=0, reverse: bool=False
    ) -> dict:
        try:
            data_pipelines: list[dict] = [*pipelines]
            match_pipeline: list[dict] = list(filter(lambda x: list(x.keys())[0] == "$match", [*pipelines]))
            current_page: int = int(page) if page else 1
            show_count: int = int(count) if count else 0

            if current_page > 1 and show_count > 0:
                data_pipelines.append({
                    "$skip": (current_page - 1) * show_count
                })

            if show_count > 0:
                data_pipelines.append({
                    "$limit": show_count
                })

            pagination_pipelines = [
                {
                    "$addFields": {
                        "id": {
                            "$toString": "$_id"
                        },
                        "_id": "$$REMOVE"
                    }
                },
                {
                    "$facet": {
                        "data": data_pipelines,
                        "info": [
                            *match_pipeline,
                            {
                                "$count": "total_count"
                            }
                        ]
                    }
                }
            ]

            aggregation_result = await self.collection.aggregate(pagination_pipelines).to_list(length=None)
            result = aggregation_result[0]

            list_data = result["data"]
            if reverse:
                list_data = list_data[::-1]

            page_count = 1
            total_count = result["info"][0]["total_count"] if len(result["info"]) > 0 else 0
            if show_count > 0 and total_count > 0:
                page_count = ((total_count - 1) // show_count) + 1

            log.info(f"{self.name.capitalize()} Read List Data: {list_data}")

            result_data = {
                "list_data": list_data,
                "page_count": page_count,
            }

            return result_data

        except Exception:
            log.error(f"{self.name.capitalize()} Read List Data Unknown Error")
            raise DBException(
                response=HttpError.Error_500_Internal_Server_Error()
            )


class BasePipeline:
    @staticmethod
    def create_match(
        equl: dict={}, fuzzy: dict={}, range: dict={}, gte: dict={}, lte: dict={}
    ) -> dict:
        return {
            "$match": {
                **{
                    key: {
                        "$eq": value
                    } for (key, value) in equl.items() if value is not None
                },
                **{
                    key: {
                        "$regex": compile(value)
                    } for (key, value) in fuzzy.items() if value is not None
                },
                **{
                    key: {
                        "$gte": value[0],
                        "$lt": value[1]
                    } for (key, value) in range.items() if value is not None
                },
                **{
                    key: {
                        "$gte": value,
                    } for (key, value) in gte.items() if value is not None
                },
                **{
                    key: {
                        "$lte": value,
                    } for (key, value) in lte.items() if value is not None
                }
            }
        }

    @staticmethod
    def create_project(
        name: str="", show: List[str]=[], hide: List[str]=[], custom: dict={}
    ) -> dict:
        default_fields = {}
        if name:
            default_fields = DataSchema.get_schema_fields(name=name)
            default_fields = [field for field in default_fields if field not in hide]

        return {
            "$project": {
                "id": True,
                **{
                    field_name: True for field_name in default_fields
                },
                **{
                    field_name: True for field_name in show
                },
                **{
                    key: value for (key, value) in custom.items()
                }
            }
        }

    @staticmethod
    def create_eq_condition(
        expression_1: str | int | dict, expression_2: str | int | dict
    ) -> dict:
        return {
            "$eq": [expression_1, expression_2]
        }

    @staticmethod
    def create_lte_condition(
        expression_1: str | int | dict, expression_2: str | int | dict
    ) -> dict:
        return {
            "$lte": [expression_1, expression_2]
        }

    @staticmethod
    def create_gte_condition(
        expression_1: str | int | dict, expression_2: str | int | dict
    ) -> dict:
        return {
            "$gte": [expression_1, expression_2]
        }

    @staticmethod
    def create_if_condition(
        if_expn: dict, then_expn: str | int | dict, else_expn: str | int | dict
    ) -> dict:
        return {
            "$cond": {
                "if": if_expn,
                "then": then_expn,
                "else": else_expn
            }
        }

    @staticmethod
    def create_and_condition(
        items: List[str | int | dict]
    ) -> dict:
        return {
            "$and": items
        }

    @staticmethod
    def create_sum(
        items: List[str | int | dict] = []
    ) -> dict:
        return {
            "$sum": items
        }


    @staticmethod
    def create_multiply(
        items: List[str | int | dict] = []
    ) -> dict:
        return {
            "$multiply": items
        }

    @staticmethod
    def create_size(
        item: str | int | dict
    ) -> dict:
        return {
            "$size": item
        }

    @staticmethod
    def create_filter(
        input: str | dict, value: str | int | bool
    ) -> dict:
        return {
            "$filter": {
                "input": input,
                "as": "field",
                "cond": {
                    "$eq": ["$$field", value]
                }
            }
        }

    @staticmethod
    def create_map(
        input: str | dict, docs: str, expn: str | dict
    ) -> dict:
        return {
            "$map": {
                "input": input,
                "as": docs,
                "in": expn
            }
        }

    @staticmethod
    def create_lookup(
        name: str, key: str, lets: dict={}, pipelines: List[dict]=[], match_conditions: List[dict]=[]
    ) -> dict:
        if not match_conditions:
            match_conditions = [
                {
                    "$eq": ["$id", f"$${key}"]
                }
            ]

        return {
            "$lookup": {
                "from": name,
                "let": {
                    key: f"${key}",
                    **lets
                },
                "pipeline": [
                    {
                        "$addFields": {
                            "id": {
                                "$toString": "$_id"
                            },
                            "_id": "$$REMOVE"
                        }
                    },
                    {
                        "$match": {
                            "$expr": {
                                "$and": match_conditions
                            }
                        }
                    },
                    *pipelines
                ],
                "as": name
            }
        }


# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
ENV_MONGO_USERNAME = environ["MONGO_USERNAME"]
ENV_MONGO_PASSWORD = environ["MONGO_PASSWORD"]
MONGO_DB_URL = f"mongodb://{ENV_MONGO_USERNAME}:{ENV_MONGO_PASSWORD}@mongo:27017/"

# Log 建立
log = LogFile("database")

# Database Select
client = AsyncIOMotorClient(MONGO_DB_URL)
database: AsyncIOMotorDatabase = client.crm

# Collection List
setting_collection = database.get_collection("setting")
user_collection = database.get_collection("user")
game_collection = database.get_collection("game")
member_collection = database.get_collection("member")
property_collection = database.get_collection("property")
stock_collection = database.get_collection("stock")
trade_collection = database.get_collection("trade")
match_collection = database.get_collection("match")
coupon_collection = database.get_collection("coupon")
