# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ
from typing import List, Self, Tuple, Dict, Any
from dataclasses import dataclass, field
from bson.objectid import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from log import LogFile
from error import HttpError, DBException
from schema import DataSchema


# =====================================================================================================================
#                   Class
# =====================================================================================================================
@dataclass
class BaseCollection:
    name: str
    collection: AsyncIOMotorCollection = field(init=False, repr=False)

    def __post_init__(self: Self):
        client = AsyncIOMotorClient(MONGO_DB_URL)
        database: AsyncIOMotorDatabase = client.crm
        self.collection = database.get_collection(self.name)

    async def create_data(self: Self, data: dict) -> dict:
        try:
            schema_data = DataSchema.set_schema_data(name=self.name, data=data)
            result = await self.collection.insert_one(schema_data)
            new_data = await self.collection.find_one({"_id": ObjectId(result.inserted_id)})
            log.info(f"{self.name.capitalize()} Create Data: {new_data}")

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

            log.info(f"{self.name.capitalize()} Delete Data: {old_data}")

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
    def match(*args: Tuple) -> dict:
        return {
            "$match": {
                "$expr": arg for arg in args if arg
            }
        }

    @staticmethod
    def filter(*args: Tuple) -> dict:
        return {
            "$filter": {
                "input": args[0],
                "as": "this",
                "cond": BaseCondition.equl("$$this", args[1])
            }
        }

    @staticmethod
    def map(input: str | dict, output: str | dict) -> dict:
        return {
            "$map": {
                "input": input,
                "as": "this",
                "in": output
            }
        }

    @staticmethod
    def add_fields(insert: dict={}, delete: list=[]) -> dict:
        return {
            "$addFields": {
                **{
                    key: value for key, value in insert.items()
                },
                **{
                    key: "$$REMOVE" for key in delete
                }
            }
        }

    @staticmethod
    def lookup(name: str, key: str, lets: dict={}, pipelines: List[dict]=[], conditions: List[dict]=[]) -> dict:
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
                                "$and": conditions if conditions else [
                                    {
                                        "$eq": ["$id", f"$${key}"]
                                    }
                                ]
                            }
                        }
                    },
                    *pipelines
                ],
                "as": name
            }
        }

    @staticmethod
    def project(name: str="", show: List[str]=[], hide: List[str]=[], custom: dict={}) -> dict:
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


class BaseCondition:
    @staticmethod
    def equl(field: Any, value: Any) -> dict:

        return {
            "$eq": [field, value]
        }

    @staticmethod
    def not_equl(field: Any, value: Any) -> dict:
        return {
            "$ne": [field, value]
        }

    @staticmethod
    def regex(field: Any, value: Any) -> dict:
        return {
            "$regexMatch": {
                "input": field,
                "regex": value
            }
        } if value is not None else {}

    @staticmethod
    def less_than(field: Any, value: Any, equl: bool=False) -> dict:
        return {
            f"$lt{"e" if equl else ""}": [field, value]
        }

    @staticmethod
    def greater_than(field: Any, value: Any, equl: bool=False) -> dict:
        return {
            f"$gt{"e" if equl else ""}": [field, value]
        }

    @staticmethod
    def if_then_else(if_expn: Any, then_expn: Any, else_expn: Any) -> Dict:
        return {
            "$cond": {
                "if": if_expn,
                "then": then_expn,
                "else": else_expn
            }
        }

    @staticmethod
    def and_expression(*args: Tuple) -> Dict:
        return {
            "$and": [
                arg for arg in args
            ]
        }

    @staticmethod
    def or_expression(*args: Tuple) -> Dict:
        return {
            "$or": [
                arg for arg in args
            ]
        }


class BaseCalculate:
    @staticmethod
    def sum(*args: Tuple) -> dict:
        return {
            "$sum": [
                arg for arg in args
            ]
        }

    @staticmethod
    def subtract(*args: Tuple) -> dict:
        return {
            "$subtract": [
                arg for arg in args
            ]
        }

    @staticmethod
    def multiply(*args: Tuple) -> dict:
        return {
            "$multiply": [
                arg for arg in args
            ]
        }

    @staticmethod
    def size(*args: Tuple) -> dict:
        return {
            "$size": args[0]
        }


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
ENV_MONGO_USERNAME = environ["MONGO_USERNAME"]
ENV_MONGO_PASSWORD = environ["MONGO_PASSWORD"]
MONGO_DB_URL = f"mongodb://{ENV_MONGO_USERNAME}:{ENV_MONGO_PASSWORD}@mongo:27017/"

# Log 建立
log = LogFile("database", enabled=False)
