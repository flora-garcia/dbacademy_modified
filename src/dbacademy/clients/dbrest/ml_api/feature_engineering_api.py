__all__ = ["FeatureEngineeringApi"]

from typing import List, Dict, Any
from dbacademy.clients.rest.common import ApiClient, ApiContainer


class FeatureEngineeringApi(ApiContainer):

    def __init__(self, client: ApiClient):
        from dbacademy.common import validate

        self.__client = validate(client=client).required.as_type(ApiClient)
        self.base_uri = f"{self.__client.endpoint}/api/2.1/unity-catalog"

    def search_tables(self, schema, catalog) -> List[Dict[str, Any]]:
        maxsize = 50
        results = []

        response = self.__client.api("GET", f"{self.base_uri}/tables/search?max_results={maxsize}&catalog_name={catalog}&schema_name={schema}")
        results.extend(response.get("tables", []))

        while "next_page_token" in response:
            next_page_token = response["next_page_token"]
            response = self.__client.api("GET", f"{self.base_uri}/tables/search?max_results={maxsize}&catalog_name={catalog}&schema_name={schema}&page_token={next_page_token}")
            results.extend(response.get("tables", []))

        return results
