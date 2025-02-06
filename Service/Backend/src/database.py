# =====================================================================================================================
#                   Import
# =====================================================================================================================
import os
import re
import motor.motor_asyncio
from log import CustomLog
from dataclasses import dataclass, field
from bson.objectid import ObjectId
from enum import Enum


# =====================================================================================================================
#                   Enumeration
# =====================================================================================================================
class DBError(Enum):
    NONE = 0
    CREATE_UNKNOWN = 10
    CREATE_DUPLICATE = 11
    UPDATE_UNKNOWN = 20
    UPDATE_NOT_FOUND = 21
    UPDATE_NOTHING = 22


# =====================================================================================================================
#                   Database Aggregation
# =====================================================================================================================
@dataclass
class CustomCollection:
    name: str
    collection: motor.motor_asyncio.AsyncIOMotorCollection = field(init=False, repr=False)


    def __post_init__(self):
        self.collection = eval(f"{self.name}_collection")


    async def create(self, data) -> tuple[dict, DBError]:
        try:
            result = await self.collection.insert_one(data.__dict__)

            new_data = await self.collection.find_one({ "_id": ObjectId(result.inserted_id) })

            return new_data, DBError.NONE

        except Exception as error:
            error_code = DBError.CREATE_UNKNOWN

            if hasattr(error, "code"):
                error_code = DBError.CREATE_DUPLICATE

            log.error(error_code)

            return {}, error_code


    async def update(self, id, methd, data) -> tuple[dict, DBError]:
        try:
            result = await self.collection.update_one({ "_id": ObjectId(id) }, { f"${methd}": data })
            if result.matched_count == 0:
                raise Exception(DBError.UPDATE_NOT_FOUND)
            elif result.modified_count <= 0:
                raise Exception(DBError.UPDATE_NOTHING)

            update_data = await self.collection.find_one({ "_id": ObjectId(result.upserted_id) })

            return update_data, DBError.NONE

        except Exception as error:
            error_code = DBError.UPDATE_UNKNOWN

            if isinstance(error.args[0], DBError):
                error_code = error.args[0]

            log.error(error_code)

            return {}, error_code


    async def delete_data(self):
        pass


    async def get_data(self):
        pass


    async def get_list_data(self, pipelines = [], page = 1, count = 0):
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

            data_result = result["data"]
            page_count = 1
            total_count = result["info"][0]["total_count"] if len(result["info"]) > 0 else 0
            if show_count > 0 and total_count > 0:
                page_count = ((total_count - 1) // show_count) + 1

            log.info(f"{self.name.capitalize()} Data: {data_result}")

            return {
                "data": data_result,
                "info": {
                    "pageCount": page_count,
                }
            }

        except Exception as error:
            log.error(error)


@dataclass
class QueryPipeline:
    data: dict = field(default_factory=lambda: {})
    equl: list[str] = field(default_factory=lambda: [])
    regex: list[str] = field(default_factory=lambda: [])
    custom: dict = field(default_factory=lambda: {})


    @property
    def pipeline(self):
        rules = {}

        if len(self.data) > 0:
            for field in self.equl:
                if self.data.get(field):
                    rules[field] = {
                        "$eq": self.data[field]
                    }

            for field in self.regex:
                if self.data.get(field):
                    rules[field] = {
                        "$regex": re.compile(self.data[field])
                    }

        return {
            "$match": {
                **rules,
                **self.custom
            }
        }


@dataclass
class LookupPipeline:
    name: str
    key: str
    pipelines: list[dict] = field(default_factory=lambda: [])


    @property
    def pipeline(self):
        return {
            "$lookup": {
                "from": self.name,
                "let": {
                    self.key: f"${self.key}"
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
                                "$eq": ["$id", f"$${self.key}"]
                            }
                        }
                    },
                    *self.pipelines
                ],
                "as": self.name
            }
        }


@dataclass
class OutputPipeline:
    fields: list[str] = field(default_factory=lambda: [])
    custom: dict = field(default_factory=lambda: {})


    @property
    def pipeline(self):
        return {
            "$project": {
                "id": True,
                **dict(map(lambda x: [x, True], self.fields)),
                **self.custom
            }
        }


class DatabaseAggregation:
    def __init__(self):
        self.data_pipelines = []
        self.info_pipelines = []
        self.count_pre_page = 0
        self.lookup_fields = {}


    @property
    def pipelines(self):
        return self.data_pipelines


    def add_match_pipeline(self, obj: dict):
        match_pipeline = {
            "$match": {}
        }

        for field, rule in obj.items():
            if rule == None:
                continue

            match_pipeline["$match"][field] = rule

        self.data_pipelines.append(match_pipeline)
        self.info_pipelines.append(match_pipeline)


    def add_lookup_pipeline(self, collection: str, key: str, pipelines: list = []):
        lookup_pipeline = {
            "$lookup": {
                "from": collection,
                "let": {
                    "game_id": f"${key}"
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
                                "$eq": ["$id", f"$${key}"]
                            }
                        }
                    },
                    *pipelines
                ],
                "as": collection
            }
        }

        self.data_pipelines.append(lookup_pipeline)
        self.lookup_fields[collection] = True


    def add_project_pipeline(self, obj):
        self.data_pipelines.append({
            "$project": {
                "id": True,
                **self.lookup_fields,
                **obj
            }
        })


    def add_pagination_pipeline(self, page = 1, count_pre_page = 0):
        if page and count_pre_page:
            page = int(page)
            count_pre_page = int(count_pre_page)

            self.data_pipelines.append({
                "$skip": (page - 1) * count_pre_page
            })
            self.data_pipelines.append({
                "$limit": count_pre_page
            })
            self.count_pre_page = count_pre_page


    async def get_json_data(self, collection_name: str):
        try:
            tidy_data_pipelinse = list(filter(lambda x: list(x.values())[0], self.data_pipelines))
            tidy_info_pipelinse = list(filter(lambda x: list(x.values())[0], self.info_pipelines))

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
                        "data": [
                            *tidy_data_pipelinse,

                        ],
                        "info": [
                            *tidy_info_pipelinse,
                            {
                                "$count": "total_count"
                            }
                        ]
                    }
                }
            ]

            collection = eval(f"{collection_name}_collection")
            aggregation_result = await collection.aggregate(pagination_pipelines).to_list(length=None)
            result = aggregation_result[0]

            data_result = result["data"]
            page_count = 1
            total_count = result["info"][0]["total_count"] if len(result["info"]) > 0 else 0
            if self.count_pre_page > 0 and total_count > 0:
                page_count = ((total_count - 1) // self.count_pre_page) + 1

            log.info(f"{collection_name.capitalize()} Data: {data_result}")
            return {
                "data": data_result,
                "info": {
                    "pageCount": page_count,
                }
            }
        except Exception as error:
            log.error(error)


# =====================================================================================================================
#                   Declare Variable
# =====================================================================================================================
ENV_MONGO_USERNAME = os.environ["MONGO_USERNAME"]
ENV_MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
MONGO_DB_URL = f"mongodb://{ENV_MONGO_USERNAME}:{ENV_MONGO_PASSWORD}@mongo:27017/"

# Database Log 建立
log = CustomLog("database")

# Database Select
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
database = client.crm

# Collection List
settings_collection = database.get_collection("settings")
users_collection = database.get_collection("users")
games_collection = database.get_collection("games")
members_collection = database.get_collection("members")
properties_collection = database.get_collection("properties")
stocks_collection = database.get_collection("stocks")
trades_collection = database.get_collection("trades")
matches_collection = database.get_collection("matchs")
coupons_collection = database.get_collection("coupons")
