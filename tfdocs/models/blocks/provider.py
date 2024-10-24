import logging
from tfdocs.models.block import Block
from tfdocs.models.blocks.resource import Resource
from tfdocs.models.blocks.datasource import DataSource

log = logging.getLogger()


class Provider(Block):
    @classmethod
    def list_providers(cls) -> list["Provider"]:
        """
        Returns all providers in the cache as objects with prefetched names
        """
        res = cls._db.sql(
            """
            SELECT block_id, block_name FROM block 
            WHERE block_type == 'Provider';
        """
        ).fetchall()
        log.debug(f"Tried listing all providers in the cache, got: {res}")

        return [Provider(type="Provider", hash=p[0], name=p[1]) for p in res]

    @classmethod
    def from_name(cls, name: str) -> "Provider":
        """
        Returns the named provider as an object
        """
        res = cls._db.sql(
            """
            SELECT block_id, block_name FROM block 
            WHERE block_type == 'Provider' 
            AND block_name == ?;                    
        """,
            (name,),
        ).fetchone()
        new_obj = Provider(type="Provider", hash=res[0], name=res[1])
        return new_obj

    def list_all(self):
        """
        Lists all Resources and Data Sources belonging to the provider
        """
        res = self._db.sql(
            """
            SELECT block_id, block_name, block_type FROM block
            WHERE block_type IN ('Resource', 'DataSource')
            AND parent_id == ?;
        """,
            (self.id,),
        ).fetchall()

        output = [
            (
                Resource(type="Resource", hash=block[0], name=block[1])
                if block[2] == "Resource"
                else DataSource(type="DataSource", hash=block[0], name=block[1])
            )
            for block in res
            if block[2] in ["Resource", "DataSource"]
        ]
        return output

    def list_resources(self):
        """
        Lists all Resources belonging to the provider
        """
        res = self._db.sql(
            """
            SELECT block_id, block_name FROM block
            WHERE block_type == 'Resource'
            AND parent_id == ?;
        """,
            (self.id,),
        ).fetchall()

        return [Resource(type="Resource", hash=r[0], name=r[1]) for r in res]

    def list_datasources(self):
        """
        Lists all DataSources belonging to the provider
        """
        res = self._db.sql(
            """
            SELECT block_id, block_name FROM block
            WHERE block_type == 'DataSource'
            AND parent_id == ?;
        """,
            (self.id,),
        ).fetchall()

        return [DataSource(type="DataSource", hash=d[0], name=d[1]) for d in res]
