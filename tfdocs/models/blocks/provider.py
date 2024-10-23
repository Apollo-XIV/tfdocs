import logging
from tfdocs.models.block import Block

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
        return [Block(type=a[2], hash=a[0], name=a[1]) for a in res]

    def list_resources(self):
        pass

    def list_data_sources(self):
        pass
