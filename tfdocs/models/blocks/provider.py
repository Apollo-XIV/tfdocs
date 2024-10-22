from tfdocs.models.block import Block


class Provider(Block):
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
        new_obj = Provider(hash=res[0], name=res[1])
        return new_obj
