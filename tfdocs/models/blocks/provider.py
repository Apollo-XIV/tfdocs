import logging
from tfdocs.models.block import Block

log = logging.getLogger()


class Provider(Block):
    @classmethod
    def list_all(cls) -> list["Provider"]:
        """
        Returns the named provider as an object
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
