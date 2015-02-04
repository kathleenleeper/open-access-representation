def author(record):
        """
        Split author field into a list of "Name, Surname". 
        :param record: the record.
        :type record: dict
        :returns: dict -- the modified record.

        """
        if "author" in record:
            if record["author"]:
                record["author"] = getnames([i.strip() for i in record["author"].replace('\n', ' ').split(" and ")])
            else:
                del record["author"]         
        return record


