from typing import Any

import jsonpickle


class JSONPickleSerializer:
    def dumps(self, value: Any) -> Any:
        return jsonpickle.dumps(value)

    def loads(self, string: Any) -> Any:
        return jsonpickle.loads(string)
